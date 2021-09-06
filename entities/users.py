import uuid
import bcrypt

class Users:
    def __init__(self):
        self.Id = uuid.uuid4()
        self._Name = ""
        self._Surname = ""
        self._StudentId = 0
        self._Password = ""
        self._Books = []

    def AddBook(self, book):
        self._Books.append(book)

    def RemoveBook(self, book):
        self._Books.remove(book)

    def GetBooks(self):
        return self._Books

    def SetBook(self, book):
        self._Books = book

    def SetName(self, name):
        self._Name = name
    
    def SetSurname(self, surname):
        self._Surname = surname

    def SetStudentId(self, studentId):
        self._StudentId = studentId

    def SetPassword(self, password):
        self._Password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    def SetId(self,id):
        self.Id = id

    def GetId(self):
        return self.Id

    def GetName(self):
        return self._Name

    def GetSurname(self):
        return self._Surname

    def GetStudentId(self):
        return self._StudentId

    def GetPassword(self):
        return self._Password






