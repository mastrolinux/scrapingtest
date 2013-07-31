import unittest
import sys
import json

import gaikaiparser
import webapp



class TestGaikaiParser(unittest.TestCase):
    def setUp(self):
        global jobs
        jobs = gaikaiparser.parse()

    def test_consistency(self):
        self.assertGreaterEqual(len(jobs), 1)
        for job in jobs:
            for key, value in job.items():
                self.assert_(value)

    def test_serialization(self):
        a = json.dumps(jobs)
        b = json.loads(a)
        self.assertEqual(b, jobs)


def patched_wget(url):
    """
    Overwriting the wget function on gaikaiparser in order to retrieve a
    consistent html page for tests
    """
    with open('gaikai.html', 'r') as gaikai:
        return gaikai.read()


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = webapp.app.test_client()
        self.original_wget = gaikaiparser.wget
        gaikaiparser.wget = patched_wget 
        webapp.jobs = gaikaiparser.parse()

    # not really needed, just a best practice
    def tearDown(self):
        gaikaiparser.wget = self.original_wget

    def test_tasks(self):
        """
        Should retrieve a full list of jobs
        """
        rv = self.app.get('/jobs')
        data = json.loads(rv.data)
        self.assertTrue('jobs' in data.keys())
         # We know it's 73, we are reading the static gaikai.html
        self.assertEqual(73, len(data['jobs']))
        self.assertTrue('skills' in data['jobs'][0])
        self.assertTrue('responsibilities' in data['jobs'][0])
        self.assertTrue('requirements' in data['jobs'][0])
        self.assertTrue('title' in data['jobs'][0])
        self.assertEqual('Senior Solution Architect', data['jobs'][0]['title'])

    def test_specific_job(self):
        """
        Should retrieve only jobs matching our query
        """
        rv = self.app.get('/jobs/manager')
        data = json.loads(rv.data)
        self.assertTrue('matched_jobs' in data.keys())
        self.assertEqual(17, len(data['matched_jobs']))  # We know it's 17, we are reading gaikai.html
        for job in data['matched_jobs']:
            self.assertTrue('manager' in job['title'].lower())  # We need a case insensitive matching

    def test_update(self):
        """
        Should update the global jobs list
        """
        webapp.jobs = {}  # Jobs is empty
        rv = self.app.get('/jobs')
        data = json.loads(rv.data)
        self.assertEqual(0, len(data['jobs']))

        rv = self.app.get('/update')  # We update jobs
        rv = self.app.get('/jobs')
        data = json.loads(rv.data)
        self.assertNotEqual(0, len(data['jobs']))


def test_main():
    tests = []
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestGaikaiParser))
    test_suite.addTest(unittest.makeSuite(TestWebApp))
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    if not test_main():
        sys.exit(1)
