from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
api = Api(app)
ma = Marshmallow(app)
auth = HTTPBasicAuth()

USER_CRED = {
    "root": "password"
}

class db_schema(ma.Schema):
	class Meta:
		fields = ('id', 'country', 'city', 'currency', 'amount')

   
class DbTable(db.Model):
	# Create Database

	id = db.Column(db.Integer, primary_key=True)
	country = db.Column(db.String(100), nullable=False)
	city = db.Column(db.String(100), nullable=False)
	currency = db.Column(db.String(100), nullable=False)
	amount = db.Column(db.Float, nullable=False)

	def __init__(self, country, city, currency, amount):
		self.country = country
		self.city = city
		self.currency = currency
		self.amount = amount


schema = db_schema(strict=True)
schemas = db_schema(many=True, strict=True)


@auth.verify_password
def authentication(username, password):
	# Basic Authorization
    if not (username and password):
        return False
    return USER_CRED.get(username) == password


class GetPost(Resource):
	# Method GET and POST
	# Require login: Basic Auth

	# Get all data
	@auth.login_required
	def get(self):
		fetch_all_data = DbTable.query.all()
		json_output = schemas.dump(fetch_all_data)
		return json_output

	@auth.login_required	
	def post(self):
		
		data =  request.get_json(force=True)
		
		country = data.get('country')
		city = data.get('city')
		currency = data.get('currency')
		amount = data.get('amount')

		new_data_entry = DbTable(country, city, currency, amount)
		db.session.add(new_data_entry)
		db.session.commit()
		
		return schema.jsonify(new_data_entry)
		


class Update(Resource):
	@auth.login_required
	def put(self, num):
		put_data =  DbTable.query.get(num)
		data =  request.get_json(force=True)

		country = data.get('country')
		city = data.get('city')
		currency = data.get('currency')
		amount = data.get('amount')

		put_data.country = country
		put_data.city = city
		put_data.currency = currency
		put_data.amount = amount

		db.session.commit()

		return schema.jsonify(put_data)


class Delete(Resource):
	@auth.login_required
	def delete(self, num):
		del_data =  DbTable.query.get(num)
		db.session.delete(del_data)
		db.session.commit()
	
		return schema.jsonify(del_data)






api.add_resource(GetPost, '/api')
api.add_resource(Update, '/update/id/<int:num>')
api.add_resource(Delete, '/delete/id/<int:num>')


# fire up the Server
if __name__ == '__main__':
	app.run(debug=True)










