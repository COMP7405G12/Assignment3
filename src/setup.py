from distutils.core import setup
import py2exe
import glob

setup(console=['index.py'],
      data_files=[(".", glob.glob('.//*.html'))],
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
