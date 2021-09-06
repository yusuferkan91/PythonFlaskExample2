from datetime import timedelta
from flask import Flask, render_template_string, render_template, request, session, redirect, url_for
from flask_session import Session
from entities.users import Users
from entities.books import Books
from entities.usersBook import UsersBook
from entities.borrower import Borrower
from apies.usersApi import UsersAPI
from apies.booksApi import BooksAPI
import uuid
import datetime

app = Flask(__name__)
app.secret_key = 'testing'
user = Users()
user_api = UsersAPI()
book_api = BooksAPI()

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        user.SetName(request.form['name'])
        user.SetSurname(request.form['surname'])
        user.SetPassword(request.form['password'])
        user.SetStudentId(request.form['studentId'])
        
        user_api.CreateUser(user)
        session['id'] = user.GetId()
        return redirect(url_for('index'))

    return render_template('signin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['id'] = user_api.Get(request.form['studentId'], request.form['password'])
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if 'id' in session:
        session.pop('id', None)
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'id' in session and len(str(session['id']))>0:
        if session['id'] == 'admin':
            bookList = book_api.GetList()
            userList = user_api.GetList()
            return render_template('admin_index.html', bookList=bookList, userList=userList)
        else:
            bookList = book_api.GetList()
            user = user_api.GetById(str(session['id']))
            usersBookList = user.GetBooks()
            return render_template('user_index.html', bookList=bookList, usersBookList=usersBookList)
    else:
        return redirect(url_for('login'))


@app.route('/deleteUser/<string:id>', methods = ['POST','GET'])
def deleteUser(id):
    user_api.DeleteUser(id)
    return redirect('/')

@app.route('/deleteBook/<string:id>', methods = ['POST','GET'])
def deleteBook(id):
    book_api.DeleteBook(id)
    return redirect('/')

@app.route('/takeBook/<string:id>', methods = ['POST','GET'])
def takeBook(id):
    borrow_date = datetime.datetime.now().strftime('%m/%d/%Y')
    user_item, book_item, user_book, borrow = GetUserBook(str(session['id']), id)
    
    borrow.SetBorrowDate(borrow_date)
    borrow.SetBackDate(0)

    user_book.SetBorrowDate(borrow_date)
    user_book.SetBackDate(0)
    user_book.SetIsHave(True)

    user_item.AddBook(user_book.GetBorrower())
    book_item.SetIsTake(False)
    book_item.AddBorrow(borrow.GetBorrower())

    user_api.UpdateUser(str(user_item.GetId()), user_item)
    book_api.UpdateBook(id, book_item)
    return redirect('/')

@app.route('/returnBook/<string:id>', methods = ['POST','GET'])
def returnBook(id):
    back_date = datetime.datetime.now().strftime('%m/%d/%Y')
    user_item, book_item, user_book, borrow = GetUserBook(str(session['id']), id)
    
    contain_user_book = next((item for item in user_item.GetBooks() if item['id'] == book_item.GetId() and item['backDate'] == 0), None)
    contain_book_borrow = next((item for item in book_item.GetBorrowList() if item['borrowerId'] == user_item.GetId() and item['backDate'] == 0), None)

    user_book.SetBorrowDate(contain_user_book['borrowDate'])
    user_book.SetBackDate(back_date)
    user_book.SetIsHave(False)
    user_item.RemoveBook(contain_user_book)
    user_item.AddBook(user_book.GetBorrower())

    borrow.SetBorrowDate(contain_book_borrow['borrowDate'])
    borrow.SetBackDate(back_date)
    book_item.SetIsTake(True)
    book_item.RemoveBorrow(contain_book_borrow)
    book_item.AddBorrow(borrow.GetBorrower())

    user_api.UpdateUser(str(user_item.GetId()), user_item)
    book_api.UpdateBook(id, book_item)

    return redirect('/')
    
@app.route('/updateUser', methods=['POST'])
def updateUser():
    id = request.form['pk']
    namepost = request.form['name']
    value = request.form['value']
    user_item = user_api.GetById(id)
    if namepost == 'name':
        user_item.SetName(value)
    elif namepost == 'surname':
        user_item.SetSurname(value)
    elif namepost == 'studentId':
        user_item.SetStudentId(value)
    user_api.UpdateUser(id, user_item)
    return 'ok'

@app.route('/updateBook', methods=['POST'])
def updateBook():
    id = request.form['pk']
    namepost = request.form['name']
    value = request.form['value']
    book_item = book_api.GetById(id)
    if namepost == 'name':
        book_item.SetName(value)
    elif namepost == 'author':
        book_item.SetAuthor(value)
    elif namepost == 'published':
        book_item.SetPublished(value)
    book_api.UpdateBook(id, book_item)
    return 'ok'

@app.route('/addUser', methods=['GET', 'POST'])
def create_user():
    user_item = Users()
    user_item.SetName(request.form['txtname'])
    user_item.SetSurname(request.form['txtsurname'])
    user_item.SetStudentId(request.form['txtstudentId'])
    user_item.SetPassword(request.form['txtpassword'])
    user_api.CreateUser(user_item)
    return redirect('/')

@app.route('/addBook', methods=['GET', 'POST'])
def create_book():
    pDate=request.form['txtpublished'] 
    pDate = datetime.datetime(int(pDate.split("-")[0]), int(pDate.split("-")[1]), int(pDate.split("-")[2])).date().strftime("%d/%m/%Y")
    book_item = Books()
    book_item.SetName(request.form['txtname'])
    book_item.SetAuthor(request.form['txtauthor'])
    book_item.SetPublished(pDate)
    book_api.CreateBook(book_item)
    return redirect('/')

def GetUserBook(userId, bookId):
    book_item = book_api.GetById(bookId)
    user_item = user_api.GetById(userId)

    user_book = UsersBook()
    user_book.SetId(book_item.GetId())
    user_book.SetName(book_item.GetName())
    user_book.SetAuthor(book_item.GetAuthor())
    user_book.SetPublished(book_item.GetPublished())  
    
    borrow = Borrower()
    borrow.SetId(user_item.GetId())
    borrow.SetName(user_item.GetName())
    borrow.SetSurname(user_item.GetSurname())
    borrow.SetStudentId(user_item.GetStudentId())

    return user_item, book_item, user_book, borrow