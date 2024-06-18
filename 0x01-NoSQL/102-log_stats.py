#!/usr/bin/env python3
"""
Script  that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

if __name__ == '__main__':
    """Prints the log stats in nginx collection"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx

    # number of logs
    count = logs.count_documents({})

    get = logs.count_documents({"method": "GET"})
    post = logs.count_documents({"method": "POST"})
    put = logs.count_documents({"method": "PUT"})
    patch = logs.count_documents({"method": "PATCH"})
    delete = logs.count_documents({"method": "DELETE"})

    doc = logs.count_documents({"method": "GET", "path": "/status"})

    print(
        f"{count} logs\n"
        "Methods:\n"
        f"\tmethod GET: {get}\n"
        f"\tmethod POST: {post}\n"
        f"\tmethod PUT: {put}\n"
        f"\tmethod PATCH: {patch}\n"
        f"\tmethod DELETE: {delete}\n"
        f"{doc} status check"
    )

    print("IPs:")
    # get top ten most common IPs
    top_ten_ips = [
        log for log in logs.aggregate(
            [
                {
                    "$group": {
                        "_id": "$ip",
                        "count": {"$sum": 1}
                    }
                },
                {
                    "$sort": {"count": -1}
                },
                {
                    "$limit": 10
                }
            ]
        )
    ]

    for value in top_ten_ips:
        ip = value["_id"]
        count = value["count"]
        print(f"\t{ip}: {count}")
