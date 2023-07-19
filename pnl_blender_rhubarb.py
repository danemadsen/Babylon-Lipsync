import bpy
from bpy_extras.io_utils import ImportHelper
from . import  op_blender_rhubarb

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
        shape_keys = context.object.data.shape_keys.key_blocks

        if shape_keys:
            prop = context.object.data.shape_keys.mouth_shapes

            row = layout.row(align=True)
            row.prop(prop, 'sound_file', text='Sound file')

            row = layout.row(align=True)
            row.prop(prop, 'dialog_file', text='Dialog file')

            row = layout.row()
            row.prop(prop, 'start_frame', text='Start frame')

            row = layout.row()

            if not (context.preferences.addons[__package__].preferences.executable_path):
                row.label(text="Please set rhubarb executable location in addon preferences")
                row = layout.row()

            row.operator(operator = "object.rhubarb_lipsync")

        else:
            row = layout.row(align=True)
            row.label(text="Rhubarb Lipsync requires shape keys")

def register():
    bpy.utils.register_class(RhubarbLipsyncPanel)

def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncPanel)
