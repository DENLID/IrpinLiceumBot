from pymongo import MongoClient
import config

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users

def register(message):
    # Регестрація юзера якщо його немає в базі
    pass
