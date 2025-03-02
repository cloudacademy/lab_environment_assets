import random
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(5, 10)

    @task
    def index_page(self):
        # Call the index page.
        response = self.client.get("/")
  
    @task
    def profile_page(self):
        # Call profile by passing index 
        # This range falls outside the index bounds and will occassionally cause an error.
        response = self.client.get(f'/{random.randint(0, 10)}')
        
        