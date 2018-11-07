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

app = Flask(__name__)

logger = logging.getLogger()

GITHUB_URL = "https://api.github.com/repos/ojalatodd/fullstory/issues"

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

    data = get_url(url=GITHUB_URL)
    #Get the parts of the data that we want:
    
    no_issues = len(data)
    print("There are {} issues".format(no_issues))

    results_string = ""
    count = 1
    for i in data:
        results_string += "Issue number " + str(count) + ": "
        title = i['title']
        results_string += title + ", "
        username = i['user']['login']
        results_string += "Username: " + username + ", "
        issue_url = i['url']
        results_string += "URL to issue: " + issue_url + ", "
        
        # Get the link to the fullstory session for this user
        fullstory_session_link = "http://blah.com"
        
        results_string += "Fullstory session link for user: " + fullstory_session_link + " *** "

    
    
    #return("Welcome to the great new web app!")
    return render_template("index.html", no_issues=no_issues, results_string=results_string)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
