'''
	Utility methods file
'''
import urllib2
import json

class http:
    @staticmethod
    def get(url, headers = None):
        response = None
        if headers is None:
            response = urllib2.urlopen(url)
        else:
            request = urllib2.Request(url=url, headers=headers)
            response = urllib2.urlopen(request)    
        return response.read()

    @staticmethod
    def post(url, data, headers = None):
        request = urllib2.Request(url=url, data=data, headers=headers)
        response = urllib2.urlopen(request)
        return response.read()

    @staticmethod
    def put(url, data, headers = None):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(url=url, data=data, headers=headers)
        request.get_method = lambda: 'PUT'
        response = opener.open(request)
        return response.read()



habit_user_id = 'ce8624f4-3a59-407a-bb01-f83615dcbd2f'
habit_api_key = 'e02ad97a-09f5-4a4e-b9a7-39871d875700'
habit_base_url = 'https://habitrpg.com/api/v2'

class task:
    tasks = []
    @staticmethod
    def fetch_tasks():
        global habit_user_id, habit_api_key, habit_base_url
        headers = {
            'x-api-user': habit_user_id,
            'x-api-key': habit_api_key
        }
        response = http.get(habit_base_url + '/user/tasks', headers)
        task.tasks = json.loads(response)
        return task.tasks

    @staticmethod
    def get_by_name(name):
        lname = name.lower()
        for obj in task.tasks:
            if lname in obj['text'].lower() or lname in obj['notes'].lower():
                return { 'name': obj['id'], 'type': obj['type'], 'text': obj['text'] }


## Kick off the task fetch
task.fetch_tasks()