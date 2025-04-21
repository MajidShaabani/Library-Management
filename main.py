from book import Book
from member import Member
from transaction import Transaction
from utils import ( 
    validate_isbn, validate_name, validate_contact, validate_integer,
    get_valid_input, save_data, load_data
)
import os


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
       
    def add_book(self):
        print("\n--- Add New Book ---")
        
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = get_valid_input(
            "Enter ISBN: ",
            validate_isbn,
            "Invalid ISBN format. Must be 10 or 13 digits."
        )
        
        book_id = 1 if not self.books else max(book.book_id for book in self.books) + 1
        new_book = Book(book_id, title, author, isbn)
        self.books.append(new_book)
        self._save_books()
        
        print(f"Book '{title}' added successfully with ID {book_id}!")
    
    def add_member(self):
        print("\n--- Add New Member ---")
        
        name = get_valid_input(
            "Enter member name: ",
            validate_name,
            "Invalid name format. Use only letters and spaces."
        )
        
        contact = get_valid_input(
            "Enter contact (email or 10-digit phone): ",
            validate_contact,
            "Invalid contact format. Enter a valid email or 10-digit phone number."
        )
        
        member_id = 1 if not self.members else max(member.member_id for member in self.members) + 1
        new_member = Member(member_id, name, contact)
        self.members.append(new_member)
        self._save_members()
        
        print(f"Member '{name}' added successfully with ID {member_id}!")
    
    def list_books(self):
        print("\n--- Book List ---")
        if not self.books:
            print("No books in the library.")
            return False
        
        for book in self.books:
            print(book.display_info())
        return True
    
    def list_members(self):
        print("\n--- Member List ---")
        if not self.members:
            print("No members registered.")
            return False
        
        for member in self.members:
            print(member.display_info())
        return True
    
    def borrow_book(self):
        print("\n--- Borrow a Book ---")
        
        if not self.list_books() or not self.list_members():
            return
        
        book_id = int(get_valid_input(
            "Enter book ID to borrow: ",
            lambda x: validate_integer(x) and any(book.book_id == int(x) for book in self.books),
            "Invalid book ID."
        ))
        
        member_id = int(get_valid_input(
            "Enter member ID: ",
            lambda x: validate_integer(x) and any(member.member_id == int(x) for member in self.members),
            "Invalid member ID."
        ))
        
        # Get the book and member objects
        book = next(book for book in self.books if book.book_id == book_id)
        member = next(member for member in self.members if member.member_id == member_id)
        
        if not book.available:
            print("This book is not available for borrowing.")
            return
        
        # Create a transaction
        transaction_id = 1 if not self.transactions else max(t.transaction_id for t in self.transactions) + 1
        transaction = Transaction(transaction_id, book_id, member_id)
        
        # Update book status and member's borrowed books
        book.update_availability(False)
        member.borrow_book(book_id)
        
        # Save the transaction and updated data
        self.transactions.append(transaction)
        self._save_books()
        self._save_members()
        self._save_transactions()
        
        print(f"Book '{book.title}' has been borrowed by {member.name} successfully!")
    
    def return_book(self):
        print("\n--- Return a Book ---")
        
        if not self.members:
            print("No members registered.")
            return
        
        member_id = int(get_valid_input(
            "Enter member ID: ",
            lambda x: validate_integer(x) and any(member.member_id == int(x) for member in self.members),
            "Invalid member ID."
        ))
        
        member = next(member for member in self.members if member.member_id == member_id)
        
        if not member.borrowed_books:
            print(f"{member.name} has no books to return.")
            return
        
        print(f"\nBooks borrowed by {member.name}:")
        for book_id in member.borrowed_books:
            book = next(book for book in self.books if book.book_id == book_id)
            print(f"ID: {book.book_id}, Title: {book.title}")
        
        book_id = int(get_valid_input(
            "Enter book ID to return: ",
            lambda x: validate_integer(x) and int(x) in member.borrowed_books,
            "Invalid book ID or not borrowed by this member."
        ))
        
        # Get the book object
        book = next(book for book in self.books if book.book_id == book_id)
        
        # Find the transaction to update
        transaction = next((t for t in self.transactions 
                          if t.book_id == book_id and t.member_id == member_id and t.status == "borrowed"), None)
        
        if transaction:
            transaction.complete_return()
        
        # Update book status and member's borrowed books
        book.update_availability(True)
        member.return_book(book_id)
        
        # Save updated data
        self._save_books()
        self._save_members()
        self._save_transactions()
        
        print(f"Book '{book.title}' has been returned by {member.name} successfully!")
    
    def list_transactions(self):
        print("\n--- Transaction History ---")
        if not self.transactions:
            print("No transactions recorded.")
            return
        
        for transaction in self.transactions:
            print(transaction.display_info())
    
    def run(self):
        menu_options = {
            '1': {'text': 'Add a Book', 'function': self.add_book},
            '2': {'text': 'Add a Member', 'function': self.add_member},
            '3': {'text': 'List all Books', 'function': self.list_books},
            '4': {'text': 'List all Members', 'function': self.list_members},
            '5': {'text': 'Borrow a Book', 'function': self.borrow_book},
            '6': {'text': 'Return a Book', 'function': self.return_book},
            '7': {'text': 'List all Transactions', 'function': self.list_transactions},
            '8': {'text': 'Exit', 'function': None}
        }
        
        while True:
            # Clear screen for better readability
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("\n===== Library Management System =====")
            for key, option in menu_options.items():
                print(f"{key}. {option['text']}")
            
            choice = get_valid_input(
                "\nEnter your choice (1-8): ",
                lambda x: x in menu_options,
                "Invalid choice. Please enter a number between 1 and 8."
            )
            
            if choice == '8':
                print("\nThank you for using the Library Management System. Goodbye!")
                break
            
            menu_options[choice]['function']()
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    library = LibraryManagementSystem()
    library.run()
