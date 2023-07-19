import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty
import blf
import bgl
import io
import sys
import select
import subprocess
from threading  import Thread
from queue import Queue, Empty
import json
import os

class RhubarbLipsyncOperator(bpy.types.Operator):
    """Run Rhubarb lipsync"""
    bl_idname = "object.rhubarb_lipsync"
    bl_label = "Rhubarb lipsync"

    cue_prefix = 'Mouth_'
    hold_frame_threshold = 4
    sound_file: StringProperty(
        name="Sound File",
        subtype='FILE_PATH',
    )
    dialog_file: StringProperty(
        name="Dialog File",
        subtype='FILE_PATH',
    )

    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.executable_path and \
            context.object.data.shape_keys

    def invoke(self, context, event):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        inputfile = bpy.path.abspath(self.sound_file)
        dialogfile = bpy.path.abspath(self.dialog_file)
        recognizer = bpy.path.abspath(addon_prefs.recognizer)
        executable = bpy.path.abspath(addon_prefs.executable_path)

        os.chmod(executable, 0o744)

        command = [executable, "-f", "json", "--machineReadable", "--extendedShapes", "GHX", "-r", recognizer, inputfile]

        if dialogfile:
            command.append("--dialogFile")
            command.append(dialogfile)

        self.rhubarb = subprocess.Popen(command,
                                        stdout=subprocess.PIPE, universal_newlines=True)

        wm = context.window_manager
        self._timer = wm.event_timer_add(2, window=context.window)
        wm.modal_handler_add(self)
        wm.progress_begin(0, 100)

        return {'RUNNING_MODAL'}

    def execute(self, context):
        return self.invoke(context, None)

    def finished(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)



def register():
    bpy.utils.register_class(RhubarbLipsyncOperator)


def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncOperator)

if __name__ == "__main__":
    register()

