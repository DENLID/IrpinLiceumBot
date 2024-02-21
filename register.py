from pymongo import MongoClient
import config

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users

def register(message):
    # Регестрація юзера якщо його немає в базі
    try:
        id = message.chat.id
    except:
        id = message.message.chat.id
    
    y = {
        "_id": id,
        "username": message.from_user.username,
        "airalert": "never"
    }

    is_exist = users.count_documents({"_id": id})
    
    if is_exist == 0:
        users.insert_one(y)
