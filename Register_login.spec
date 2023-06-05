# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
   ['Main_kivy.py','webcam_demo.py','get_standard_data.py','dict_base.py','dataloader.py','dataloader_webcam.py',
'demo.py','dict_base.py','fn.py','opt.py','online_demo.py','pPose_nms.py','Register_login.py','video_play.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['kivy._2.0.0'],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Register_login',
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
