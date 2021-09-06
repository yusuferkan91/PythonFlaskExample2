from apies.mongoApi import MongoAPI
from bson.objectid import ObjectId
from entities.users import Users
import bcrypt
import uuid

class UsersAPI:
    def __init__(self):
        data = {
            'database': 'LibraryDb',
            'collection': 'UserCollection'
        }
        self.mongo_api = MongoAPI(data)

    def GetList(self):
        return self.mongo_api.collection.find()

    def CreateUser(self, user):
        user_data ={
            '_id': user.GetId(),
            'name': user.GetName(),
            'surname': user.GetSurname(),
            'studentId': user.GetStudentId(),
            'password': user.GetPassword(),
            'books':[]
        }
        return self.mongo_api.collection.insert_one(user_data)

    def UpdateUser(self, id, user):
        id = uuid.UUID(id)
        filter = {'_id': id}
        values = {'$set': {
            'name': user.GetName(),
            'surname': user.GetSurname(),
            'studentId': user.GetStudentId(),
            'books': user.GetBooks()
        }}

        self.mongo_api.collection.update_one(filter, values)

    def DeleteUser(self, id):
        id = uuid.UUID(id)
        self.mongo_api.collection.delete_one({'_id': id})

    def Get(self, studentId, password):
        itm = self.mongo_api.collection.find_one({'studentId':studentId})
        password_check = itm['password']
        if password_check != 'admin':
            if bcrypt.checkpw(password.encode('utf-8'), password_check):
                return itm['_id']
            else:
                return None
        else:
            return "admin"

    def GetById(self, id):
        user = Users()
        itm = self.mongo_api.collection.find_one({'_id': uuid.UUID(id)})
        user.SetId(itm['_id'])
        user.SetName(itm['name'])
        user.SetSurname(itm['surname'])
        user.SetStudentId(itm['studentId'])
        user.SetBook(itm['books'])
        return user
