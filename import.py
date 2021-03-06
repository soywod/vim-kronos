#!/usr/bin/env python

import sys
import json
from datetime import datetime

if len(sys.argv) != 3:
    raise Exception('args missing or invalid')

if not sys.argv[1]:
    raise Exception('provider missing')

if not sys.argv[2]:
    raise Exception('file missing')

if sys.argv[1] == 'taskwarrior':
    tasks = {}
    database_in = open(sys.argv[2], 'r')
    database_out = open('.database', 'w')

    def parse_due(raw_due):
        return raw_due if not raw_due else datetime.strptime(raw_due, '%Y%m%dT%H%M%SZ').strftime('%s')

    def parse_status(status):
        return 1 if status == 'completed' or status == 'deleted' else 0

    for line in database_in.read().split('\n'):
        try:
            task = json.loads(line)

            if 'tags' not in task.keys():
                task['tags'] = []

            if 'due' not in task.keys():
                task['due'] = ''

            tasks[task['uuid']] = {
                'desc': task['description'],
                'tags': task['tags'],
                'due': parse_due(task['due']),
                'index': parse_due(task['entry']),
                'start': [],
                'stop': [],
                'active': 0,
                'done': parse_status(task['status']),
            }

        except:
            continue

    database_out.write('[]\n0\n')

    for index, task in enumerate(tasks.values()):
        task['id'] = index + 1
        task['index'] = -int(str(task['id']) + task['index'])
        database_out.write(json.dumps(task) + '\n')

    database_in.close()
    database_out.close()
