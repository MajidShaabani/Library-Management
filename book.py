class Book:
    def __init__(self, book_id, title, author, isbn, available=True):
        self.book_id = book_id
        
        # Apply length limitations
        if len(title) > 100:
            title = title[:100]
        self.title = title
        
        if len(author) > 50:
            author = author[:50]
        self.author = author
        
        self.isbn = isbn
        self.available = available
    
    def display_info(self):
        """Returns formatted book information for display"""
        return f" ID: {self.book_id}\n Title: {self.title}\n Author: {self.author}\n" \
               f" ISBN: {self.isbn}\n Status: {'Available' if self.available else 'Not Available'}"
    
    def update_availability(self, is_available):
        """Update book availability status"""
        self.available = is_available
    
    def to_dict(self):
        """Convert book object to dictionary for serialization"""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a book object from dictionary data"""
        return cls(**data)
