from cx_Freeze import setup, Executable
includefiles = ['cubapp-cd4ba-firebase-adminsdk-7xaqh-5688a100f9.json','logo.png']
executables = [Executable('main.py',
                          targetName='cubic.exe',
                          base="Win32GUI")]

options = {
    'build_exe': {
        'includes' : ['Login','pyrebase'],
        'include_msvcr': True,
        'include_files': includefiles
    }
}
setup(name='Cubic',
      version='0.0.1',
      description='pre_alpha_test',
      executables=executables,
      options=options
      )