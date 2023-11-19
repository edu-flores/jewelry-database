from locust import HttpUser, task, between
import random

class AuthMicroserviceUser(HttpUser):
    wait_time = between(1, 3)

    # Simulating an authentication
    @task
    def check_auth(self):
        data = {"username": "raul.moraless@udem.edu", "password": "666"}
        response = self.client.post("/check-auth", json=data)
        print(f"Response status code for /check-auth: {response.status_code}")

    # Simulating a new user registration
    @task
    def register_user(self):
        data = {
            "name": "Locust",
            "lastname": "Test",
            "username": ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(12)) + "@gmail.com",
            "password": "123"
        }
        response = self.client.post("/new-user", json=data)
        print(f"Response status code for /new-user: {response.status_code}")
