"""
Test runner script. Provided so that tests can be run with pvpython,
which doesn't support the "-m unittest" argument.
"""


import os
import unittest

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
    unittest.TextTestRunner(verbosity=2).run(suite)
