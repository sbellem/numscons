#! /usr/bin/env python
# Last Change: Sun Jan 06 09:00 PM 2008 J

"""This module defines various utilities used throughout the scons support
library."""

import os
import re

from copy import deepcopy

_START_WITH_MINUS = re.compile('^\s*-')

def popen_wrapper(cmd, merge = False):
    """This works like popen, but it returns both the status and the output.

    If merge is True, then output contains both stdout and stderr. 
    
    Returns: (st, out), where st is an integer (the return status of the
    subprocess, and out the string of the output).
    
    NOTE:
        - it tries to be robust to find non existing command. For example, is
          cmd starts with a minus, a nonzero status is returned, and no junk is
          displayed on the interpreter stdout."""
    if _START_WITH_MINUS.match(cmd):
        return 1, ''
    if merge:
        # XXX: I have a bad feeling about this. Does it really work reliably on
        # all supported platforms ?
        cmd += ' 2>& 1 '
    output = os.popen(cmd)
    out = output.read()
    st = output.close()
    if st:
        status = st
    else:
        status = 0

    return status, out

def pkg_to_path(pkg_name):
    """Given a python package name, returns its path from the root.

    Example: numpy.core becomes numpy/core."""
    return os.sep.join(pkg_name.split('.'))

def get_empty(dic, key):
    """Assuming dic is a dictionary with lists as values, returns an empty
    list if key is not found, or a (deep) copy of the existing value if it
    does."""
    try:
        return deepcopy(dic[key])
    except KeyError, e:
        return []

class NonDefaultKeyError(KeyError):
    pass

class DefaultDict(dict):
    """Structure similar to a dictionary, with a restricted set of possible
    keys."""
    def __init__(self, avkeys, default = None):
        dict.__init__(self, [(i, default) for i in avkeys])

    def __setitem__(self, key, val):
        if not self.has_key(key):
            raise NonDefaultKeyError(key)
        dict.__setitem__(self, key, val)
        
def rsplit(s, sep, maxsplit = -1):
    """Equivalent of rsplit, but works on 2.3."""
    try:
        return s.rsplit(sep, maxsplit)
    except AttributeError:
        return _rsplit(s, sep, maxsplit)

def _rsplit(s, sep, maxsplit):
    """Equivalent of rsplit, but works on 2.3."""
    l = s.split(sep)
    if len(l) < 2 or maxsplit == 0:
        return [s]
    elif maxsplit < 0:
        return l[-len(l):]
    else:
        st = sep.join(l[0:-maxsplit])
        return [st] + l[-maxsplit:]

class partial:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs

        return self.fun(*(self.pending + args), **kw)

# Copied from scons code...
import types
from UserString import UserString
# Don't "from types import ..." these because we need to get at the
# types module later to look for UnicodeType.
StringType      = types.StringType
TupleType       = types.TupleType
if hasattr(types, 'UnicodeType'):
    UnicodeType = types.UnicodeType
    def isstring(obj):
        t = type(obj)
        return t is StringType \
            or t is UnicodeType \
            or (t is InstanceType and isinstance(obj, UserString))
else:
    def isstring(obj):
        t = type(obj)
        return t is StringType \
            or (t is InstanceType and isinstance(obj, UserString))
