#!/usr/bin/env python3
"""This module contains a function that update a document in a collection
"""
from pymongo import MongoClient
import pymongo


def display():
    """update a document into a collection"""
    client = MongoClient()
    collection = client.logs.nginx

    # Defining the conditions
    conditions = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    values = []
    # Create pipeline and their match condition
    for condition in conditions:
        pipeline = [
            {
                "$match": {"method": condition},
                },
            {
                "$count": f"occurrences"
            }]
        result = list(collection.aggregate(pipeline))
        data = result[0][f"occurrences"] if result else 0
        values.append(data)

    # Create a pipeline for grouping ips
    newdata = collection.aggregate([
      {
          "$group": {
              "_id": "$ip",
              "count_me": {"$sum": 1}
              }
      },
      {
          "$project": {
              "_id": 0,
              "ip": "$_id",
              "count_me": 1
          }
      },
      {
          "$sort": {
              "count_me": pymongo.DESCENDING,
          }
      }
    ])

    stat = len(list(collection.find({"path": "/status"})))
    print(f'{len(list(collection.find()))} logs')
    print("Methods:")
    for idx, cond in enumerate(conditions):
        print(f'\tmethod {cond}: {values[idx]}')

    print(f"{stat} status check")

    # display top 10 ips
    print("IPs:")
    newdata = list(newdata)
    for dat in range(min(10, len(newdata))):
        print(f'\t{newdata[dat]["ip"]}: {newdata[dat]["count_me"]}')


if __name__ == '__main__':
    display()
