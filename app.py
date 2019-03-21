"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Web Services using Python and MongoDB
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

''' For our API we will use the Flask library.
    Flask allows us to serve our code with a
    lightweight web server.  Flask can be used
    in poduction environments, however, if you
    plan to implement it the way I do in this
    document, then you're going to have a bad
    time in the long run.

    We also need a MongoDB library so that we
    can implement CRUD operations with our API.
'''

import flask
from flask import request, jsonify
import pymongo

# Creating our initial Flask object and setting
# the debug mode to something that is helpful

app = flask.Flask(__name__)
app.config["DEBUG"] = True




















"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Section One:  Helper Functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



''' Setup helper functions for later use.  
    These functions are not 'critical' for functionality,
    and each can be written on a per use basis for a given
    route.  However, I'm lazy, so I like to set this stuff
    up first.  They aren't complete, and in now way am I saying
    that this is the only way to accomplish this task.  If
    you can be more efficient/creative/innovative, then go
    right ahead... it wont hurt my feels, and bonus points if
    you are able to teach me something about Python.

    In practice, I would break these helper functions out into
    their own file and import them into this script for use.
    I much prefer to keep things neat and clean, plus it 
    keeps the focus on your API.
'''





















'''
    To connect to the MongoDB we have to establish a connection
    This will happen anytime we perform a CRUD operation, so
    I put it into a function to save a few lines of code.
    In practice... we would close the session with 
    client.close() once we are done with it.  I'm lazy and
    don't do this in this document, however, yous should as
    you build out your API.

    It reallly is a case of 'do as I say, not as I do'.
'''
def create_mongo_session(database, collection):
    client = pymongo.MongoClient('localhost', 27017)
    db = client[database]
    col = db[collection]
    return db, col


















'''
    I have created a few HTML forms, to show how a POST request
    works.  These forms return data into Flask in a strange
    way.  They are called MultiDicts, and are essentially a list
    of tuples, that get treated like dictionaries... I know right!

    What we gain from this is the ability to have a single key
    have multiple values.  What I mean by that is consider you
    have two middle names, and your database is just using 
    'middle-name' as a key.  This data type allows for you to
    correctly input that individuals middle names.

    But becuase of that, we have to parse it out and create a 
    dictionary that makes sense, or else we can't get the
    pymongo library to place nice with it for CRUD operations.
'''
def parse_form():
    x={}
    d = request.form
    for key in d.keys():
        value = request.form.getlist(key)
        x[key]=value
    return x



















'''
    I hope this is self-explanatory, but since we will be using
    this API to retrieve data from our database, I went ahead and
    created a function that will perform that query for us with
    varying parameters.

    Typically, the moment I write code more than once, I try to 
    create a function to accomplish that.  I try to be as lazy as
    possible when programming.  

    Do as you wish!
'''
def mongo_find(query):
    _, col = create_mongo_session('apitest', 'v1')
    find_result = []
    for i in col.find(query):
        find_result.append(i)
    return str(find_result)













'''
    Plot twist, I do this will every Mongo CRUD operation.
    Which is what you are going to see below, so I'll just
    show you all of that right now.

    I left two of these as incomplete, with the hopes that
    you implement them, but seriously think things through
    before you do.  There are large implications behind these
    operations.
'''
def mongo_insert_one(doc):
    #insert one document in the 'v1' collection of the 'apitest' database
    _, col = create_mongo_session('apitest', 'v1')
    col.insert_one(doc)

def mongo_insert_many(doc):
    #inserting many... just in case!
    db, col = create_mongo_session('somedb', 'somecol')
    col.insert_many(doc)

def mongo_delete():
    #delete some sh*t
    db, col = create_mongo_session('apitest', 'v1')
    return

def mongo_update():
    # update some s**t
    db, col = create_mongo_session('apitest', 'v1')
    return
        




















'''
    You should also consider experimenting with SQL libraries
    and implementing helper functions like this for your API.
    You may not be using MongoDB, and the API concepts will
    remain the same regardless of your database, however how
    you interact with that database will differ significantly.

    Notice how things like authentication have been left out?!
    That's one major reason setting this up in production is a 
    very bad thing!!  You should consider security at every
    step along the way.  

    There are also no request limits, consider what happens if
    someone makes 90million requests at once... this is called
    a denial of service attack, and can render your resources
    inaccessible.  If you are running on a cloud providers 
    platform, you will most likely be paying per request for
    things like this... and that bill gets expensive fast, so 
    consider everything!
'''



























"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Section 2:  The Web Service... Also Known As Our API
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

'''
    A web service in Flask is defined by routes.  Routes is just 
    a fancy word for URL.  Our routes will point to Python
    logic, and when we browse to them, something will happen to
    our MongoDB.
'''








'''
    Our first route is the root route.  This is
    what happens if I navigate to
    http://www.somesite.com/
    Nothing the / at the end of that URL?  That
    is defined within the @app.route line.  We
    also need to define what kind of request we
    are allowed to accept at this route.  

    In our case we will use a GET request, since 
    we will only be readin data at the root route
    and we wont be including any functionality there
    we have no need to use this route to POST data
    from the client to the server.
'''

# homepage
@app.route("/", methods=["GET"])
def home_page():
    #use a flask method to read a static HTML file
    #this file get's served everytime we got to /
    #Doing this allows for updates to the content
    #without dropping our application offline
    return flask.render_template('index.html')


















































'''
    The /api/v1 route uses flask to render another
    template from a static HTML file.  This is where
    our API starts however.  Somtimes you will see
    public API's have a /api/v1/docs route that contains
    instructions for using their API, this route is
    where I plan to put the instructions for our API.

    It's basic, so there is nothing to really see here
    when it comes to what happens at this route.
'''

# root for api/v1
@app.route('/api/v1', methods=['GET'])
def api_root():
    return flask.render_template('docs.html')
















































'''
    Let's start using some of our helper functions at these
    routes.  The first route will be the simplest one to 
    implement logic for. 

    We want a route that will return to us, ALL of the data
    in a given collection from a specific database.

    If you think back to our helper function (hint... go look)
    you will know which collection this is.

    In our case, the result of mongo_find() gets returned
    in the HTTP response when a HTTP GET request is made at
    this route.

    No GET request, no function.  However this route is only
    accepting of a GET request.  If we tried to use a POST,
    UPDATE, or DELETE we would see and error saying the 
    method is not allowed.

    Refer to the MongoDB documentation if you don't understand
    why {} was the filter arguement for our mongo_find function
'''

# GET to show data from MongoDB
@app.route('/api/v1/mongo/find/all', methods=['GET'])
def api_mongo_find_all():
    return mongo_find({})




















'''
    The next route implements even more logic.  It can
    look at whether or not the request at the route is 
    a GET or a POST, based on that information it determines
    which block of code to run.

    In our example, if the request is GET, then it will
    return a Flask method to render a form written in HTML.

    If the request is a POST, it calls some of our helper
    functions to extract the data from the form and then
    run the query based on the form information.

    POST is necessary here becuase the action our form
    makes, located in the query.html file, is a POST when
    the submit button is pressed.
'''

# GET to filter find query from MongoDB
@app.route('/api/v1/mongo/find', methods=['GET', 'POST'])
def api_mongo_find():
    if request.method == 'GET':
        return flask.render_template('query.html')
    elif request.method == 'POST':
        data = parse_form()
        return mongo_find(data)
































'''
    What if we aren't building a front end and our API is
    designed to be used strictly with query strings in the
    URL?

    Good news, we can accomodate that.  

    The following route only listens for a GET request,
    and it takes the arguments from the request and uses
    them in our mongo_find() function.

    Refer to HTTP query strings for more information about
    how to craft a query like this (hint:  give examples
    in your documentation!)
'''

# GET to filter find query from MongoDB with request.args
@app.route('/api/v1/mongo/findargs', methods=['GET'])
def api_mongo_find_args():
    return mongo_find(request.args)

























'''
    Let's take a look at inserting data into our database
    with our API.  This is going to get a little confusing,
    since we will do this with a GET as well as a POST request, 
    so stick with me.

    Upon sending a GET request to this route, such as
    navigation to it in a web browser, or crafting a request
    with a programming language, if the GET flag is set in the
    header, the logic runs.  That's really all there is to
    consider.

    Don't get confused with GET being for reading data, and
    POST being for writing it, that's not what they are for.
    They exist to do stuff based on flags set on each reqeust
    and BOTH can read or write data!

    You'll notice that our parse_forms() function is pretty
    much replicated in this block of code.  However, it is
    modified slightly.  This is for demonstration purposes,
    you should absolutely create a function out of this if
    you plan to implement somethign like this.

    Again, we take the request arguments, only this time those
    arguements aren't for reading data based on a filter, they
    become the data that we plan to write into the database.
'''

# GET to insert data to MongoDB with request.args
@app.route('/api/v1/mongo/insertargs', methods=['GET'])
def api_mongo_insert_args():
    x = {}
    args = request.args
    for key in args.keys():
        value = request.args.getlist(key)
        x[key]=value
    mongo_insert_one(x)
    return "data inserted"

'''
    Now let's do it by sending a POST request from our form.
    This draws parrallels to someone entering their login 
    credentials, when they click submit a POST request goes
    out, and the POST logic fires.
'''

# POST to create new entry to Mongodb
@app.route('/api/v1/mongo/insert', methods=['GET', 'POST'])
def api_mongo_insert():
    if request.method == 'GET':
        return flask.render_template('mongoinsert.html')
    elif request.method == 'POST':
        #we have to use our parse_form() function becuase of
        #how Flask handles responses
        data = parse_form()
        mongo_insert_one(data)
        #another Flask method is used, this time to redirect
        #the browser to the API root.  You could create something
        #that shows the newly inserted data instead
        return flask.redirect(flask.url_for('api_root'))







































"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Section 3:  Extra Lab Exercises
skip to the bottom before covering this, let's take a look at what exists
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




'''
    Exercise 1:  build the following route using what you know
                 and the PyMongo library
'''
# POST to update old entry from MongoDB
@app.route('/api/v1/mongo/update', methods=['GET', 'POST'])
def api_mongo_update():
    return "<h1>mongo update</h1>"



'''
    Exercise 2:  Create and API to query your HR database
'''
# GET to show data from Oracle 12c
@app.route('/api/v1/oracle/find', methods=['GET'])
def api_oracle_find():
    return "<h1>12c find</h1>"

# POST to create new entry to Oracle 12c
@app.route('/api/v1/oracle/insert', methods=['GET', 'POST'])
def api_oracle_insert():
    return "<h1>12c insert</h1>"

# POST to update data in Oracle 12c
@app.route('/api/v1/oracle/update', methods=['GET', 'POST'])
def api_oracle_update():
    return "<h1>12c update</h1>"

































"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
START THE FLASK SERVER OR ELSE NO ROUTES WILL WORK
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Tell flask to start serving your API and specify which port to serve on!
app.run(port=80)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Exercise 3:
    Explore the API though PostMan, the web browser, and other API navigation
    tools like insomnia.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Discussion Topics:
    Why is there no route to delete entries from the databases?
    Could we do such a thing with a route?
    Would a GET, POST, or other flag be used to delete data?
    What makes a good API?
    Does our API make sense?
    What would you change?
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""





    

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Micro Project:  Building and Sharing API's

    Step 1:
        Each team has been given a JSON file containing data.  You must import
        that data into MongoDB, then write an API for others to use against
        you're data.  They will not know what your database contains, each
        group has been given different data.

    Step 2:
        Using another teams API, take what you have learned about data
        analysis and query their database for interesting data.  Create
        a presentation about what you were able to find.  Lean on the skills
        you learned during data visualization, using libraries like matplotlib
        and the others.

        Build a report about the data, (seriously, be creative, the data
        is fun, analyze it as you wish).

    Step 3:
        Formulate a presentation about using the other teams API.  What
        went well, what was easy, what was hard, what couldn't you do,
        would you recommend this API to others?  Could you get the information
        you wanted?  Did their routes make sense?

        The purpose is to understand what may or may not go into an API,
        not to demean the other team... unless their API is really 
        just that bad.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""






















