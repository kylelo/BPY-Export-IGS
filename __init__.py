import bpy
import math

from .operators.polyhedral_splines import PolyhedralSplines
from .operators.highlighter import Highlighter
from .operators.main_ui import MainUI
from .operators.ui_helper import ToggleFaces, ToggleSurfPatchCollection
from .operators.ui_color import COLOR_OT_TemplateOperator

bl_info = {
    "name": "polyhedral_splines",
    "description": "An interactive spline generation addon",
    "version": (1, 0, 0),
    "blender": (2, 80, 2),
    "category": "Modeling"
}

classes = (
    PolyhedralSplines,
    Highlighter,
    ToggleFaces,
    ToggleSurfPatchCollection,
    MainUI,
    COLOR_OT_TemplateOperator
)

register, unregister = bpy.utils.register_classes_factory(classes)
def write_some_data(context, filepath):
    f = open(filepath, 'w', encoding='utf-8')
    f.write("copyright(c)Jorg Peters [jorg.peters@gmail.com]                         S      1\n")
    patch_obj = bpy.context.active_object
    k = None
    k1 = None
    w = None
    w1 = None
    rows = None
    flen = [0 for _ in range(4)]
    i = None
    m = None
    j = None
    col = None
    cols = None
    fc = None
    sds = None
    dg = None
    h = None
    
    #int facelen = 2
    t_Bbctr = 1
    t_Ffctr = 1

    fc = 0
    while fc < m_Patches.size():

        t_Patch = m_Patches[fc]
        t_DegU = t_Patch.m_DegU
        t_DegV = t_Patch.m_DegV

        #k = (dg+1)*2
        k = (t_DegU + 1) + (t_DegV + 1)
        k1 = 1 if (math.fmod(k, 8) != 0) + math.trunc(k / float(8)) else 0 # knots
        w = (t_DegU + 1) * (t_DegV + 1)
        w1 = 1 if (math.fmod(w, 8) != 0) + math.trunc(w / float(8)) else 0 # weights

        # deg-line, knots, weights, xyz location, param 
        rows = (1 + 2 * k1 + w1 + w + 1) # size of one block

        f.write("     128%8d       0       1       0       0       0        00000000D%7d\n"(t_Bbctr, t_Ffctr))
        f.write("     128%8d       8      %d       2                NurbSurf       0D%7d\n"(0, rows, t_Ffctr+1))

        t_Bbctr += rows
        t_Ffctr += 2
        fc += 1
    flen[0] = 1
    flen[1] = 10

    # data entries 
    t_Ffctr = 1
    t_Bbctr = 1
    fc = 0
    while fc < m_Patches.size():

        t_Patch = m_Patches[fc]
        t_DegU = t_Patch.m_DegU
        t_DegV = t_Patch.m_DegV

        # HEADER 
        f.write("128,%7d,%7d,%7d,%7d,0,0,1,0,0,%26dP%7d\n"(t_DegV, t_DegU, t_DegV, t_DegU, t_Ffctr, t_Bbctr))
        t_Bbctr += 1

        # KNOTS 
        w = (t_DegU + 1) * (t_DegV + 1)
        g = None
        h = None
        a_Deg1 = t_DegV + 1

        for g in range(0, a_Deg1):
            if (math.fmod(g, 8) == 0) and (g != 0):
                f.write("%8dP%7d\n"(t_Ffctr, t_Bbctr))
                t_Bbctr += 1
            f.write("0.00000,")
        while g< 2 *a_Deg1:
            if math.fmod(i, 8) == 0:
                f.write("%8dP%7d\n"(t_Ffctr, t_Bbctr))
                t_Bbctr += 1
            f.write("1.00000,")
            g += 1
        h = math.fmod((2 *a_Deg1), 8)
        if h != 0:
            h = 8 - j
            for g in range(0, h):
                f.write(fp,"        ")

        f.write("%8dP%7d\n"(t_Ffctr,t_Bbctr))
        t_Bbctr += 1
        d = None
        e = None
        a_Deg1 = t_DegV + 1

        for d in range(0, a_Deg1):
            if (math.fmod(d, 8) == 0) and (d != 0):
                f.write("%8dP%7d\n"(t_Ffctr, t_Bbctr))
                t_Bbctr += 1
            f.write("0.00000,")
        while d < 2 *a_Deg1:
            if math.fmod(d, 8) == 0:
                f.write("%8dP%7d\n"(t_Ffctr, t_Bbctr))
                t_Bbctr += 1
            f.write("1.00000,")
            d += 1
        e = math.fmod((2 *a_Deg1), 8)
        if e != 0:
            e = 8 - e
            for d in range(0, e):
                f.write(fp,"        ")

        f.write("%8dP%7d\n"(t_Ffctr,t_Bbctr))
        t_Bbctr += 1
        #t_Bbctr = IGSWriter.knots(t_DegV + 1, t_Bbctr, t_Ffctr, m_OutFile, 8)
        #t_Bbctr = IGSWriter.knots(t_DegU + 1, t_Bbctr, t_Ffctr, m_OutFile, 8)

        # the w==RATIONAL coordinate 
        cols = 8
        col = 0
        for i in range(0, t_DegU + 1):
            for j in range(0, t_DegV + 1):
                if (math.fmod(col, cols) == 0) and (col != 0):
                    f.write("%8dP%7d\n" (t_Ffctr,t_Bbctr))
                    t_Bbctr += 1
                h = 1
                f.write("%7.5f,", h)
                col += 1

        # finish line 
        col = math.fmod(col, cols)
        if col != 0:
            col = cols-col
            for i in range(0, col):
                f.write("        ")

        f.write("%8dP%7d\n", t_Ffctr, t_Bbctr)
        t_Bbctr += 1

        # the XYZ coordinates 
        for i in range(0, t_DegU + 1):
            for j in range(0, t_DegV + 1):
                f.write(m_OutFile,"%20e,%20e,%20e,%9dP%7d\n", t_Patch.m_BBcoefs[i][j][0], t_Patch.m_BBcoefs[i][j][1], t_Patch.m_BBcoefs[i][j][2], t_Ffctr,t_Bbctr)
                t_Bbctr += 1

        f.write("0.00000,1.00000,0.00000,1.00000;%40dP%7d\n", t_Ffctr, t_Bbctr)
        t_Bbctr += 1
        t_Ffctr += 2
        fc += 1
    flen[2] = t_Ffctr
    flen[3] = t_Bbctr

    # structure of file 
    f.write("S%7dG%7dD%7dP%7d%40dT%7d\n", flen[0], flen[1], flen[2] - 1, flen[3] - 1, 1, 1)
    f.close




# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportData(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export IGS"

    # ExportHelper mixin class uses this
    filename_ext = ".igs"

    filter_glob: StringProperty(
        default="*.igs",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    def execute(self, context):
        return write_some_data(context, self.filepath)


def menu_func_export(self, context):
    self.layout.operator(ExportData.bl_idname, text="IGS Export Operator")


# Register and add to the "file selector" menu (required to use F3 search "IGS Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
