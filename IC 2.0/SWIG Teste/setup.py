from distutils.core import setup, Extension

norms_and_vecs = Extension('_norms_and_vecs',
                           sources=['norms_and_vecs_wrap.cxx', 'norms_and_vecs.cpp'],
                           extra_compile_args=["-std=c++11"])

setup(name='norms_and_vecs',
      version='0.1',
      author="José Roman",
      description="""Teste para exportar função de C++ para Python""",
      ext_modules=[norms_and_vecs],
      py_modules=["norms_and_vecs"])