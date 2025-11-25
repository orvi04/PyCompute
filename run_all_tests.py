import unittest

if __name__ == "__main__":
    loader = unittest.TestLoader()
    
    start_dir = '.'
    suite = loader.discover(start_dir, pattern='*_test.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)