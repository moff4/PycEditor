
import marshal
import unittest

import pyceditor


class MarshalMixin:
    def test_none(self):
        self._test(None)

    def test_true(self):
        self._test(True)

    def test_false(self):
        self._test(False)

    def test_ellipsis(self):
        self._test(...)
        self._test(Ellipsis)

    def test_stopiter(self):
        self._test(StopIteration)

    def test_int(self):
        self._test(123)

    # def test_big_int(self):
    #     # not yet implemented
    #     self._test(12312387123154125)

    def test_float(self):
        self._test(123.111)

    def test_tuple(self):
        self._test((1, 2, 3))

    def test_complex_tuple(self):
        self._test((1, (None,), ((((...,), ), ), ),), )

    def test_str(self):
        self._test('str')

    def test_bytes(self):
        self._test(b'str')

    def test_complex_str(self):
        self._test('str 12312!%')

    def test_cyrillic_str(self):
        self._test('лол кек чебурек')
        self._test('лол')

    def test_list(self):
        self._test(['чебурек', 123, (True, )])

    def test_set(self):
        self._test({'str', 123})

    def test_dict(self):
        self._test({'str': 123})
        self._test({...: [123.22], '<just null>': '<just null>'})


class TestSTD(unittest.TestCase, MarshalMixin):

    def _test(self, x):
        y = marshal.dumps(x)
        self.assertEqual(marshal.loads(y), x)


class TestPyceditor(unittest.TestCase, MarshalMixin):

    def _test(self, x):
        y = pyceditor.dumps(x)
        self.assertEqual(pyceditor.loads(y), x)


class TestLoad(unittest.TestCase, MarshalMixin):

    def _test(self, x):
        y = marshal.dumps(x)
        self.assertEqual(pyceditor.loads(y), x)


class TestWrite(unittest.TestCase, MarshalMixin):
    def _test(self, x):
        y = pyceditor.dumps(x)
        self.assertEqual(marshal.loads(y), x)

    def _code_tester(self, pycode):
        code_obj_1 = pyceditor.Code.from_pycode(pycode)
        code_obj_2 = pyceditor.loads(marshal.dumps(pycode))
        self.assertEqual(code_obj_1.__dict__, code_obj_2.__dict__)

    def test_code(self):
        def f(x):
            x = x ** 123
            return x / 123
        self._test(f.__code__)
        self._code_tester(f.__code__)
        self._test(self._test.__code__)
        self._code_tester(self._test.__code__)

    def test_complext_code(self):
        def f(x):
            x = x ** 123
            return x / 123

        def g(x):
            print('hello!', '(:')
            return x / 123

        self._test([g.__code__, f.__code__])
        self._test((f.__code__, g.__code__, f.__code__, [1, 2, 3, 1], self._test.__code__))
