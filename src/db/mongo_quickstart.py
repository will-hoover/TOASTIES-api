"""
Quickstart program for setting up and testing a local mongodb environment.
"""

import pymongo
from datetime import datetime

# Local parameters - change these as needed
URI = "mongodb://localhost:27017/"
DB_NAME = "toaster"

if __name__ == "__main__":
    client = pymongo.MongoClient(URI)
    db = client[DB_NAME]
    db.drop_collection("Players")
    db.drop_collection("Toasts")
    db.drop_collection("Scoresheets")
    db.create_collection("Players")
    db.create_collection("Toasts")
    db.create_collection("Scoresheets")
    db["Toasts"].insert_many([
        {
            "number": 1,
            "name": "Buttered Toast",
            "date": datetime(2021, 11, 7),
            "content": "Trash",
            "live": False
        }
    ])
    client.close()
    print("Success")
