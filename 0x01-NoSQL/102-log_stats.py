#!/usr/bin/env python3
"""This script provides statistics about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_stats():
    """Provides statistics about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count the number of documents in the collection
    total_logs = collection.count_documents({})

    # Count number of documents by method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = collection.count_documents({"method": method})

    # Count number of documents with method = GET and path=/status
    status_check = collection.count_documents(
        {"method": "GET", "path": "/status"})

    # Find the top 10 most present IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Print the results
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")

    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    log_stats()
