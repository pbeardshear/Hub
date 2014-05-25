'''
	Providers implement the following interface:
		- polling_interval [int] = amount of time (in minutes) between polling
		- fetch_data [function] = function which grabs data from an API and returns in to the callback
'''
from utils import http, task
from datetime import datetime, timedelta

# Private state
_API_KEY = '45aafe36aa0161da3b2628ac00ac83a626c9aa47'
_BASE_URL = 'https://api.github.com'

# Amount of time (in minutes) between polling
polling_interval = 15

time_offset = timedelta(minutes=-polling_interval)


# List of tasks that this provider listens on
task_list = { 'selenium': task.get_by_name('selenium') }




# Grab latest commit data from GitHub
def fetch_data():
    global _BASE_URL, _API_KEY
    since = datetime.now() + time_offset
    url = _BASE_URL + '/repos/pbeardshear/hub/commits'
    query = '?author={0}&since={1}&access_token={2}'.format('pbeardshear', since.isoformat(), _API_KEY)
    commits = http.get(url)
    return [task_list['selenium']]
