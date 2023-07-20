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

    phoneme_A: EnumProperty(
        name="Phoneme A",
        description="Closed mouth for the \"P\", \"B\", and \"M\" sounds. This is almost identical to the 'X' shape, but there is ever-so-slight pressure between the lips.",
        items=get_shape_keys
    )

    phoneme_B: EnumProperty(
        name="Phoneme B",
        description="Slightly open mouth with clenched teeth. This mouth shape is used for most consonants (\"K\", \"S\", \"T\", etc.). It's also used for some vowels such as the \"EE\" sound in bee.",
        items=get_shape_keys
    )

    phoneme_C: EnumProperty(
        name="Phoneme C",
        description="Open mouth. This mouth shape is used for vowels like \"EH\" as in men and \"AE\" as in bat. It's also used for some consonants, depending on context. This shape is also used as an in-between when animating from 'A' or 'B' to 'D'.",
        items=get_shape_keys
    )

    phoneme_D: EnumProperty(
        name="Phoneme D",
        description="Wide open mouth. This mouth shapes is used for vowels like \"AA\" as in father.",
        items=get_shape_keys
    )

    phoneme_E: EnumProperty(
        name="Phoneme E",
        description="Slightly rounded mouth. This mouth shape is used for vowels like \"AO\" as in off and \"ER\" as in bird.",
        items=get_shape_keys
    )

    phoneme_F: EnumProperty(
        name="Phoneme F",
        description="Puckered lips. This mouth shape is used for \"UW\" as in you, \"OW\" as in show, and \"W\" as in way.",
        items=get_shape_keys
    )

    phoneme_G: EnumProperty(
        name="Phoneme G",
        description="Upper teeth touching the lower lip for \"F\" as in for and \"V\" as in very.",
        items=get_shape_keys
    )

    phoneme_H: EnumProperty(
        name="Phoneme H",
        description="This shape is used for long \"L\" sounds, with the tongue raised behind the upper teeth.",
        items=get_shape_keys
    )

    phoneme_X: EnumProperty(
        name="Phoneme X",
        description="Shape key for the 'rest' phoneme",
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
        row.prop(my_tool, 'phoneme_A', text='A')

        row = layout.row()
        row.prop(my_tool, 'phoneme_B', text='B')

        row = layout.row()
        row.prop(my_tool, 'phoneme_C', text='C')

        row = layout.row()
        row.prop(my_tool, 'phoneme_D', text='D')

        row = layout.row()
        row.prop(my_tool, 'phoneme_E', text='E')

        row = layout.row()
        row.prop(my_tool, 'phoneme_F', text='F')

        row = layout.row()
        row.prop(my_tool, 'phoneme_G', text='G')

        row = layout.row()
        row.prop(my_tool, 'phoneme_H', text='H')

        row = layout.row()
        row.prop(my_tool, 'phoneme_X', text='X')

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
