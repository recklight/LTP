import sys
from distutils.core import setup
from Cython.Build import cythonize

compile_files = sys.argv[3:]
del sys.argv[3:]
print(f"\033[1;36m{compile_files}\033[0m")
print("\033[5;37;41m======== Compiling ========\033[0m")

setup(ext_modules=cythonize(compile_files))

print("\033[5;37;41m ======== Completed ======== \033[0m")
