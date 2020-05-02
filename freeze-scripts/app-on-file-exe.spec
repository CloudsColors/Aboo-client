# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['app.py'],
             pathex=['C:\\Users\\Andreas\\.virtualenvs\\Aboo-client-glzfX4Km', 'C:\\Users\\Andreas\\Desktop\\Programmering\\Python\\aboo-client'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

a.datas += [("Settings/settings.json", "C:\\Users\\Andreas\\Desktop\\Programmering\\Python\\aboo-client\\Settings\\settings.json", "DATA"),
            ("Statics/logo.png", "C:\\Users\\Andreas\\Desktop\\Programmering\\Python\\aboo-client\\Statics\\logo.png", "DATA"),
            ("Statics/icon-large.png", "C:\\Users\\Andreas\\Desktop\\Programmering\\Python\\aboo-client\\Statics\\icon-large.png", "DATA")]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Aboo-client',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='C:\\Users\\Andreas\\Desktop\\Programmering\\Python\\aboo-client\\Statics\\icon-large.ico')
