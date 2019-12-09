
import time
import marshal
import importlib._bootstrap_external

from .load import load, loads, _r_long
from .dump import dump, dumps, _w_long
from .types import Code


class PycFile:
    def __init__(self, filename):
        self.filename = filename
        self._loaded = False

    def load(self):
        with open(self.filename, 'rb') as f:
            self.magic_number = f.read(4)
            assert self.magic_number == importlib._bootstrap_external.MAGIC_NUMBER
            _r_long(f)  # zeros
            self.timestamp = _r_long(f)
            self.source_size = _r_long(f)
            self._code = loads(f.read())
        self._loaded = True

    @classmethod
    def load_from_code(cls, code):
        self = cls(code.co_filename)
        self._code = code
        self.timestamp = int(time.time())
        self.source_size = 0
        self._loaded = True
        return self

    @classmethod
    def load_from_pycode(cls, pycode):
        code = loads(marshal.dumps(pycode))
        self = cls(code.co_filename)
        self._code = code
        self.timestamp = int(time.time())
        self.source_size = 0
        self._loaded = True
        return self

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, *a, **b):
        self.save()

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, new_code):
        if not isinstance(new_code, (Code, type(self.__init__.__code__))):
            raise TypeError('Invalid type %s for code' % type(new_code))
        self._code = new_code
        if not self._loaded:
            self._loaded = True
            self.timestamp = int(time.time())
            self.source_size = 0
            self.magic_number = importlib._bootstrap_external.MAGIC_NUMBER

    def save(self, source_size=None, reset_timestamp=True):
        if not self._loaded:
            raise ValueError('File not loaded; use .load() before .save()')
        if reset_timestamp:
            self.timestamp = int(time.time())
        if source_size:
            self.source_size = source_size
        code = dumps(self._code)
        with open(self.filename, 'wb') as f:
            f.write(self.magic_number)
            f.write(bytes(_w_long(0)))
            f.write(bytes(_w_long(self.timestamp)))
            f.write(bytes(_w_long(self.source_size)))
            f.write(code)
        self._loaded = False

    @property
    def pycode(self):
        return marshal.loads(dumps(self._code))


__all__ = [
    'load',
    'loads',
    'dump',
    'dumps',
    'Code',
    'PycFile',
]
