# -*- mode: python -*-

block_cipher = None

a = Analysis(['q1a2b.py'],
             pathex=[],
             binaries=[],
             datas=[('q1a2b.ui', '.'),('images/q1a2b.png', 'images/')],
             hiddenimports=['pyttsx3.drivers', 'pyttsx3.drivers.dummy',
             'pyttsx3.drivers.espeak', 'pyttsx3.drivers.nsss', 
             'pyttsx3.drivers.sapi5'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='q1a2b',
          debug=False,
          strip=False,
          upx=False,
          console=False, 
          icon='images/q1a2b.ico',
          version='q1a2b.ver')
