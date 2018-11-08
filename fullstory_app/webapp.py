'''
This app displays a list of github issues that have been raised
by users who also have captured Fullstory sessions!

Usage: 
python webapp.py 

If python doesn't link to python version 3.x, use:
python3 webapp.py

Runs on port: 8080

Password for github user: 
The password for the github user that owns the web app being tracked is
stored in a text file in the same directory as the app named password.txt

November 7, 2018
Updated version: November 8, 2018

Copyright Todd Ojala, 2018

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

GITHUB_ISSUES = "https://api.github.com/repos/ojalatodd/fullstory/issues" 
FULLSTORY_URL = "https://www.fullstory.com/api/v1/sessions"

GITHUB_USER_EMAILS = "https://api.github.com/user/emails"

# Retrieve password for github account
file = open('password.txt')
passwd = file.read().strip()


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
    '''
    Display all the issues associated with the Web Calculate app
    Then display the links to Fullstory sessions associated with 
    the github users who submitted the issue, if they exist.

    '''

    github_data = get_url(url=GITHUB_ISSUES)
    nu_issues = len(github_data)

    # Create a session with auth using special Fullstory authentication
    s = requests.Session()
    s.headers.update({'Authorization': 'Basic Rzc5NEI6UnpjNU5FSTZRVVZDYjJaSllUWmFlVlEwT0hwR2JYZFdhVWhPTm5aNmRtUkdRMEpGYkRSRllXRnBVeXM0V1M4NVRUMD0='})

    # Create a session with basic user/password auth for github
    s2 = requests.Session()
    s2.auth = ('ojalatodd', passwd)

    issues = []  # Initialize the list that holds all the issues

    for i in github_data:
        
        # Get the email to use for retrieving Fullstory sessions
        email_data = s2.get(GITHUB_USER_EMAILS).json()
        email = email_data.pop(0)['email']

        # Get the Fullstory session data for this user based on email.
        sess_data = s.get(FULLSTORY_URL, params={'email':email}).json()
        
        # Get the link to the session
        first_session = sess_data.pop() # Only get last session in this beta version
        sess_link = first_session['FsUrl']
        print(sess_link)

        # Construct a dict that stores the data we want to display on the web page
        issue={'title':i['title'], 'username':i['user']['login'], 'url':i['html_url'], 'session_link':sess_link}
        issues.append(issue)

    return render_template("index.html", nu_issues=nu_issues, issues=issues)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
