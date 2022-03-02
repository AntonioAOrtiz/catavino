"""
App configuration
"""

###
# database configuration
TESTING = True
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/catavino_memory'
SQLALCHEMY_TRACK_MODIFICATIONS = False

###
# praetorian configuration
SECRET_KEY = "latch"
JWT_ACCESS_LIFESPAN = {"days": 30}
JWT_REFRESH_LIFESPAN = {"days": 30}

###
# gitHub OAuth config
GITHUB_CLIENT_ID = "de3719ce10145f958512"
GITHUB_CLIENT_SECRET = "ebb4e8244e0fbb4a47f4c4e519d39bbeb8e3b3b0"

###
# using environment variables
import os
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")