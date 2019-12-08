import random
import unittest

import pyceditor


class TestPycFile(unittest.TestCase):
    def test_pyc_edit(self):
        def f():
            return 123

        pyc = pyceditor.PycFile.load_from_pycode(f.__code__)
        code = pyc.code
        x = random.randint(15, 10**4)
        code.co_consts = (None, x)
        self.assertEqual(eval(pyc.pycode), x)
