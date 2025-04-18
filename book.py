class Book:
    def __init__(self, book_id, title, author, isbn, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available
    
    def display_info(self):
        status = "Available" if self.available else "Not Available"
        return f" ID: {self.book_id}\n Title: {self.title}\n Author: {self.author}\n ISBN: {self.isbn}\n Status: {status}"
    
    def update_availability(self, is_available):
        self.available = is_available
        
    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            available=data["available"]
        )
