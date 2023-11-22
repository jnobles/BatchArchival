# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['../src/archival_assistant/controller.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# for some reason pywintypes is included in both the root and pywin32_system32
# folders.  This causes failed imports and crash.  The root dll must be manually
# excluded
a.binaries = a.binaries - TOC([
    ('pywintypes310.dll', None, None),
    ('pythoncom310.dll', None, None)
])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
splash = Splash(
    'splash.png',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=(10, 55),
    text_size=10,
    minify_script=True,
    always_on_top=True,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='BatchArchivalAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
