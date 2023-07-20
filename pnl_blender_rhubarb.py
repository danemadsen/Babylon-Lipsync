import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import PointerProperty, StringProperty, IntProperty, EnumProperty
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

    dialog_text: StringProperty(
        name="Dialog",
        description="Enter the dialog here",
        default="",
        maxlen=1024,
    )

    start_frame: IntProperty(
        name="Start Frame",
        description="Start frame for the lip-sync",
        default=0,
    )

    def get_shape_keys(self, context):
        obj = context.object
        items = [(str(index), key.name, key.name) for index, key in enumerate(obj.data.shape_keys.key_blocks)]
        return items

    phoneme_REST: EnumProperty(
        name="Phoneme rest",
        description="Shape key for the 'rest' phoneme",
        items=get_shape_keys
    )

    phoneme_AI: EnumProperty(
        name="Phoneme AI",
        description="Shape key for the 'AI' phoneme",
        items=get_shape_keys
    )

    phoneme_E: EnumProperty(
        name="Phoneme E",
        description="Shape key for the 'E' phoneme",
        items=get_shape_keys
    )

    phoneme_ETC: EnumProperty(
        name="Phoneme etc",
        description="Shape key for the 'etc' phoneme",
        items=get_shape_keys
    )

    phoneme_FV: EnumProperty(
        name="Phoneme FV",
        description="Shape key for the 'FV' phoneme",
        items=get_shape_keys
    )

    phoneme_L: EnumProperty(
        name="Phoneme L",
        description="Shape key for the 'L' phoneme",
        items=get_shape_keys
    )

    phoneme_MBP: EnumProperty(
        name="Phoneme MBP",
        description="Shape key for the 'MBP' phoneme",
        items=get_shape_keys
    )

    phoneme_O: EnumProperty(
        name="Phoneme O",
        description="Shape key for the 'O' phoneme",
        items=get_shape_keys
    )

    phoneme_U: EnumProperty(
        name="Phoneme U",
        description="Shape key for the 'U' phoneme",
        items=get_shape_keys
    )

    phoneme_WQ: EnumProperty(
        name="Phoneme WQ",
        description="Shape key for the 'WQ' phoneme",
        items=get_shape_keys
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
        row.prop(my_tool, 'dialog_text', text='Dialog')

        row = layout.row()
        row.prop(my_tool, 'start_frame', text='Start frame')

        layout.label(text="Phoneme to Shape Key Mapping:")

        row = layout.row()
        row.prop(my_tool, 'phoneme_AI', text='AI')

        row = layout.row()
        row.prop(my_tool, 'phoneme_E', text='E')

        row = layout.row()
        row.prop(my_tool, 'phoneme_ETC', text='ETC')

        row = layout.row()
        row.prop(my_tool, 'phoneme_FV', text='FV')

        row = layout.row()
        row.prop(my_tool, 'phoneme_L', text='L')

        row = layout.row()
        row.prop(my_tool, 'phoneme_MBP', text='MBP')

        row = layout.row()
        row.prop(my_tool, 'phoneme_O', text='O')

        row = layout.row()
        row.prop(my_tool, 'phoneme_REST', text='REST')

        row = layout.row()
        row.prop(my_tool, 'phoneme_U', text='U')

        row = layout.row()
        row.prop(my_tool, 'phoneme_WQ', text='WQ')

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
