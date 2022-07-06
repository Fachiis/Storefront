from locust import HttpUser, task, between
from random import randint


class BrowseProducts(HttpUser):
    wait_time = between(1, 5)

    @task(2)
    def view_products(self):
        collection_id = randint(3, 6)
        self.client.get(
            f"/api/v1/store/products/?collection_id={collection_id}",
            name="/api/v1/store/products",
        )

    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(
            f"/api/v1/store/products/{product_id}/", name="/api/v1/store/products/:id"
        )

    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(
            f"/api/v1/store/carts/{self.cart_id}/items/",
            name="/api/v1/store/carts/items",
            json={
                "product_id": product_id,
                "quantity": 1,
            },
        )

    @task
    def read_homepage(self):
        self.client.get("/home/")

    # Life cycle hook: on_start which is called every time a new use starts browsing the website. Here we create a cart obj like we always do by default and save the cart id
    def on_start(self):
        response = self.client.post("/api/v1/store/carts/")
        result = response.json()
        self.cart_id = result["id"]
