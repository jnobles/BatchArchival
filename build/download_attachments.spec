# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['../src/attachment_downloader/download_attachments.py'],
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ScanDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
