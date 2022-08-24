#set up the flask and create the routes
from flask import Flask

#create the instance
app = Flask(__name__)

# define the root or starting point
# `/` denotes that we want to put our data at the root of our routes. 
@app.route('/')

# create the function
def hello_world():
    return 'Hello world'


###################################################################
# use the Py command prompt or git bash, run flask to get host website

# set FLASK_APP=app.py   (start flask)
# flask run              (return local URL)

# copy/paste into browser
###################################################################