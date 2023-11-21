from locust import HttpUser, task, between

class TrucksMicroserviceUser(HttpUser):
    wait_time = between(1, 3)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_truck_id = None

    # Simulating retrieving all the trucks
    @task
    def retrieve_trucks(self):
        response = self.client.get("/retrieve-trucks")
        print(f"Response status code for /retrieve-trucks: {response.status_code}")

    # Simulating adding a new truck
    @task
    def add_truck(self):
        data = {
            "name": "TestTruck",
            "total_distance": 500,
            "average_trip_distance": 50,
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        response = self.client.post("/add-truck", json=data)
        print(f"Response status code for /add-truck: {response.status_code}")

        if response.status_code == 201:
            truck_id = response.json().get("truck_id")
            self.new_truck_id = truck_id

    # Simulating editing an existing truck
    @task
    def edit_truck(self):
        truck_id = 1
        data = {
            "id": truck_id,
            "name": "UpdatedTruck",
            "total_distance": 600,
            "average_trip_distance": 60,
            "latitude": 37.7749,
            "longitude": -122.4194
        }
        response = self.client.post("/edit-truck", json=data)
        print(f"Response status code for /edit-truck: {response.status_code}")

    # Simulating getting a specific truck
    @task
    def retrieve_truck(self):
        truck_id = 1
        response = self.client.get(f"/retrieve-truck?id={truck_id}")
        print(f"Response status code for /retrieve-truck: {response.status_code}")

    # Simulating deleting an existing truck
    @task
    def delete_truck(self):
        if self.new_truck_id is not None:
            data = {"id": self.new_truck_id}
            response = self.client.post("/delete-truck", json=data)
            print(f"Response status code for /delete-truck: {response.status_code}")
        else:
            print("No truck ID available to delete.")

    # Simulate getting conditions
    @task
    def get_conditions(self):
        response = self.client.get("/get-conditions")
        print(f"Response status code for /get-conditions: {response.status_code}")

    # Simulating getting the XML representation of a truck
    @task
    def retrieve_xml(self):
        truck_id = 1
        response = self.client.get(f"/retrieve-xml?id={truck_id}")
        print(f"Response status code for /retrieve-xml: {response.status_code}")

    # Simulating getting the JSON representation of a truck
    @task
    def retrieve_json(self):
        truck_id = 1
        response = self.client.get(f"/retrieve-json?id={truck_id}")
        print(f"Response status code for /retrieve-json: {response.status_code}")
