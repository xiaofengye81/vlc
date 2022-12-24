#!/usr/bin/env python3
import os
import argparse
import shlex

# Argument parsing
parser = argparse.ArgumentParser(
    description="Generate a meson crossfile based on environment variables")
parser.add_argument('file', type=argparse.FileType('w', encoding='UTF-8'),
    help="output file")
args = parser.parse_args()

# Helper to add env variable value to crossfile
def _add_environ_val(meson_key, env_key):
    env_value = os.environ.get(env_key)
    if env_value != None:
        args.file.write(f"{meson_key} = '{env_value}'\n")

# Helper to add env variable array to crossfile
def _add_environ_arr(meson_key, env_key):
    env_array = os.environ.get(env_key)
    if env_array != None:
        env_values = shlex.split(env_array)
        arr_string = ', '.join(f"'{item}'" for item in env_values)
        args.file.write(f"{meson_key} = [{arr_string}]\n")

# Generate meson crossfile
args.file.write("# Automatically generated by contrib makefile\n")

# Binaries section
args.file.write("\n[binaries]\n")
_add_environ_val('c', 'CC')
_add_environ_val('cpp', 'CXX')
if os.environ.get('HOST_SYSTEM') == 'darwin':
    _add_environ_val('objc', 'OBJC')
    _add_environ_val('objcpp', 'OBJCXX')
_add_environ_val('ar', 'AR')
_add_environ_val('strip', 'STRIP')
_add_environ_val('pkgconfig', 'PKG_CONFIG')
_add_environ_val('windres', 'WINDRES')

# Properties section
args.file.write("\n[properties]\n")
args.file.write("needs_exe_wrapper = true\n")
_add_environ_val('pkg_config_libdir', 'PKG_CONFIG_LIBDIR')

# Host machine section
args.file.write("\n[host_machine]\n")
_add_environ_val('system', 'HOST_SYSTEM')
_add_environ_val('cpu_family', 'HOST_ARCH')
args.file.write("endian = 'little'\n")

# Get first part of triplet
cpu = os.environ.get('HOST', '').split('-')[0]
args.file.write(f"cpu = '{cpu}'\n")

# CMake section
args.file.write("\n[cmake]\n")
_add_environ_val('CMAKE_C_COMPILER', 'CC')
_add_environ_val('CMAKE_CXX_COMPILER', 'CXX')
_add_environ_val('CMAKE_SYSTEM_NAME', 'CMAKE_SYSTEM_NAME')
_add_environ_val('CMAKE_SYSTEM_PROCESSOR', 'ARCH')

