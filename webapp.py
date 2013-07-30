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
    return Response(json.dumps(dict(jobs=jobs)),  mimetype="application/json")

@app.route('/jobs/<string:job_name>', methods=['GET'])
def get_specific_job(job_name):
    ret = []
    for job in jobs:
        if re.search(job_name, job['title'], re.IGNORECASE):
            ret.append(job)
    return Response(json.dumps(dict(matched_jobs=ret)), mimetype="application/json")

@app.route('/update', methods = ['GET'])
def update_json():
    global jobs
    jobs = parse()
    return "Status updated"

if __name__ == '__main__':
    app.run(debug=False)
