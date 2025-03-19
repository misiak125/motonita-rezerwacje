# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

tkinter_data = collect_data_files('tkinter')

a = Analysis(
    ['main.py'],
    pathex=['.' , './src' , './src/utils/' , './src/views/'],
    binaries=[],
    datas=[
        ('src/static/*', 'static')
        (r'C:\Python311\tcl\*', 'tcl'),
        (r'C:\Python311\Lib\lib-tk\*', 'lib-tk'),
        ('src/static/splash.png', '.')
    ] + tkinter_data,
    hiddenimports=[
        'babel.numbers'
        'sqlalchemy.dialects.sqlite',
        'sqlalchemy.ext.baked',
        'sqlalchemy.ext.declarative',
        'PIL._tkinter_finder',
        'PIL.Image', 
        'PIL.ImageTk',
        'PIL._tkinter_finder',
        'reportlab.pdfgen',
        'reportlab.lib',
        'reportlab.rl_settings',
        'dateutil.tz',
        'dateutil.parser',
        'tkinter.filedialog',
        'tkinter.font',
        'tkcalendar',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='motonita_rezerwacje',
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
    icon='icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='motonita_rezerwacje',
)
