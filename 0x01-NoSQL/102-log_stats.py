#!/usr/bin/env python3
""" Defines a program that prints nginx stats in a mongo db """

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://localhost:27017/')
    db = client['logs']
    collection = db['nginx']
    all = [i for i in collection.find()]
    ips = collection.aggregate([{"$group": {"_id": "$ip", "num": {"$sum": 1}}},
                                {"$sort": {"num": -1}}])
    ips = [i for i in ips][:10]  # get the top 10

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(f"{len(all)} logs")
    print("Methods:")

    for i in methods:
        print("\tmethod {}: {}"
              .format(i, len([j for j in all if j["method"] == i])))

    print("{} status check".format(len(list(collection.find({"method": "GET",
                                            "path": "/status"})))))

    print("IPs:")
    for i in ips:
        print('\t{}: {}'.format(i["_id"], i["num"]))
