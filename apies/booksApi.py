from apies.mongoApi import MongoAPI
from entities.books import Books
import bcrypt
import uuid


class BooksAPI:
    def __init__(self):
        data = {
            'database': 'LibraryDb',
            'collection': 'BookCollection'
        }
        self.mongo_api = MongoAPI(data)

    def GetList(self):
        return self.mongo_api.collection.find()

    def CreateBook(self, book):
        book_data ={
            '_id': book.GetId(),
            'name': book.GetName(),
            'author': book.GetAuthor(),
            'published': book.GetPublished(),
            'isTake': book.GetIsTake(),
            'borrowList':[]
        }
        return self.mongo_api.collection.insert_one(book_data)

    def UpdateBook(self, id, book):
        id = uuid.UUID(id)
        filter = {'_id': id}
        values = {'$set': {'name': book.GetName(),
                            'author': book.GetAuthor(),
                            'published': book.GetPublished(),
                            'isTake': book.GetIsTake(),
                            'borrowList':book.GetBorrowList()
                            }}
        return self.mongo_api.collection.update_one(filter, values)

    def DeleteBook(self, id):
        id = uuid.UUID(id)
        self.mongo_api.collection.delete_one({'_id': id})

    def GetById(self, id):
        book = Books()
        itm = self.mongo_api.collection.find_one({'_id': uuid.UUID(id)})
        book.SetId(itm['_id'])
        book.SetName(itm['name'])
        book.SetAuthor(itm['author'])
        book.SetPublished(itm['published'])
        book.SetIsTake(itm['isTake'])
        book.SetBorrowList(itm['borrowList'])
        return book
