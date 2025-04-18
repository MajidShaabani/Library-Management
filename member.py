class Member:
    def __init__(self, member_id, name, contact, borrowed_books=None):
        self.member_id = member_id
        self.name = name
        self.contact = contact
        self.borrowed_books = borrowed_books if borrowed_books else []
    
    def display_info(self):
        return f" ID: {self.member_id}\n Name: {self.name}\n Contact: {self.contact}\n Books Borrowed: {len(self.borrowed_books)}"
    
    def borrow_book(self, book_id):
        if book_id not in self.borrowed_books:
            self.borrowed_books.append(book_id)
            return True
        return False
    
    def return_book(self, book_id):
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False
    
    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "contact": self.contact,
            "borrowed_books": self.borrowed_books
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            member_id=data["member_id"],
            name=data["name"],
            contact=data["contact"],
            borrowed_books=data["borrowed_books"]
        )
