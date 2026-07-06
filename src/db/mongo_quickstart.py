"""
Quickstart program for setting up and testing a local mongodb environment.
"""

import pymongo

# Local parameters - change these as needed
URI = "mongodb://localhost:27017/"
DB_NAME = "toaster"

if __name__ == "__main__":
    client = pymongo.MongoClient(URI)
    db = client[DB_NAME]
    db.create_collection("Players")
    db.create_collection("Toasts")
    db.create_collection("Scoresheets")
    client.close()
    print("Success")
