# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = [('/Users/hiran0rm/write_hacker/venv/lib/python3.11/site-packages/customtkinter', 'customtkinter/'), ('/Users/hiran0rm/write_hacker/images', 'images/')]
datas += collect_data_files('unidic_lite')
datas += collect_data_files('ipadic')
datas += copy_metadata('tqdm')
datas += copy_metadata('regex')
datas += copy_metadata('requests')
datas += copy_metadata('packaging')
datas += copy_metadata('filelock')
datas += copy_metadata('numpy')
datas += copy_metadata('importlib_metadata')


block_cipher = None


a = Analysis(
    ['app_free.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=['unidic_lite', 'ipadic'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app_free',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.icns'],
)
app = BUNDLE(
    exe,
    name='app_free.app',
    icon='icon.icns',
    bundle_identifier=None,
)
