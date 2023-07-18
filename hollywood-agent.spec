# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['hollywood_agent/main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('config', 'config')],
             hiddenimports=[
                'cement', 
                'cement.ext.ext_dummy', 
                'cement.ext.ext_smtp', 
                'cement.ext.ext_plugin', 
                'cement.ext.ext_configparser',
                'cement.ext.ext_logging',
                'hollywood_agent.controllers',
                'hollywood_agent.flask_server',
                'hollywood_agent.periodic_task',
                'hollywood_agent.utils',
            ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='hollywood-agent',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
