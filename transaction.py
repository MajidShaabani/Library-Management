import datetime

class Transaction:
    def __init__(self, transaction_id, book_id, member_id, borrow_date=None, return_date=None, status="borrowed"):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date if borrow_date else datetime.datetime.now().ctime()
        self.return_date = return_date
        self.status = status

