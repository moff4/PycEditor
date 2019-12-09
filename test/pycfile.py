import sys
import dis
import random
import unittest

import pyceditor


class TestPycFile(unittest.TestCase):
    def test_edit_consts(self):
        def f():
            return 123

        pyc = pyceditor.PycFile.load_from_pycode(f.__code__)
        code = pyc.code
        x = random.randint(15, 10**4)
        code.co_consts = (None, x)
        self.assertEqual(eval(pyc.pycode), x)

    def test_bytecode_edit(self):
        args = {
            'co_argcount': 0,
            'co_kwonlyargcount': 0,
            'co_nlocals': 0,
            'co_stacksize': 2,
            'co_flags': 64,
            'co_code': bytes(
                [
                    dis.opmap['LOAD_NAME'], 0,
                    dis.opmap['LOAD_CONST'], 0,
                    dis.opmap['BINARY_MULTIPLY'], 0,
                    dis.opmap['RETURN_VALUE'], 0,
                ],
            ),
            'co_consts': (3, 'any else'),
            'co_names': ('x',),
            'co_varnames': (),
            'co_freevars': (),
            'co_cellvars': (),
            'co_filename': '<stdin>',
            'co_name': '<module>',
            'co_firstlineno': 1,
            'co_lnotab': b'',
        }
        if sys.version_info[1] >= 8:
            args['co_posonlyargcount'] = 0
        code = pyceditor.Code(**args)
        pyc = pyceditor.PycFile.load_from_code(code)
        self.assertEqual(eval(pyc.pycode, {'x': 123}), 123 * 3)
        self.assertEqual(eval(pyc.pycode, {'x': '123'}), '123123123')
