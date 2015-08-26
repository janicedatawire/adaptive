# Helpers for generating Python code

import sys

py_reserved = set("id is class def".split())  # FIXME
def py_name(name):
    if name in py_reserved:
        return name + "_"
    return name


sdl_to_python = {
    "int32": "int",
    "int64": "int",
    "double": "float",
    "string": "basestring"
}
def py_Typename(name):
    return sdl_to_python.get(name, name)


class Pythonize(object):
    "Add py_name node attributes"

    def visit_DEFAULT(self, node):
        print "DEFAULT", repr(node)

    def visit_Module(self, node):
        node.py_name = py_name(node.name)

    def visit_Struct(self, node):
        node.py_name = py_name(node.name)

    def visit_Field(self, node):
        node.py_name = py_name(node.name)

    def visit_Parameter(self, node):
        node.py_name = py_name(node.name)
        if node.default:
            if node.default.name == "null":
                node.default.py_name = "None"
            else:
                node.default.py_name = repr(node.default.name)

    def visit_Operation(self, node):
        node.py_name = py_name(node.name)

    def visit_Type(self, node):
        node.py_name = py_Typename(node.name)


class PyOutput(object):
    "Generate decent-looking Python code"

    def __init__(self):
        self.lines = []
        self.main_indent_level = 0
        self.ref_indent_level = 0

    def out(self, line):
        self.lines.append(self.main_indent_level * "    " + line.strip())

    def ref(self, line):
        self.lines.append("## " + self.ref_indent_level * "    " + line.strip())

    def indent(self):
        self.main_indent_level += 1

    def dedent(self):
        assert self.main_indent_level > 0, (self.main_indent_level, "\n".join(self.lines))
        self.main_indent_level -= 1

    def ref_indent(self):
        self.ref_indent_level += 1

    def ref_dedent(self):
        assert self.ref_indent_level > 0, (self.ref_indent_level, "\n".join(self.lines))
        self.ref_indent_level -= 1

    def dump(self, fd=sys.stdout):
        # Fancy print...
        wasPassThru = True
        for line in self.lines:
            isPassThru = line.startswith("## ")
            if isPassThru != wasPassThru:
                fd.write("\n")
            fd.write(line)
            fd.write("\n")
            wasPassThru = isPassThru


def assertListOf(lst, typ, orNone=True):
    assert isinstance(lst, list), lst
    if orNone:
        for idx, value in enumerate(lst):
            assert value is None or isinstance(value, typ), (idx, value)
    else:
        for idx, value in enumerate(lst):
            assert isinstance(value, typ), (idx, value)
    return True


def emitTypeCheck(out, name, typ, orNone=True):
    d = dict(name=name, typ=typ.py_name)
    if typ.name == "void":
        out("assert %(name)s is None, %(name)s" % d)
    elif typ.parameters:
        assert len(typ.parameters) == 1, "Unimplemented: %s" % typ
        assert typ.name == "List",  "Unimplemented: %s" % typ
        d["param"] = typ.parameters[0].py_name
        if orNone:
            out("assert %(name)s is None or _assertListOf(%(name)s, %(param)s), %(name)s" % d)
        else:
            out("_assertListOf(%(name)s, %(param)s), %(name)s" % d)
    else:
        if orNone:
            out("assert %(name)s is None or isinstance(%(name)s, %(typ)s), %(name)s" % d)
        else:
            out("assert isinstance(%(name)s, %(typ)s), %(name)s" % d)