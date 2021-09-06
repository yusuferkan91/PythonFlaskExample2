import uuid

class Books:
    def __init__(self):
        self._Id = uuid.uuid4()
        self._Name = ""
        self._Author = ""
        self._Published = 0
        self._IsTake = True
        self._BorrowList = []

    def SetName(self, name):
        self._Name = name

    def SetAuthor(self, author):
        self._Author = author

    def SetPublished(self, published):
        self._Published = published

    def SetIsTake(self, isTake):
        self._IsTake = isTake

    def SetId(self, id):
        self._Id = id
        
    def SetBorrowList(self, borrowList):
        self._BorrowList = borrowList

    def AddBorrow(self, borrower):
        self._BorrowList.append(borrower)

    def RemoveBorrow(self, borrower):
        self._BorrowList.remove(borrower)

    def GetBorrowList(self):
        return self._BorrowList

    def GetId(self):
        return self._Id

    def GetName(self):
        return self._Name

    def GetAuthor(self):
        return self._Author

    def GetPublished(self):
        return self._Published

    def GetIsTake(self):
        return self._IsTake