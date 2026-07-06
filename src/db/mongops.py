"""
Mongo database connection file
"""

import pymongo
from dotenv import load_dotenv

# DB connection variables - change these as required for your local system.
load_dotenv()
 
URI = "mongodb://localhost:27017/"
DB_NAME = "toaster"

def connect():
    """
    Creates and returns a connection to the mongo db. Must be closed after use.
    """
    client = pymongo.MongoClient(URI)
    db = client[DB_NAME]
    return client, db

if __name__ == "__main__":
    client, db = connect()
    db.create_collection()
    client.close()
    print("Success")