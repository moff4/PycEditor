import sys
import struct

from .types import *


TYPE_WRITERS = {}


def reg_writer(key):
    def wrapper(func):
        TYPE_WRITERS[key] = func
        return func
    return wrapper


def _w_type(type_):
    yield from type_.encode()


def _w_byte(obj):
    yield obj & 0xff


def _w_short(obj):
    yield from _w_byte(obj)
    yield from _w_byte(obj >> 8)


def _w_long(obj):
    if obj > 2 ** 32:
        raise NotImplementedError
    yield from _w_byte(obj)
    yield from _w_byte(obj >> 8)
    yield from _w_byte(obj >> 16)
    yield from _w_byte(obj >> 24)


@reg_writer(type(None))
def _w_none(obj):
    yield from _w_type(TYPE_NONE)


@reg_writer(type(...))
def _w_ellipsis(obj):
    yield from _w_type(TYPE_ELLIPSIS)


def _w_true(obj):
    yield from _w_type(TYPE_TRUE)


def _w_false(obj):
    yield from _w_type(TYPE_FALSE)


@reg_writer(StopIteration)
def _w_stopiter(obj):
    yield from _w_type(TYPE_STOPITER)


@reg_writer(int)
def _w_int(obj):
    yield from _w_type(TYPE_INT)
    yield from _w_long(obj)


@reg_writer(float)
def _w_float(obj):
    yield from _w_type(TYPE_BINARY_FLOAT)
    yield from struct.pack('d', obj)


@reg_writer(bytes)
def _w_bytes(obj):
    yield from _w_type(TYPE_STRING)
    yield from _w_long(len(obj))
    yield from obj


@reg_writer(str)
def _w_str(obj):
    yield from _w_type(TYPE_UNICODE)
    obj = obj.encode('utf-8')
    yield from _w_long(len(obj))
    yield from obj


@reg_writer(set)
def _w_set(obj):
    yield from _w_type(TYPE_SET)
    yield from _w_long(len(obj))
    for item in obj:
        yield from _dumps(item)


@reg_writer(list)
def _w_list(obj):
    yield from _w_type(TYPE_LIST)
    yield from _w_long(len(obj))
    for item in obj:
        yield from _dumps(item)


@reg_writer(tuple)
def _w_tuple(obj):
    yield from _w_type(TYPE_TUPLE)
    yield from _w_long(len(obj))
    for item in obj:
        yield from _dumps(item)


@reg_writer(dict)
def _w_dict(obj):
    yield from _w_type(TYPE_DICT)
    for key, value in obj.items():
        yield from _dumps(key)
        yield from _dumps(value)
    yield from _w_type(TYPE_NULL)


@reg_writer(type(reg_writer.__code__))
@reg_writer(Code)
def _w_code(obj):
    yield from _w_type(TYPE_CODE)
    yield from _w_long(obj.co_argcount)
    if sys.version_info[1] >= 8:
        yield from _w_long(obj.co_posonlyargcount)
    yield from _w_long(obj.co_kwonlyargcount)
    yield from _w_long(obj.co_nlocals)
    yield from _w_long(obj.co_stacksize)
    yield from _w_long(obj.co_flags)
    yield from _dumps(obj.co_code)
    yield from _dumps(obj.co_consts)
    yield from _dumps(obj.co_names)
    yield from _dumps(obj.co_varnames)
    yield from _dumps(obj.co_freevars)
    yield from _dumps(obj.co_cellvars)
    yield from _dumps(obj.co_filename)
    yield from _dumps(obj.co_name)
    yield from _w_long(obj.co_firstlineno)
    yield from _dumps(obj.co_lnotab)


def _dumps(obj) -> bytes:
    if isinstance(obj, bool):
        res = (_w_true if obj else _w_false)(obj)
    else:
        for key in TYPE_WRITERS:
            if key == obj or (isinstance(key, type) and isinstance(obj, key)):
                res = TYPE_WRITERS[key](obj)
                break
        else:
            raise TypeError('unexpected type "%s"' % type(obj))

    yield from res


def dumps(obj) -> bytes:
    res = bytes(_dumps(obj))
    return b''.join([res])


def dump(fd, obj):
    fd.write(dumps(obj))
