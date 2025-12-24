# -*- coding: utf-8 -*-
import sys
from cx_Freeze import setup, Executable

includes = []
include_files = [
    ('/Users/[USERNAME]/novel_hacker/images','images'),
    ]
packages = ['os', 'sys', 'tkinter', 'unidic_lite', 'ipadic']
#excludes = ['pandas']
excludes = ['pandas', 'numpy']

build_exe_options = {
    'includes': includes,
    'include_files': include_files,
    'packages': packages,
    'excludes': excludes
}

setup(name='Write Hacker Free',
      version = '1.0.0',
      options={'build_exe': build_exe_options},
      executables=[Executable(script='app_free.py', base=None)])

