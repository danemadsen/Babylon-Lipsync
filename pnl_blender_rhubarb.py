import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import PointerProperty, StringProperty, IntProperty
from bpy.types import PropertyGroup
from . import op_blender_rhubarb

class MyProperties(PropertyGroup):

    sound_file: StringProperty(
        name="Sound File",
        description="Path to the sound file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    dialog_file: StringProperty(
        name="Dialog File",
        description="Path to the dialog file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
    )

    start_frame: IntProperty(
        name="Start Frame",
        description="Start frame for the lip-sync",
        default=0,
    )

class RhubarbLipsyncPanel(bpy.types.Panel):
    bl_idname = "DATA_PT_rhubarb_lipsync"
    bl_label = "Rhubarb Lipsync"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return (obj and obj.type == 'MESH' and obj.data.shape_keys)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        my_tool = scene.my_tool


        row = layout.row(align=True)
        row.prop(my_tool, 'sound_file', text='Sound file')

        row = layout.row(align=True)
        row.prop(my_tool, 'dialog_file', text='Dialog file')

        row = layout.row()
        row.prop(my_tool, 'start_frame', text='Start frame')

        row = layout.row()

        if not (context.preferences.addons[__package__].preferences.executable_path):
            row.label(text="Please set rhubarb executable location in addon preferences")
            row = layout.row()

        row.operator(operator = "object.rhubarb_lipsync")

def register():
    bpy.utils.register_class(MyProperties)
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)
    bpy.utils.register_class(RhubarbLipsyncPanel)

def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncPanel)
    del bpy.types.Scene.my_tool
    bpy.utils.unregister_class(MyProperties)

if __name__ == "__main__":
    register()
