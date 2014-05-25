from bottle import route, run, template
from threading import Thread, Event
from providers import *
from providers import module_names
from utils import http
import json

# from celery import Celery

api_calls = 0
result = None
interval = 15
modules = []

## Celery crap
# app = Celery('hello', broker='amqp://guest@localhost//')
# @app.task
# def hello():
#     return 'hello world'


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/api')
def api():
    global api_calls
    return template('<p>Made {{calls}} so far!', calls=api_calls)

## Iterate each of the modules, and add them to the queue
for name in module_names:
    provider = globals()[name]
    provider.tick = provider.polling_interval / interval
    modules.append(provider)


## Start teh timer so we can pull from the API
class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global api_calls, modules, interval        
        while not self.stopped.wait(interval):
            print 'Running thread...'
            api_calls += 1
            # Read each provider
            tasks = []
            for provider in modules:
                provider.tick -= 1;
                if provider.tick is 0:
                    tasks += provider.fetch_data()
                    provider.tick = provider.polling_interval / interval
            print 'Tasks:'
            print tasks
            push_updates(tasks)


stop_flag = Event()
thread = MyThread(stop_flag)
# Setting the thread as a daemon means it will end if the parent process ends
thread.daemon = True
thread.start()



'''
    Layout:
        API providers (each defines a poll interval + callback)
        push provider output => HabitRPG
            define consumers for the provider data (function composition)
        store historic data in database/flat file for statistics
        add statistics page
        add GUI for adding provider => consumer relationship
'''

'''
    HabitRPG API requests
'''
habit_user_id = 'ce8624f4-3a59-407a-bb01-f83615dcbd2f'
habit_api_key = 'e02ad97a-09f5-4a4e-b9a7-39871d875700'
habit_base_url = 'https://habitrpg.com/api/v2'

def push_updates(tasks):
    global habit_base_url, habit_user_id, habit_api_key
    print '\nPushing updates...'
    for task in tasks:
        url = habit_base_url + '/user/tasks/' + task['name']
        headers = {
            'x-api-user': habit_user_id,
            'x-api-key': habit_api_key,
            'Content-Type': 'application/json'
        }
        data = { }

        if task['type'] == 'habit':
            url += '/up'
        elif task['type'] == 'daily':
            data['completed'] = 'true'
        
        print 'Data:'
        print url
        print data
        response = http.put(url, json.dumps(data), headers)


## Start the bottle server
run(host='localhost', port=8080)

