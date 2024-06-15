from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error 
from flask_bcrypt import Bcrypt


app = Flask(__name__)
bcrypt=Bcrypt()



def connect_to_database():
	try:
		connection= mysql.connector.connect(
			host = '127.0.0.1',
			port = '3306',
			database= 'your-db-name',
			user='your-db-username',
			password='your-db-password'

			)
		if connection.is_connected():
			return connection
	except Error as e:
		print("Error while connecting to Mysql:", e)
		return None
@app.route('/register', methods=['POST'])
def register_user():
	try:
		data= request.get_json()
		username=data.get('username')
		password= data.get('password')

		if username and password:
			hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')

			connection = connect_to_database()
			if connection:
				cursor= connection.cursor()
				insert_query="INSERT INTO users (username, password_hash)  VALUES(%s, %s)"
				cursor.execute(insert_query, (username, hashed_password))
				connection.commit()
				cursor.close()
				connection.close()
				return jsonify({"message":"User registered successfully"}),201
			else:
				return jsonify({"error":"Failed to connect to database"}), 500
		else:
			return jsonify({"error":"Username ad password are required"}), 400
	except Exception as e:
		print("Error:", e)
		return jsonify({"error":"Internal server"}), 500

if __name__=='__main__':
	app.run(host='0.0.0.0', port=5000)


				

