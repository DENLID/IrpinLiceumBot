from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://DENLID:jok674527@cluster0.6xtz3yk.mongodb.net/?retryWrites=true&w=majority")
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
