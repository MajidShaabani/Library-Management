from book import Book
from member import Member
from transaction import Transaction
from utils import ( 
    save_data, load_data
)

class LibraryManagementSystem:
    def __init__(self):
        self.books_file = "books.json"
        self.members_file = "members.json"
        self.transactions_file = "transactions.json"
        
        # Load data from files
        self.books = self._load_books()
        self.members = self._load_members()
        self.transactions = self._load_transactions()
        
    def _load_books(self):
        books_data = load_data(self.books_file)
        return [Book.from_dict(book) for book in books_data]
    
    def _load_members(self):
        members_data = load_data(self.members_file)
        return [Member.from_dict(member) for member in members_data]
    
    def _load_transactions(self):
        transactions_data = load_data(self.transactions_file)
        return [Transaction.from_dict(transaction) for transaction in transactions_data]
    
    def _save_books(self):
        books_data = [book.to_dict() for book in self.books]
        save_data(books_data, self.books_file)
    
    def _save_members(self):
        members_data = [member.to_dict() for member in self.members]
        save_data(members_data, self.members_file)
    
    def _save_transactions(self):
        transactions_data = [transaction.to_dict() for transaction in self.transactions]
        save_data(transactions_data, self.transactions_file)