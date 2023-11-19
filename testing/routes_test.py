from locust import HttpUser, task, between

class RoutesMicroserviceUser(HttpUser):
    wait_time = between(1, 3)

    # Simulating getting all routes
    @task
    def retrieve_routes(self):
        response = self.client.get("/retrieve-routes")
        print(f"Response status code for /retrieve-routes: {response.status_code}")

    # Simulating adding a route
    @task
    def add_route(self):
        data = {
            "name": "TestRoute",
            "distance": 1234567,
            "active": 1,
            "average_speed": 50,
            "time": 120,
            "truck_id": 1
        }
        response = self.client.post("/add-route", json=data)
        print(f"Response status code for /add-route: {response.status_code}")

        if response.status_code == 201:
            route_id = response.json().get("route_id")
            self.new_route_id = route_id

    # Simulating editing a route
    @task
    def edit_route(self):
        route_id = 1
        data = {
            "id": route_id,
            "name": "EditedRoute",
            "distance": 15000,
            "active": 0,
            "average_speed": 605,
            "time": 180,
            "truck_id": 2
        }
        response = self.client.post("/edit-route", json=data)
        print(f"Response status code for /edit-route: {response.status_code}")

    # Simulating getting a specific route
    @task
    def retrieve_route(self):
        route_id = 1
        response = self.client.get(f"/retrieve-route?id={route_id}")
        print(f"Response status code for /retrieve-route: {response.status_code}")

    # Simulating deleting a route
    @task
    def delete_route(self):
        if self.new_route_id is not None:
            data = {"id": self.new_route_id}
            response = self.client.post("/delete-route", json=data)
            print(f"Response status code for /delete-route: {response.status_code}")
        else:
            print("No route ID available to delete.")

    # Simulating getting the XML representation of a route
    @task
    def retrieve_xml(self):
        route_id = 1
        response = self.client.get(f"/retrieve-xml?id={route_id}")
        print(f"Response status code for /retrieve-xml: {response.status_code}")

    # Simulating getting the JSON representation of a route
    @task
    def retrieve_json(self):
        route_id = 1
        response = self.client.get(f"/retrieve-json?id={route_id}")
        print(f"Response status code for /retrieve-json: {response.status_code}")
