from cx_Freeze import setup, Executable
includefiles = ['new_cubsappkotlin-firebase-adminsdk-ovpmb-f533780929.json','logo.png','logo1.ico']
executables = [Executable('main.py',
                          targetName='cubic.exe',
                          base="Win32GUI",
                          icon='logo1.ico',
                          shortcutName='Cubic',
                          shortcutDir='DesktopFolder'
                          )]
zip_include_packages = ['PyQt5','numpy']
version='0.0.4'
options = {
    'build_exe': {
        'includes' : ['Login'],
        'include_msvcr': True,
        'include_files': includefiles,
        'zip_include_packages': zip_include_packages,
        "build_exe": "Smart cube."+version
    }
}
setup(name='Cubic',
      version=version,
      description='Пре-альфа тестирование',
      executables=executables,
      options=options
      )