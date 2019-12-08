import sys
from dataclasses import dataclass

TYPE_NULL = '0'
TYPE_NONE = 'N'
TYPE_FALSE = 'F'
TYPE_TRUE = 'T'
TYPE_STOPITER = 'S'
TYPE_ELLIPSIS = '.'
TYPE_INT = 'i'
TYPE_INT64 = 'I'
TYPE_FLOAT = 'f'
TYPE_BINARY_FLOAT = 'g'
TYPE_COMPLEX = 'x'
TYPE_BINARY_COMPLEX = 'y'
TYPE_LONG = 'l'
TYPE_STRING = 's'
TYPE_INTERNED = 't'
TYPE_REF = 'r'
TYPE_TUPLE = '('
TYPE_LIST = '['
TYPE_DICT = '{'
TYPE_CODE = 'c'
TYPE_UNICODE = 'u'
TYPE_UNKNOWN = '?'
TYPE_SET = '<'
TYPE_FROZENSET = '>'
TYPE_ASCII = 'a'
TYPE_ASCII_INTERNED = 'A'
TYPE_SMALL_TUPLE = ')'
TYPE_SHORT_ASCII = 'z'
TYPE_SHORT_ASCII_INTERNED = 'Z'


@dataclass
class Code:
    co_argcount: int
    if sys.version_info[1] >= 8:
        co_posonlyargcount: int
    co_kwonlyargcount: int
    co_nlocals: int
    co_stacksize: int
    co_flags: int
    co_code: bytes
    co_consts: tuple
    co_names: str
    co_varnames: tuple
    co_freevars: tuple
    co_cellvars: tuple
    co_filename: str
    co_name: str
    co_firstlineno: int
    co_lnotab: str

    @classmethod
    def from_dict(cls, params):
        return cls(
            **{
                key: value
                for key, value in params.items()
            }
        )

    @classmethod
    def from_pycode(cls, pycode):
        return cls(
            **{
                key: getattr(pycode, key)
                for key in dir(pycode)
                if key.startswith('co_')
            }
        )
