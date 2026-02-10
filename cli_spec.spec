# -*- mode: python ; coding: utf-8 -*-

import os
import flet
import flet_desktop

# Get paths for manual inclusion
flet_path = os.path.dirname(flet.__file__)
flet_desktop_path = os.path.dirname(flet_desktop.__file__)

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('lib', 'lib'),
        ('models', 'models'),  # Include models directory
        (flet_path, 'flet'),   # Include flet package
        (flet_desktop_path, 'flet_desktop'), # Include flet_desktop package (essential for finding the executable)
        # ('poppler/bin', 'poppler/bin'), # Poppler binaries if present - user instructions needed
    ],
    hiddenimports=[
        'flet',
        'easyocr',
        'iopaint',
        'iopaint.model',
        'iopaint.model.lama',
        'iopaint.model_manager',
        'engineio.async_drivers.threading', # Common hidden import for socketio/flet
        'sklearn.utils._cython_blas', 
        'sklearn.neighbors.typedefs',
        'sklearn.neighbors.quad_tree',
        'sklearn.tree._utils', 
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='NotebookLM2PPTX',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Hide console for production
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='NotebookLM2PPTX',
)
