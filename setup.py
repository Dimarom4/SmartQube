from cx_Freeze import setup, Executable
includefiles = ['new_cubsappkotlin-firebase-adminsdk-ovpmb-f533780929.json','logo.png','logo1.ico']
executables = [Executable('main.py',
                          targetName='cubic.exe',
                          base="Win32GUI",
                          icon='logo1.ico'
                          )]
zip_include_packages = ['PyQt5']
options = {
    'build_exe': {
        'includes' : ['Login'],
        'include_msvcr': True,
        'include_files': includefiles,
        'zip_include_packages': zip_include_packages
    }
}
setup(name='Cubic',
      version='0.0.3',
      description='pre_alpha_test',
      executables=executables,
      options=options
      )