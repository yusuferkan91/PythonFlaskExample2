from apies.mongoApi import MongoAPI
import uuid
import random
import time
import bcrypt


'''
    This file for create sample data
'''
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y', prop)

data_user = {
    'database': 'LibraryDb',
    'collection': 'UserCollection'
}
user_api = MongoAPI(data_user)

data_book = {
    'database': 'LibraryDb',
    'collection': 'BookCollection'
}
book_api = MongoAPI(data_book)

admin_user = { '_id': 'admin', 'name': 'admin', 'studentId': '0000', 'password': 'admin'}
user_api.collection.insert_one(admin_user)

userList = []
bookList = []
for i in range(10):
    r_date = random_date('1/1/2000', '1/1/2020', random.random())
    
    passW_txt = 'UserPassword' + str(i)
    passW = bcrypt.hashpw(passW_txt.encode('utf-8'), bcrypt.gensalt())
    item_user = { '_id': uuid.uuid4(), 'name': 'UserName' + str(i), 'surname': 'UserSurname' + str(i), 'studentId': str(i), 'password': passW, 'books':[]}
    item_book = { '_id': uuid.uuid4(), 'name': 'Bookname' + str(i), 'author': 'BookAuthor' + str(i), 'published': r_date, 'isTake': True, 'borrowList':[]}
    print(item_user)
    userList.append(item_user)
    bookList.append(item_book)

user_api.collection.insert_many(userList)
book_api.collection.insert_many(bookList)