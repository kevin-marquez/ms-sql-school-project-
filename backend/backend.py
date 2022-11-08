#### Final Project Sprint 1 ####
'''
Kevin Marquez
CIS 3368
10/8/22
'''

from types import NoneType
import flask
from flask import jsonify
from flask import request 
from flask import request, make_response
import mysql.connector 
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
import creds
from operator import itemgetter
import hashlib

# setting up an application name 
app = flask.Flask(__name__) # sets up the application 
app.config["DEBUG"] = True # allow to show errors in browser \


#### login ####
# I have created two login API. login1 uses headers through postman and login2 uses browser login.
# for both the username is "flights" and password is "password"



# Login using headers through postman. username: flights and password: password. 
authorizedusers = [
    {
        #Admin user
        'username': 'flights',
        'password': 'password', 
        'Role': 'You are clear to view flights, and run CRUD operations on planes and aiports.',
    }
]
@app.route('/api/login1', methods=['GET'])
def login_headers():
    username = request.headers['username'] #get the header parameters (as dictionaries)
    pw = request.headers['password']
    for auth in authorizedusers: #loop over all users and find one that is authorized to access
        if auth['username'] == username and auth['password'] == pw: #found an auth user
            return '<h1> You are authorized to view, create and delete flights. You may also run CRUD operations on planes and airports. </h1>'

    return 'SECURITY ERROR' 


# Login using browser. basic http authentication, prompts username and password upon contacting the endpoint. username: flights an password: password
masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8" # password 'password' hashed
masterUsername = 'flights'
@app.route('/api/login2', methods=['GET'])
def login_browser():
    if request.authorization:
        encoded=request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> Welcome to flights manager software! </h1>'
    return make_response('COULD NOT VERIFY!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})





#### airports ####
#POST
@app.route('/api/airports/post', methods = ['POST']) #adds a new airports record by a json format object through postman(body,raw,json)
def api_airports_post():
    request_data = request.get_json()

    new_airportcode = request_data['airportcode']
    new_airportname = request_data['airportname']
    new_country = request_data['country']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    query = "INSERT INTO airports (airportcode, airportname, country) VALUES('%s', '%s', '%s')" %(new_airportcode, new_airportname, new_country)
    execute_query(conn, query)
    return 'POST request was successful'
''' 
Here is a handy json object to copy and paste on to postman for post method body:
{
"airportcode": "_",
"airportname": "_",
"country": "_",
}
'''

# GET
@app.route('/api/airports/get', methods = ['GET']) # show table for airports 
def api_airports_get():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM airports"
    airports = execute_read_query(conn, sql)
    return jsonify(airports) 

#PUT
@app.route('/api/airports/put', methods = ['PUT']) # updates a airports record by parameter 'airportcode' and desired field to be changed 
def api_airports_put():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    if 'airportcode' in request.args: #sets which airport is going to be updated by airport code
        airportToUpdate = request.args['airportcode']
    else:
        return 'ERROR: No Airport Code Provided'

    #looks for second argument/parameter to determince which field wants to get updated (options are airportname, country, and id)
    if 'airportname' in request.args: # Airport Name
        updateField = request.args['airportname']
        update_airports_query = """
        UPDATE airports 
        SET airportname = '%s'
        WHERE airportcode = '%s'
        """ %(updateField, airportToUpdate)

        execute_query(conn, update_airports_query)
        return 'Airport Name update request was successful'   

    elif 'country' in request.args: # Airport Country
        updateField = request.args['country']
        update_airports_query = """
        UPDATE airports 
        SET country = '%s'
        WHERE airportcode = '%s'
        """ %(updateField, airportToUpdate)

        execute_query(conn, update_airports_query)
        return 'Airport Country update request was successful'  

    elif 'id' in request.args: #Airport ID
        updateField = request.args['id']
        update_airports_query = """
        UPDATE airports 
        SET id = %s
        WHERE airportcode = '%s'
        """ %(updateField, airportToUpdate)

        execute_query(conn, update_airports_query)
        return 'Airport id update request was successful'   

    else:
        return 'ERROR: No Field Provided' # There wasnt a second argument/parameter inputed 

#DELETE
@app.route('/api/airports/delete', methods = ['DELETE']) #will delete record by parameter 'airportcode' 
def api_airports_delete():
    if 'airportcode' in request.args: 
        airportToDelete = request.args['airportcode']
    else:
        return 'ERROR: No Airport Code Provided'
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM airports"
    airports = execute_read_query(conn, sql)
    for records in range(len(airports)-1, -1, -1): #(start, stop, step size)
        if airports[records]['airportcode'] == airportToDelete:
            delete_statement = "DELETE FROM airports WHERE airportcode = '%s'" %airportToDelete
            execute_query(conn, delete_statement)
    return 'Delete airport "%s" request successful' %airportToDelete




#### planes ####
#POST
@app.route('/api/planes/post', methods = ['POST']) #adds a new planes record by a json format object through postman(body,raw,json)
def api_planes_post():
    request_data = request.get_json()

    new_make = request_data['make']
    new_model = request_data['model']
    new_year = request_data['year']
    new_capacity = request_data['capacity']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    query = "INSERT INTO planes (make, model, year, capacity) VALUES('%s', '%s', %s, %s)" %(new_make, new_model, new_year, new_capacity)
    execute_query(conn, query)
    return 'POST request was successful'
''' 
Here is a handy json object to copy and paste on to postman for post method body:
{
"make": "_",
"model": "_",
"year": _,
"capacity": _
}
'''

# GET
@app.route('/api/planes/get', methods = ['GET']) # show table for planes 
def api_planes_get():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM planes"
    planes = execute_read_query(conn, sql)
    return jsonify(planes) 

#PUT
@app.route('/api/planes/put', methods = ['PUT']) # updates a planes record by parameter 'model' and desired field to be changed 
def api_planes_put():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    if 'model' in request.args: #sets which plane is going to be updated by plane model
        planeToUpdate = request.args['model']
    else:
        return 'ERROR: No Plane Model Provided'

    #looks for second argument/parameter to determince which field wants to get updated (options are capacity, id, make, and year)
    if 'capacity' in request.args: # Plane Capacity
        updateField = int(request.args['capacity'])
        update_planes_query = """
        UPDATE planes 
        SET capacity = %s
        WHERE model = '%s'
        """ %(updateField, planeToUpdate)

        execute_query(conn, update_planes_query)
        return 'Plane Capacity update request was successful'   

    elif 'id' in request.args: # Plane ID
        updateField = int(request.args['id'])
        update_planes_query = """
        UPDATE planes 
        SET id = %s
        WHERE model = '%s'
        """ %(updateField, planeToUpdate)

        execute_query(conn, update_planes_query)
        return 'Plane ID update request was successful'  

    elif 'make' in request.args: # Plane Make
        updateField = request.args['make']
        update_planes_query = """
        UPDATE planes 
        SET make = '%s'
        WHERE model = '%s'
        """ %(updateField, planeToUpdate)

        execute_query(conn, update_planes_query)
        return 'Plane Make update request was successful'

    elif 'year' in request.args: # Plane Year
        updateField = request.args['year']
        update_planes_query = """
        UPDATE planes 
        SET year = %s
        WHERE model = '%s'
        """ %(updateField, planeToUpdate)

        execute_query(conn, update_planes_query)
        return 'Plane year update request was successful'

    else:
        return 'ERROR: No Field Provided' # There wasnt a second argument/parameter inputed 

#DELETE
@app.route('/api/planes/delete', methods = ['DELETE']) #will delete record by parameter 'model' 
def api_planes_delete():
    if 'model' in request.args: 
        planeToDelete = request.args['model']
    else:
        return 'ERROR: No Plane Model Provided'
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM planes"
    planes = execute_read_query(conn, sql)
    for records in range(len(planes)-1, -1, -1): #(start, stop, step size)
        if planes[records]['model'] == planeToDelete:
            delete_statement = "DELETE FROM planes WHERE model = '%s'" %planeToDelete
            execute_query(conn, delete_statement)
    return 'Delete model "%s" request successful' %planeToDelete




#### Flights #### 
#POST
@app.route('/api/flights/post', methods = ['POST']) #adds a new flights record by a json format object through postman(body,raw,json)
def api_flights_post():
    request_data = request.get_json()

    new_planeid = request_data['planeid']
    new_airportfromid = request_data['airportfromid']
    new_airporttoid = request_data['airporttoid']
    new_date = request_data['date']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    query = "INSERT INTO flights (planeid, airportfromid, airporttoid, date) VALUES(%s, %s, %s, '%s')" %(new_planeid, new_airportfromid, new_airporttoid, new_date)
    execute_query(conn, query)
    return 'POST request was successful'
''' 
Here is a handy json object to copy and paste on to postman for post method body:
{
"planeid": _,
"airportfromid": _,
"airporttoid": _,
"date": "YYYY-MM-DD"
}
'''

# GET
@app.route('/api/flights/get', methods = ['GET']) # show table for flights
def api_flights_get():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM flights"
    flights = execute_read_query(conn, sql)
    return jsonify(flights) 


#DELETE
# I chose to delete by flight id since its the only thing that uniquely identifies each flight 
@app.route('/api/flights/delete', methods = ['DELETE']) #will delete record by parameter 'id' 
def api_flights_delete(): # uses Query params in postman 
    if 'id' in request.args: 
        flightToDelete = int(request.args['id'])
    else:
        return 'ERROR: No Flight ID Provided'
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    sql = "SELECT * FROM flights"
    flights = execute_read_query(conn, sql)
    for records in range(len(flights)-1, -1, -1): #(start, stop, step size)
        if flights[records]['id'] == flightToDelete:
            delete_statement = "DELETE FROM flights WHERE id = %s" %flightToDelete
            execute_query(conn, delete_statement)
    return 'Delete Flight ID "%s" request was successful' %flightToDelete



app.run()
