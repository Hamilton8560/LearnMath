import unittest
from unittest import TestCase
import requests 
import random
import string
import json
import os


# test case for heath status
class HealthStatusCheck(TestCase):
    # test successful response
    def test_status_codes_200(self):
        result = requests.get("http://127.0.0.1:3000/api/health/status")
        assert result.status_code == 200
        assert "service" in result.json()
        assert result.json()["service"] == "Running"
    
    # test not found due to incorrect url
    def test_status_codes_404(self):
        result = requests.get("http://127.0.0.1:3000/api/health/")
        assert result.status_code == 404
        assert "status" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["response"] == "Not found" 
    
    # test method not allowed
    def test_status_codes_405(self):
        result = requests.put("http://127.0.0.1:3000/api/health/status")
        assert result.status_code == 405
        assert "status" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["response"] == "Method not allowed"


# test users API calls to /api/users/create API endpoint
class UsersCreatedCheck(TestCase):
    """
    /api/usrs/create

    Endpoint is used for account creation. Expecting firstName, lastName, email and password within 
    request body. Account email addresses are unique and passwords constraints require 1 uppercase and lowercase characters, 
    1 numeric chaaracter, and between 8-16 character range.
    """

    # Test successful account creation
    def test_status_codes_200(self):
        # expected fail, no body
        data = json.dumps({
            "firstName": "test",
            "lastName": "account",
            "email": "Test." + "".join( 
                random.choice( string.ascii_lowercase) for _ in range(6) )
                + "@email.com",
            "password": "Test123!"
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 201
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "success"
        assert result.json()["created"] == True
        assert result.json()["response"] == "Account successfully created!" 
    
    
    # Test invalid responses
    def test_status_codes_400(self):
        # expected fail, no body
        data = {}
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Invalid request, request.body must be json format." 
    
        # expected fail, invalid body
        data = json.dumps({
            "test": "foo"
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Missing firstName, lastName, email, password values within body." 

        # expected fail, invalid email address format
        data = json.dumps({
            "firstName": "foo",
            "lastName": "bar",
            "email": "foo.bar",
            "password": "Test1234!"
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Invalid email address format."

       
        # expected fail, password does not meet minimum length
        data = json.dumps({
            "firstName": "bar",
            "lastName": "baz",
            "email": "bar.baz@email.com",
            "password": "Test1!"
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Password range must be between (8-16) characters."

        # expected fail, password exceeds maximum length
        data = json.dumps({
            "firstName": "bar",
            "lastName": "baz",
            "email": "bar.baz@email.com",
            "password": "Test123456789012!" # 17 chars
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Password range must be between (8-16) characters."

        # expected fail, password must contain 1 special character
        data = json.dumps({
            "firstName": "bar",
            "lastName": "baz",
            "email": "bar.baz@email.com",
            "password": "Test1234" # 17 chars
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Password must contain 1 special character."
        
        # expected fail, password must contain 1 uppcase character
        data = json.dumps({
            "firstName": "bar",
            "lastName": "baz",
            "email": "bar.baz@email.com",
            "password": "test123!" 
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Password must contain 1 uppercase character."

        # expected fail, password must contain 1 lowercase character
        data = json.dumps({
            "firstName": "bar",
            "lastName": "baz",
            "email": "bar.baz@email.com",
            "password": "TEST123!" 
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Password must container 1 lowercase chatacter."

        # expected fail, password must contain 1 numeric character
        data = json.dumps({
            "firstName": "bar",
            "lastName": "baz",
            "email": "bar.baz@email.com",
            "password": "Testtest!" # 17 chars
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 400
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Password must contain 1 numeric character."

    def test_status_codes_401(self):
         # expected fail, email already exists
        data = json.dumps({
            "firstName": "foo",
            "lastName": "bar",
            "email": "foo.bar@email.com",
            "password": "Test123!"
        })
        result = requests.post("http://127.0.0.1:3000/api/users/create", data=data)
        assert result.status_code == 401
        assert "status" in result.json()
        assert "created" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["created"] == False
        assert result.json()["response"] == "Email address already exists, please sign in."
        
    # test not found due to incorrect url
    def test_status_codes_404(self):
        result = requests.get("http://127.0.0.1:3000/api/users/")
        assert result.status_code == 404
        assert "status" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["response"] == "Not found" 
    
    # test method not allowed
    def test_status_codes_405(self):
        result = requests.put("http://127.0.0.1:3000/api/health/status")
        assert result.status_code == 405
        assert "status" in result.json()
        assert "response" in result.json()
        assert result.json()["status"] == "error"
        assert result.json()["response"] == "Method not allowed"




if __name__ == "__main__":
    unittest.main()