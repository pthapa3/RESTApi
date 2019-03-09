# Test script for RESTApi


from rest_api import app, db
import unittest
from flask_testing import TestCase
import base64
import json


class BasicTest(TestCase):

    def create_app(self):
        
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



class TestMethods(BasicTest):
    def test_unauth(self):
        response = self.client.get('/api')
        self.assert401(response=response, message=None) 

    def test_invalid_username(self):
        invalid_usr = base64.b64encode(b'admin:password').decode('utf-8')
        response = self.client.get('/api?', headers={'Authorization': 'Basic ' + invalid_usr})
        self.assertEqual(response.status_code, 401) 

    def test_invalid_pass(self):
        invalid_pass = base64.b64encode(b'admin:pass').decode('utf-8')
        response = self.client.get('/api?', headers={'Authorization': 'Basic ' + invalid_pass})
        self.assertEqual(response.status_code, 401) 


    def test_get(self):
        valid_credentials = base64.b64encode(b'root:password').decode('utf-8')
        response = self.client.get('/api', headers={'Authorization': 'Basic ' + valid_credentials})
        self.assertEqual(response.status_code, 200) 

    def test_post(self):
        valid_credentials = base64.b64encode(b'root:password').decode('utf-8')
        post_data =  {
                        "country": "FR",
                        "city": "Paris",
                        "currency": "EUR",
                        "amount": 20
                      }
       
        response = self.client.post('/api', data = (json.dumps(post_data)), headers={'Authorization': 'Basic ' + valid_credentials})
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data())
        self.assertEqual(json_response['amount'], 20)

    def test_put(self):
        valid_credentials = base64.b64encode(b'root:password').decode('utf-8')
        post_data =  {
                        "country": "FR",
                        "city": "Paris",
                        "currency": "EUR",
                        "amount": 20
                      }
       
        response = self.client.post('/api', data = (json.dumps(post_data)),
                     headers={'Authorization': 'Basic ' + valid_credentials})
        self.assertEqual(response.status_code, 200)
        
        put_data =  {
                        "country": "FR",
                        "city": "Paris",
                        "currency": "EUR",
                        "amount": 25.0
                      }
        response = self.client.put('/update/id/1', data = (json.dumps(put_data)), 
                    headers={'Authorization': 'Basic ' + valid_credentials})
       
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data())
        self.assertEqual(json_response['amount'], 25.0)

    def test_delete(self):
        valid_credentials = base64.b64encode(b'root:password').decode('utf-8')
        post_data =  {
                        "country": "FR",
                        "city": "Paris",
                        "currency": "EUR",
                        "amount": 20
                      }

        response = self.client.post('/api', data = (json.dumps(post_data)),
                   headers={'Authorization': 'Basic ' + valid_credentials})
        self.assertEqual(response.status_code, 200)
        response = self.client.delete('/delete/id/1', headers={'Authorization': 'Basic ' + valid_credentials})
        self.assertEqual(response.status_code, 200)
        result = self.client.get('/api/1', headers={'Authorization': 'Basic ' + valid_credentials})
        self.assertEqual(result.status_code, 404)




    


if __name__ == '__main__':
    unittest.main()



















