class Borrower:
    def __init__(self):
        self._Id = 0
        self._Name = ""
        self._Surname = ""
        self._StudentId = 0
        self._BorrowDate = 0
        self._BackDate = 0

    def SetName(self, name):
        self._Name = name
    
    def SetSurname(self, surname):
        self._Surname = surname

    def SetStudentId(self, studentId):
        self._StudentId = studentId

    def SetId(self,id):
        self._Id = id

    def SetBorrowDate(self, date):
        self._BorrowDate = date

    def SetBackDate(self, date):
        self._BackDate = date

    def GetBorrower(self):
        return {
            'borrowerId': self._Id,
            'borrowerName': self._Name,
            'borrowerSurname': self._Surname,
            'borrowerStudentId': self._StudentId,
            'borrowDate': self._BorrowDate,
            'backDate': self._BackDate
        }
    
