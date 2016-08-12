from distutils.core import setup
import py2exe
setup(
    options = {"py2exe": {'bundle_files': 2, 'compressed': True}},
    console = ["updater.py"],
    zipfile = None,
)