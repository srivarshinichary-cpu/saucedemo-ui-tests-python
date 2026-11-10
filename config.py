import os

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")

# Public demo credentials published on the SauceDemo login page
PASSWORD = os.getenv("SAUCE_PASSWORD", "secret_sauce")
STANDARD_USER = "standard_user"
LOCKED_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
PERFORMANCE_USER = "performance_glitch_user"
