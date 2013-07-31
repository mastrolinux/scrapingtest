#!/usr/bin/env python

import re
import json

from flask import Flask, Response
from gaikaiparser import parse


DEBUG = True
app = Flask(__name__)
jobs = parse()  # load jobs into memory


@app.route('/jobs', methods=['GET'])
def get_tasks():
    """
    Returns a json with every job listed
    http://localohost:5000/jobs
    """
    return Response(json.dumps(dict(jobs=jobs)),  mimetype="application/json")

@app.route('/jobs/<string:job_name>', methods=['GET'])
def get_specific_job(job_name):
    """
    Returns a json looking for jobs matching a given set of words in the title
    http://localohost:5000/jobs/IT%20Manager
    (the search is case insensitive)
    """
    ret = []
    for job in jobs:
        if re.search(job_name, job['title'], re.IGNORECASE):
            ret.append(job)
    return Response(json.dumps(dict(matched_jobs=ret)), mimetype="application/json")

@app.route('/update', methods = ['GET'])
def update_json():
    """
    Fetch the content of the webiste and stores it in ram as a new copy
    """
    # In general is bad to have global vars, but in this case allow us to
    # avoid saving on file system for a superfast search (everything in ram)
    global jobs
    jobs = parse()
    return "Status updated"

if __name__ == '__main__':
    app.run(debug=False)
