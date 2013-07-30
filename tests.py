import unittest
import sys
import json

from gaikaiparser import parse


jobs = parse()


class TestGaikaiParser(unittest.TestCase):

    def test_consistency(self):
        self.assertGreaterEqual(len(jobs), 1)
        for job in jobs:
            for key, value in job.items():
                self.assert_(value)

    def test_serialization(self):
        a = json.dumps(jobs)
        b = json.loads(a)
        self.assertEqual(b, jobs)


def test_main():
    tests = []
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestGaikaiParser))
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    if not test_main():
        sys.exit(1)
