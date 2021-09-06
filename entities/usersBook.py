class UsersBook:
    def __init__(self):
        self._Id = 0
        self._Name = ""
        self._Author = ""
        self._Published = 0
        self._BorrowDate = 0
        self._BackDate = 0
        self._IsHave = False

    def SetName(self, name):
        self._Name = name

    def SetAuthor(self, author):
        self._Author = author

    def SetPublished(self, published):
        self._Published = published

    def SetId(self, id):
        self._Id = id

    def SetBorrowDate(self, date):
        self._BorrowDate = date

    def SetBackDate(self, date):
        self._BackDate = date

    def SetIsHave(self, isHave):
        self._IsHave = isHave
        
    def GetBorrower(self):
        return {
            'id': self._Id,
            'name': self._Name,
            'author': self._Author,
            'published': self._Published,
            'borrowDate': self._BorrowDate,
            'backDate': self._BackDate,
            'isHave': self._IsHave
        }