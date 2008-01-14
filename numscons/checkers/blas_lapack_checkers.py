#! /usr/bin/env python
# Last Change: Tue Dec 04 03:00 PM 2007 J

# Module for custom, common checkers for numpy (and scipy)
import sys
import os.path
from copy import deepcopy
from distutils.util import get_platform

from numscons.core.libinfo import get_config_from_section, get_config
from numscons.testcode_snippets import cblas_sgemm as cblas_src, \
        c_sgemm as sunperf_src, lapack_sgesv, blas_sgemm, c_sgemm2, \
        clapack_sgesv as clapack_src
from numscons.fortran_scons import CheckF77Mangling, CheckF77Clib
from numscons.core.utils import rsplit
from numscons.core.extension_scons import built_with_mstools, built_with_mingw

from configuration import add_info, BuildOpts, ConfigRes
from perflib import CONFIG, checker
from support import check_include_and_run

def _check_perflib(perflibs, libname, context, autoadd, check_version):
    """perflibs should be a list of perflib to check."""
    def _check(func, name):
        st, res = func(context, autoadd, check_version)
        if st:
            cfgopts = res.cfgopts.cblas_config()
            st = check_include_and_run(context, 'CBLAS (%s)' % name, 
                                       cfgopts, [], cblas_src, autoadd)
            if st:
                add_info(env, libname, res)
            return st
    for p in perflibs:
        st = _check(checker(p), CONFIG[p].name)
        if st:
            return st

def CheckCBLAS(context, autoadd = 1, check_version = 0):
    """This checker tries to find optimized library for cblas."""
    libname = 'cblas'
    env = context.env

    def check(perflibs):
        """perflibs should be a list of perflib to check."""
        def _check(func, name):
            st, res = func(context, autoadd, check_version)
            if st:
                cfgopts = res.cfgopts.cblas_config()
                st = check_include_and_run(context, 'CBLAS (%s)' % name, 
                                           cfgopts, [], cblas_src, autoadd)
                if st:
                    add_info(env, libname, res)
                return st
        for p in perflibs:
            st = _check(checker(p), CONFIG[p].name)
            if st:
                return st

    # If section cblas is in site.cfg, use those options. Otherwise, use default
    section = "cblas"
    siteconfig, cfgfiles = get_config()
    (cpppath, libs, libpath), found = get_config_from_section(siteconfig, section)
    if found:
        # XXX: deepcopy rpath ?
        cfg = BuildOpts(cpppath = cpppath, libs = libs, libpath = libpath,
                         rpath = libpath)
        st = check_include_and_run(context, 'CBLAS (from site.cfg) ', cfg,
                                  [], cblas_src, autoadd)
        if st:
            add_info(env, libname, ConfigRes('Generic CBLAS', cfg, found))
            return st
    else:
        if sys.platform == 'darwin':
            st = check(('Accelerate', 'vecLib'))
            if st:
                return st
        else:
            st = check(('MKL', 'ATLAS', 'Sunperf'))
            if st:
                return st

    add_info(env, libname, None)
    return 0

def CheckF77BLAS(context, autoadd = 1, check_version = 0):
    """This checker tries to find optimized library for blas (fortran F77)."""
    libname = 'blas'
    env = context.env

    # Get Fortran things we need
    if not env.has_key('F77_NAME_MANGLER'):
        if not CheckF77Mangling(context):
            add_info(env, libname, None)
            return 0

    if not env.has_key('F77_LDFLAGS'):
        if not CheckF77Clib(context):
            add_info(env, 'blas', None)
            return 0

    func_name = env['F77_NAME_MANGLER']('sgemm')
    test_src = c_sgemm2 % {'func' : func_name}

    def check(perflibs):
        def _check(func, name):
            st, res = func(context, autoadd, check_version)
            if st:
                cfgopts = res.cfgopts.blas_config()
                st = check_include_and_run(context, 'BLAS (%s)' % name, cfgopts,
                        [], test_src, autoadd)
                if st:
                    add_info(env, libname, res)
                return st
        for p in perflibs:
            st = _check(checker(p), CONFIG[p].name)
            if st:
                return st

    # If section blas is in site.cfg, use those options. Otherwise, use default
    section = "blas"
    siteconfig, cfgfiles = get_config()
    (cpppath, libs, libpath), found = get_config_from_section(siteconfig, section)
    if found:
        cfg = BuildOpts(cpppath = cpppath, libs = libs, libpath = libpath,
                         rpath = libpath)
        st = check_include_and_run(context, 'BLAS (from site.cfg) ', cfg,
                                  [], test_src, autoadd)
        if st:
            add_info(env, libname, ConfigRes('Generic BLAS', cfg, found))
            return st
    else:
        if sys.platform == 'darwin':
            st = check(('Accelerate', 'vecLib'))
            if st:
                return st
        else:
            st = check(('MKL', 'ATLAS', 'Sunperf'))
            if st:
                return st

    def check_generic_blas():
        name = 'Generic'
        cfg = CONFIG['GenericBlas']
        res = ConfigRes(name, cfg.defopts, 0)
        st = check_include_and_run(context, 'BLAS (%s)' % name, res.cfgopts,
                                   [], test_src, autoadd)
        if st:
            add_info(env, libname, res)
        return st

    # Check generic blas last
    st = check_generic_blas()
    if st:
        return st

    add_info(env, libname, None)
    return 0

def CheckF77LAPACK(context, autoadd = 1, check_version = 0):
    """This checker tries to find optimized library for F77 lapack.

    This test is pretty strong: it first detects an optimized library, and then
    tests that a simple (C) program can be run using this (F77) lib.
    
    It looks for the following libs:
        - Mac OS X: Accelerate, and then vecLib.
        - Others: MKL, then ATLAS."""
    libname = 'lapack'
    env = context.env

    if not env.has_key('F77_NAME_MANGLER'):
        if not CheckF77Mangling(context):
            add_info(env, 'lapack', None)
            return 0
    
    if not env.has_key('F77_LDFLAGS'):
        if not CheckF77Clib(context):
            add_info(env, 'lapack', None)
            return 0
    
    # Get the mangled name of our test function
    sgesv_string = env['F77_NAME_MANGLER']('sgesv')
    test_src = lapack_sgesv % sgesv_string

    def check(perflibs):
        def _check(func, name):
            # func is the perflib checker, name the printed name for the check,
            # and suplibs a list of libraries to link in addition.
            st, res = func(context, autoadd, check_version)
            if st:
                cfgopts = res.cfgopts.lapack_config()
                st = check_include_and_run(context, 'LAPACK (%s)' % name, cfgopts,
                                           [], test_src, autoadd)
                if st:
                    add_info(env, libname, res)
                return st
        for p in perflibs:
            st = _check(checker(p), CONFIG[p].name)
            if st:
                return st

    # If section lapack is in site.cfg, use those options. Otherwise, use default
    section = "lapack"
    siteconfig, cfgfiles = get_config()
    (cpppath, libs, libpath), found = get_config_from_section(siteconfig, section)
    if found:
        # XXX: handle def library names correctly
        if len(libs) == 1 and len(libs[0]) == 0:
            libs = ['lapack', 'blas']
        cfg = BuildOpts(cpppath = cpppath, libs = libs, libpath = libpath,
                         rpath = deepcopy(libpath))

        # fortrancfg is used to merge info from fortran checks and site.cfg
        fortrancfg = deepcopy(cfg)
        fortrancfg['linkflags'].extend(env['F77_LDFLAGS'])

        st = check_include_and_run(context, 'LAPACK (from site.cfg) ', fortrancfg,
                                  [], test_src, autoadd)
        if st:
            add_info(env, libname, ConfigRes('Generic LAPACK', cfg, found))
            return st
    else:
        if sys.platform == 'darwin':
            st = check(('Accelerate', 'vecLib'))
            if st:
                return st
        else:
            st = check(('MKL', 'ATLAS', 'Sunperf'))
            if st:
                return st

    def check_generic_lapack():
        name = 'Generic'
        cfg = CONFIG['GenericLapack']
        res = ConfigRes(name, cfg.defopts, 0)
        st = check_include_and_run(context, 'LAPACK (%s)' % name, res.cfgopts,
                                   [], test_src, autoadd)
        if st:
            add_info(env, libname, res)
        return st

    # Check generic blas last
    st = check_generic_lapack()
    if st:
        return st

    add_info(env, libname, None)
    return 0

def CheckCLAPACK(context, autoadd = 1, check_version = 0):
    """This checker tries to find optimized library for lapack.

    This test is pretty strong: it first detects an optimized library, and then
    tests that a simple cblas program can be run using this lib.
    
    It looks for the following libs:
        - Mac OS X: Accelerate, and then vecLib.
        - Others: MKL, then ATLAS."""
    libname = 'clapack'
    env = context.env

    def check(perflibs):
        def _check(func, name):
            st, res = func(context, autoadd, check_version)
            if st:
                cfgopts = res.cfgopts.clapack_config()
                st = check_include_and_run(context, 'CLAPACK (%s)' % name, 
                                           res.cfgopts, [], clapack_src, autoadd)
                if st:
                    add_info(env, libname, res)
                return st
        for p in perflibs:
            st = _check(checker(p), CONFIG[p].name)
            if st:
                return st

    # If section lapack is in site.cfg, use those options. Otherwise, use default
    section = "clapack"
    siteconfig, cfgfiles = get_config()
    (cpppath, libs, libpath), found = get_config_from_section(siteconfig, section)
    if found:
        # XXX: handle section
        pass
    else:
        if sys.platform == 'darwin':
            pass
        else:
            # Check ATLAS
            st = check(('ATLAS'),)
            if st:
                return st

    add_info(env, libname, None)
    return 0
