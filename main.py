from bottle import route, run, template
from threading import Thread, Event
# from celery import Celery

api_calls = 0
result = None

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


## Start teh timer so we can pull from the API
class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global stop_flag, api_calls
        while not self.stopped.wait(0.5):
            api_calls += 1
            # stop_flag.set()


stop_flag = Event()
thread = MyThread(stop_flag)
thread.daemon = True
thread.start()


## Start the bottle server
run(host='localhost', port=8080)


'''
    Layout:
        API providers (each defines a poll interval + callback)
        push provider output => HabitRPG
            define consumers for the provider data (function composition)
        store historic data in database/flat file for statistics
        add statistics page
        add GUI for adding provider => consumer relationship
'''