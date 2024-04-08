#!/usr/bin/env python3

####################################################################################
#
# This file contains the routes for our shortURL webapp
#
####################################################################################

import sys
from flask import Flask, jsonify, abort, request, make_response, session, redirect
from flask_restful import reqparse, Resource, Api
from flask_session import Session
import json
from ldap3 import Server, Connection, ALL
from ldap3.core.exceptions import *
import ssl #include ssl libraries
import pymysql.cursors
import json
import string
import random

from db_util import db_access
import settings

# Set Server-side session config: Save sessions in the local app directory.
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_NAME'] = 'peanutButter'
app.config['SESSION_COOKIE_DOMAIN'] = settings.APP_HOST
#Session(app)

####################################################################################
#
# Error handlers
#
@app.errorhandler(400) # decorators to add to 400 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Bad request' } ), 400)

@app.errorhandler(404) # decorators to add to 404 response
def not_found(error):
	return make_response(jsonify( { 'status': 'Resource not found' } ), 404)

####################################################################################
#
# Routes for the /url endpoint
# Routing: GET using Flask-Session
#

class Root(Resource):
   # get method. What might others be aptly named? (hint: post)
	def get(self):
		return app.send_static_file('static/index.html')

class Url(Resource):
	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET d '{"url": "https://www.youtube.com"}' -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:8028/url
	def get(self):
		if not request.json:
			abort(400) # bad request

			# Parse the json
			parser = reqparse.RequestParser()
		try:
			# Check for required attributes in json document, create a dictionary
			parser.add_argument('url', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

			sqlProc = 'getAllUrl'
			sqlArgs = [request_params['url']]
		try:
			rows = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(500, e) # server error
		if not rows:
			responseCode = 404
			return make_response(jsonify(rows), responseCode)

		responseCode = 200
		return make_response(jsonify(rows), responseCode)
	
	def post(self):
		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('url', type=str, required=True)
			parser.add_argument('username', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		if request_params['url'] and request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
			
		url = request_params['url']
		username = request_params['username']
		sqlProc = 'getUserID'
		sqlArgs = [username]
		try:
			result = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(403, e) # server error
		if result:
			id = (result[0].get('ID'))
		else:
			return "User not found", 403
		sqlProc = 'addURL'
		characters = string.ascii_letters + string.digits
		tiny = ''.join(random.choice(characters) for _ in range(6))
		sqlArgs = [id, url, tiny]
		try:
			result = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(403, e) # server error
		if result:
			id = (result[0].get('ID'))
			return "https://cs3103.cs.unb.ca:8028/"+tiny, 200
		else:
			return "User not found", 403
	#TODO
	def delete(self):
		if not request.json:
			abort(400) # bad request
		
		url = request.json.get('url')
		username = request.json['username'] # This is returning id for some reason
		print(request.json['username'])

		if url and username in session:
			response = {'status': 'success'}
			responseCode = 200
			
		sqlProc = 'removeURL'
		sqlArgs = [username, url]
		try:
			result = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(403, e) # server error
		if result:
			return make_response({'status': 'Record was successfully deleted'}, 200)
		else:
			return make_response({'status': 'Record not deleted'}, 403)

		

	
	
class ShortUrl(Resource):
	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:8028/<short_url>
	def get(self, short_url):
		sqlProc = 'getURL'
		sqlArgs = [short_url]
		try:
			result = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(500, e) # server error
		if result:
			return redirect(result[0].get('LONGURL'))
		else:
			return "URL not found", 404


####################################################################################
#
# Routes for the /user/<int:id>/url endpoint
# Routing: GET using Flask-Session
#
class User(Resource):
	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:8028/user/<int:id>/url
	def get(self, id):
		sqlProc = 'getUsersURLs'
		sqlArgs = [id]
		try:
			rows = db_access(sqlProc, sqlArgs)
		except Exception as e:
			abort(500, e) # server error

		responseCode = 200
		return make_response(jsonify(rows), responseCode)


####################################################################################
#
# Routes for the /signin endpoint
# Routing: GET and POST using Flask-Session
#
class SignIn(Resource):
	#
	# Set Session and return Cookie
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X POST -d '{"username": "Casper", "password": "crap"}'
	#  	-c cookie-jar -k https://cs3103.cs.unb.ca:8028/signin
	#
	# FIX THIS SO MY USER WORKS
	def post(self):
		if not request.json:
			abort(400) # bad request

		# Parse the json
		parser = reqparse.RequestParser()
		try:
 			# Check for required attributes in json document, create a dictionary
			parser.add_argument('username', type=str, required=True)
			parser.add_argument('password', type=str, required=True)
			request_params = parser.parse_args()
		except:
			abort(400) # bad request

		if request_params['username'] in session:
			response = {'status': 'success'}
			responseCode = 200
		else:
			try:
				ldapServer = Server(host=settings.LDAP_HOST)
				ldapConnection = Connection(ldapServer,
					raise_exceptions=True,
					user='uid='+request_params['username']+', ou=People,ou=fcs,o=unb',
					password = request_params['password'])
				ldapConnection.open()
				ldapConnection.start_tls()
				ldapConnection.bind()
				# At this point we have sucessfully authenticated.
				session['username'] = request_params['username']
				response = {'status': 'success' }
				responseCode = 201

				sqlProc = 'getUserID'
				sqlArgs = (request_params['username'],)
				result = db_access(sqlProc, sqlArgs)
				if len(result) == 0:
					sqlProc = 'addUser'
					result = db_access(sqlProc, sqlArgs)

				session['id'] = result[0]['ID']	
				response = {'status': 'success', 'id' : result[0]['ID']	}	
			except Exception as e:
				print("An error has occurred:", str(e))
				print("Type of exception:", type(e))
				print("More info:", e.args)
				response = {'status': 'Access denied'}
				responseCode = 403
			finally:
				ldapConnection.unbind()

		return make_response(jsonify(response), responseCode)

	# GET: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X GET -b cookie-jar
	#	-k https://cs3103.cs.unb.ca:61340/signin
	def get(self):
		success = False
		if 'username' in session:
			username = session['username']
			response = {'status': 'success'}
			responseCode = 200
		else:
			response = {'status': 'fail'}
			responseCode = 403

		return make_response(jsonify(response), responseCode)

	# DELETE: Check Cookie data with Session data
	#
	# Example curl command:
	# curl -i -H "Content-Type: application/json" -X DELETE -b cookie-jar
	#	-k https://info3103.cs.unb.ca:61340/signin

	#
	#	Here's your chance to shine!
	#
	def delete(self):
		if 'username' in session:
			session.pop('username', None)
			response = {'status': 'logged out'}
			responseCode = 200
		else:
			response = {'status': 'session not present'}
			responseCode = 404

		return make_response(jsonify(response), responseCode)

####################################################################################
#
# Identify/create endpoints and endpoint objects
#
api = Api(app)
api.add_resource(Root,'/')
api.add_resource(Url, '/url')
api.add_resource(User, '/user/<int:id>/url')
api.add_resource(SignIn, '/signin')
api.add_resource(ShortUrl, '/<short_url>')


#############################################################################
# xxxxx= last 5 digits of your studentid. If xxxxx > 65535, subtract 30000
if __name__ == "__main__":
	#
	# You need to generate your own certificates. To do this:
	#	1. cd to the directory of this app
	#	2. run the makeCert.sh script and answer the questions.
	#	   It will by default generate the files with the same names specified below.
	#
	context = ('cert.pem', 'key.pem') # Identify the certificates you've generated.
	app.run(
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		ssl_context=context,
		debug=settings.APP_DEBUG)
