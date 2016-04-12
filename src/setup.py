from distutils.core import setup
import py2exe
import glob

setup(console=['index.py'],
      data_files=[("html", glob.glob('.//html//*.html')),
                  ('static', []),
                  ('static//css', [r"./static/css/style.css"]),
                  (r'static/css/images', glob.glob('./static/css/images/*.gif')),
                  ('.', [r'I:\Anaconda2\Library\bin\libiomp5md.dll',
                         r'I:\Anaconda2\Library\bin\mkl_p4.dll',
                         r'I:\Anaconda2\Library\bin\mkl_avx2.dll',
                         ])],
      options={
          "py2exe": {
              "packages": ["web"],
              "includes": ["web",
                           "scipy.special._ufuncs_cxx",
                           "scipy.sparse.csgraph._validation",
                           "scipy.linalg.cython_blas",
                           "scipy.linalg.cython_lapack"]
          }
      }
      )
