import datetime

class Transaction:
    def __init__(self, transaction_id, book_id, member_id, borrow_date=None, return_date=None, status="borrowed"):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date if borrow_date else datetime.datetime.now().ctime()
        self.return_date = return_date
        self.status = status

    def display_info(self):
        return_info = f", Return Date: {self.return_date}" if self.return_date else ""
        return f"ID: {self.transaction_id}, Book ID: {self.book_id}, Member ID: {self.member_id}, " \
               f"Borrow Date: {self.borrow_date}{return_info}, Status: {self.status}"
    
    def complete_return(self):
        self.status = "returned"
        self.return_date = datetime.datetime.now().ctime()
    
    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            transaction_id=data["transaction_id"],
            book_id=data["book_id"],
            member_id=data["member_id"],
            borrow_date=data["borrow_date"],
            return_date=data["return_date"],
            status=data["status"]
        )
    