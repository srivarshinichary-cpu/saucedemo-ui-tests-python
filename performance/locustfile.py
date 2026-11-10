"""
Light load test for the Restful-Booker practice API (built for testing practice).
Keep the load small and polite: this is a shared public service.

Run (headless, 10 users, 1 minute):
    pip install -r requirements-perf.txt
    locust -f performance/locustfile.py --headless -u 10 -r 2 -t 1m --csv=reports/locust
"""
from locust import HttpUser, between, task

BOOKING = {
    "firstname": "Ravi",
    "lastname": "Kumar",
    "totalprice": 500,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
    "additionalneeds": "Breakfast",
}


class BookerUser(HttpUser):
    host = "https://restful-booker.herokuapp.com"
    wait_time = between(1, 3)

    @task(3)
    def list_bookings(self):
        self.client.get("/booking", name="GET /booking")

    @task(2)
    def create_then_read(self):
        with self.client.post(
            "/booking", json=BOOKING, name="POST /booking", catch_response=True
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"unexpected status {resp.status_code}")
                return
            booking_id = resp.json()["bookingid"]
        self.client.get(f"/booking/{booking_id}", name="GET /booking/{id}")

    @task(1)
    def health_check(self):
        self.client.get("/ping", name="GET /ping")
