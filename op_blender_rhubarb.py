import bpy
from bpy.props import IntProperty, FloatProperty, StringProperty
import blf
import bgl
import io
import sys
import select
import subprocess
from threading import Thread
from queue import Queue, Empty
import json
import os

phoneme_translation_dict = {
    'X': 'phoneme_REST',
    'A': 'phoneme_AI',
    'B': 'phoneme_E',
    'C': 'phoneme_ETC',
    'D': 'phoneme_O',
    'E': 'phoneme_U',
    'F': 'phoneme_FV',
    'G': 'phoneme_WQ',
    'H': 'phoneme_L'
}

def translate_phoneme(context, phoneme):
    if phoneme in phoneme_translation_dict:
        property_name = phoneme_translation_dict[phoneme]
        if hasattr(context.scene.my_tool, property_name):
            shape_key_index = int(getattr(context.scene.my_tool, property_name))
            print(shape_key_index)
            shape_key_name = context.object.data.shape_keys.key_blocks[shape_key_index].name
            print(shape_key_name)
            return shape_key_name
    return None

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

    def modal(self, context, event):
        wm = context.window_manager
        wm.progress_update(50)

        try:
            (stdout, stderr) = self.rhubarb.communicate(timeout=1)

            try:
                result = json.loads(stderr)
                if result['type'] == 'progress':
                    print(result['log']['message'])
                    self.message = result['log']['message']

                if result['type'] == 'failure':
                    self.report(type={'ERROR'}, message=result['reason'])
                    return {'CANCELLED'}

            except ValueError:
                pass
            except TypeError:
                pass
            except json.decoder.JSONDecodeError:
                print("JSON Decode Error!!!")
                print("stdout: ", stdout)
                print("stderr: ", stderr)
                pass

            self.rhubarb.poll()

            if self.rhubarb.returncode is not None:
                wm.event_timer_remove(self._timer)
                results = json.loads(stdout)
                fps = context.scene.render.fps
                last_frame = 0
                last_shape_key_name = None

                for cue in results['mouthCues']:
                    frame_num = round(cue['start'] * fps)
                    shape_key_name = translate_phoneme(context, cue['value'])
                    print("start: {0} frame: {1} value: {2} shape key: {3}".format(cue['start'], frame_num , cue['value'], shape_key_name))
                
                    if shape_key_name:
                        # Set all shape keys to 0.0 at the start of this phoneme.
                        for key in context.object.data.shape_keys.key_blocks:
                            key.value = 0.0
                            key.keyframe_insert('value', frame=frame_num - 1)
                
                        # Set the current shape key to 1.0.
                        context.object.data.shape_keys.key_blocks[shape_key_name].value = 1.0
                        context.object.data.shape_keys.key_blocks[shape_key_name].keyframe_insert('value', frame=frame_num)
                
                        last_shape_key_name = shape_key_name
                
                # Set all shape keys to 0.0 after the last phoneme.
                for key in context.object.data.shape_keys.key_blocks:
                    key.value = 0.0
                    key.keyframe_insert('value', frame=frame_num + 1)


                if last_shape_key_name:
                    context.object.data.shape_keys.key_blocks[last_shape_key_name].value = 0.0
                    context.object.data.shape_keys.key_blocks[last_shape_key_name].keyframe_insert('value', frame=frame_num + 1)

                wm.progress_end()
                return {'FINISHED'}

            return {'PASS_THROUGH'}
        except subprocess.TimeoutExpired as ex:
            return {'PASS_THROUGH'}
        except json.decoder.JSONDecodeError:
            print("JSON Decode Error!!!")
            print("stdout: ", stdout)
            print("stderr: ", stderr)
            wm.progress_end()
            return {'CANCELLED'}
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            print(template.format(type(ex).__name__, ex.args))
            wm.progress_end()
            return {'CANCELLED'}

    def invoke(self, context, event):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
    
        inputfile = bpy.path.abspath(context.scene.my_tool.sound_file)
        print(f"Self.sound_file: {context.scene.my_tool.sound_file}")
        print(f"Inputfile: {inputfile}")
        if not os.path.isfile(inputfile):
            print(f"File does not exist: {inputfile}")
        dialogfile = bpy.path.abspath(context.scene.my_tool.dialog_file)
        recognizer = bpy.path.abspath(addon_prefs.recognizer)
        executable = bpy.path.abspath(addon_prefs.executable_path)
    
        os.chmod(executable, 0o744)
    
        command = [executable, "-f", "json", "--machineReadable", "--extendedShapes", "GHX", "-r", recognizer, inputfile]
    
        if dialogfile:
            command.append("--dialogFile")
            command.append(dialogfile)
    
        self.rhubarb = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
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
