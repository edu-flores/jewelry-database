from locust import HttpUser, task, between

class GPSMicroserviceUser(HttpUser):
    wait_time = between(1, 3)

    # Simulate GPS microservice
    @task
    def get_locations(self):
        response = self.client.get("/get-locations")
        print(f"Response status code for /get-locations: {response.status_code}")
