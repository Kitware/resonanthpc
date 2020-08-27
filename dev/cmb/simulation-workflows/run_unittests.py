"""
Test runner script. Provided so that tests can be run with pvpython,
which doesn't support the "-m unittest" argument.
"""


import os
import sys
import unittest

source_path = os.path.abspath(os.path.dirname(__file__))
writer_path = os.path.join(source_path, "ats", "internal")
sys.path.insert(0, writer_path)

if __name__ == "__main__":
    loader = unittest.TestLoader()

    # Next 3 lines dont work and I wish I knew why...
    # import tests
    # suite = unittest.TestSuite()
    # suite.addTests(loader.loadTestsFromModule(tests))

    # So instead, use discover
    source_path = os.path.abspath(os.path.dirname(__file__))
    test_path = os.path.join(source_path, "tests")
    suite = loader.discover(start_dir=test_path, pattern="test*.py")
    # print(suite)

    # Because pvpython hijacks command line options, we'll
    # hard-code verbosity to level 2 for now
    run = unittest.TextTestRunner(verbosity=2).run(suite)
    exit(len(run.failures) > 0 or len(run.errors) > 0)
