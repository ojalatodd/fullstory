'''
This app displays a list of github issues that have been raised
by users who also have captured Fullstory sessions!

November 7, 2018
'''


from flask import Flask
from flask import render_template
from flask import request

import json
import logging
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

logger = logging.getLogger()

GITHUB_URL = "https://api.github.com/repos/ojalatodd/fullstory/issues"
FULLSTORY_URL = "https://www.fullstory.com/api/v1/sessions"

def get_url(url):
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return False

    try:
        return response.json()
    except Exception as err:
        logger.exception(err)
        logger.error(
            'Error parsing JSON response from "{url}". Dumping response content: {raw}'.format(
                url=url,
                raw=response.text
            )
        )
        return None

        
    
@app.route("/")
def test():

    alert="Hello!"

    return "The Fullstory app is online. Please go to endpoint /webapp"


@app.route("/webapp", methods=['POST', 'GET'])
def index():

    #Display all the issues associated with the Web Calculate app

    github_data = get_url(url=GITHUB_URL)
    #Get the parts of the data that we want:
    
    nu_issues = len(github_data)

    # Create a session with auth
    s = requests.Session()
    s.headers.update({'Authorization': 'Basic Rzc5NEI6UnpjNU5FSTZRVVZDYjJaSllUWmFlVlEwT0hwR2JYZFdhVWhPTm5aNmRtUkdRMEpGYkRSRllXRnBVeXM0V1M4NVRUMD0='})
    issues = []  # Initialize the list that holds all the issues

    for i in github_data:

        # To-do: Get the user's email from github with the user endpoint,
        # then use that to pull the Fullstory session data

        # Get the Fullstory session data for this user based on email.
        sess_data = s.get(FULLSTORY_URL, params={'email':'todd@toddojala.com'}).json()
        
        # Get the link to the session
        first_session = sess_data.pop() # Only get first session in this beta version
        sess_link = first_session['FsUrl']
        print(sess_link)
        issue={'title':i['title'], 'username':i['user']['login'], 'url':i['html_url'], 'session_link':sess_link}
        issues.append(issue)

    #issues = [{'title':'Title 1'}]   
    return render_template("index.html", nu_issues=nu_issues, issues=issues)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
