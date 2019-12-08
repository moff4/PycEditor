#!/usr/bin/env python3.8
import sys
import struct
from io import BytesIO

from .types import *

TYPE_READERS = {}

NULL_OBJECT = object()


REF = []


def reg_parser(char):
    def wrapper(func):
        TYPE_READERS[ord(char)] = func
        return func
    return wrapper


@reg_parser(TYPE_NULL)
def _r_null(source, flag):
    return NULL_OBJECT


@reg_parser(TYPE_ELLIPSIS)
def _r_ellipses(source, flag):
    return ...


@reg_parser(TYPE_STOPITER)
def _r_stopiter(source, flag):
    return StopIteration


@reg_parser(TYPE_NONE)
def _r_none(source, flag):
    return None


@reg_parser(TYPE_FALSE)
def _r_false(source, flag):
    return False


@reg_parser(TYPE_TRUE)
def _r_true(source, flag):
    return True


def _r_byte(source):
    return source.read(1)[0]


def _r_long(source):
    x = 0
    for i in source.read(4)[::-1]:
        x = x << 8 | i
    return x


@reg_parser(TYPE_INT)
def _r_int(source, flag):
    res = _r_long(source)
    if flag:
        REF.append(res)
    return res


@reg_parser(TYPE_LONG)
def _r_long_int(source, flag):
    raise NotImplementedError


@reg_parser(TYPE_FLOAT)
def _r_float(source, flag):
    n = _r_byte(source)
    res = float(source.read(n))
    if flag:
        REF.append(res)
    return res


@reg_parser(TYPE_BINARY_FLOAT)
def _r_binary_float(source, flag):
    res = struct.unpack('d', source.read(8))[0]
    if flag:
        REF.append(res)
    return res


@reg_parser(TYPE_SMALL_TUPLE)
def _r_small_tuple(source, flag):
    if flag:
        idx = len(REF)
        REF.append(None)
    res = tuple(_r_object(source) for i in range(_r_byte(source)))
    if flag:
        REF[idx] = res
    return res


@reg_parser(TYPE_TUPLE)
def _r_tuple(source, flag):
    if flag:
        idx = len(REF)
        REF.append(None)
    res = tuple(_r_object(source) for i in range(_r_long(source)))
    if flag:
        REF[idx] = res
    return res


@reg_parser(TYPE_STRING)
def _r_string(source, flag):
    res = source.read(_r_long(source))
    if flag:
        REF.append(res)
    return res


@reg_parser(TYPE_SHORT_ASCII)
@reg_parser(TYPE_SHORT_ASCII_INTERNED)
def _r_short_ascii(source, flag):
    res = source.read(_r_byte(source)).decode('utf-8')
    if flag:
        REF.append(res)
    return res


@reg_parser(TYPE_ASCII)
@reg_parser(TYPE_ASCII_INTERNED)
def _r_ascii(source, flag):
    res = source.read(_r_long(source)).decode('utf-8')
    if flag:
        REF.append(res)
    return res


@reg_parser(TYPE_INTERNED)
@reg_parser(TYPE_UNICODE)
def _r_unicode(source, flag):
    res = source.read(_r_long(source)).decode('utf-8')
    if flag:
        REF.append(res)
    return res


@reg_parser(TYPE_SET)
@reg_parser(TYPE_FROZENSET)
def _r_set(source, flag):
    if flag:
        idx = len(REF)
        REF.append(None)
    res = {_r_object(source) for i in range(_r_long(source))}
    if flag:
        REF[idx] = res
    return res


@reg_parser(TYPE_LIST)
def _r_list(source, flag):
    if flag:
        idx = len(REF)
        REF.append(None)
    res = [_r_object(source) for i in range(_r_long(source))]
    if flag:
        REF[idx] = res
    return res


@reg_parser(TYPE_DICT)
def _r_dict(source, flag):
    d = {}
    if flag:
        REF.append(d)
    while True:
        key = _r_object(source)
        if key is NULL_OBJECT:
            break
        value = _r_object(source)
        if value is NULL_OBJECT:
            break
        d[key] = value
    return d


@reg_parser(TYPE_REF)
def _r_ref(source, flag):
    return REF[_r_long(source)]


@reg_parser(TYPE_CODE)
def _r_code(source, flag):
    if flag:
        idx = len(REF)
        REF.append(None)
    data = {}
    data['co_argcount'] = _r_long(source)
    if sys.version_info[1] >= 8:
        data['co_posonlyargcount'] = _r_long(source)
    data['co_kwonlyargcount'] = _r_long(source)
    data['co_nlocals'] = _r_long(source)
    data['co_stacksize'] = _r_long(source)
    data['co_flags'] = _r_long(source)
    data['co_code'] = _r_object(source)
    data['co_consts'] = _r_object(source)
    data['co_names'] = _r_object(source)
    data['co_varnames'] = _r_object(source)
    data['co_freevars'] = _r_object(source)
    data['co_cellvars'] = _r_object(source)
    data['co_filename'] = _r_object(source)
    data['co_name'] = _r_object(source)
    data['co_firstlineno'] = _r_long(source)
    data['co_lnotab'] = _r_object(source)
    res = Code.from_dict(data)
    if flag:
        REF[idx] = res
    return res


def _r_object(source):
    type_ = source.read(1)[0]
    flag = False
    if type_ > 128:
        type_ -= 128
        flag = True
    if type_ not in TYPE_READERS:
        raise TypeError('unknown type: %s (%s)' % (type_, chr(type_)))
    return TYPE_READERS[type_](source, flag)


def load(fd):
    REF.clear()
    res = _r_object(fd)
    REF.clear()
    return res


def loads(source: bytes):
    if not isinstance(source, bytes):
        raise TypeError('expected bytes, not %s' % type(source))
    REF.clear()
    res = _r_object(BytesIO(source))
    REF.clear()
    return res
