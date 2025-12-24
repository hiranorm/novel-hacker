# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs
from PyInstaller.utils.hooks import copy_metadata

datas = [('/Users/hiran0rm/write_hacker/venv/lib/python3.11/site-packages/customtkinter', 'customtkinter/'), ('/Users/hiran0rm/write_hacker/images', 'images/'), ('/Users/hiran0rm/write_hacker/models', 'models/')]
binaries = []
datas += collect_data_files('unidic_lite')
datas += collect_data_files('ipadic')
datas += collect_data_files('torch')
datas += copy_metadata('torch')
datas += copy_metadata('tqdm')
datas += copy_metadata('regex')
datas += copy_metadata('requests')
datas += copy_metadata('packaging')
datas += copy_metadata('filelock')
datas += copy_metadata('sacremoses')
datas += copy_metadata('numpy')
datas += copy_metadata('tokenizers')
datas += copy_metadata('importlib_metadata')
binaries += collect_dynamic_libs('functorch')


block_cipher = None


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=['unidic_lite', 'ipadic', 'pytorch'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='app',
)
app = BUNDLE(
    coll,
    name='app.app',
    icon='icon.icns',
    bundle_identifier=None,
)
