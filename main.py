from book import Book
from member import Member
from transaction import Transaction
from utils import (
    validate_isbn, validate_name, validate_contact, validate_integer, 
    validate_title, validate_author, get_valid_input, save_data, load_data
)
from sorting import get_sorting_algorithms, logical_and, logical_or, logical_implies
from performance import PerformanceAnalyzer
from data_handler import DataHandler
import os
import time

class LibraryManagementSystem:
    def __init__(self):
        self.books_file = "books.json"
        self.members_file = "members.json"
        self.transactions_file = "transactions.json"
        
        # Load data from files
        self.books = self._load_data(self.books_file, Book.from_dict)
        self.members = self._load_data(self.members_file, Member.from_dict)
        self.transactions = self._load_data(self.transactions_file, Transaction.from_dict)

        # Initialize sorting algorithms and performance analyzer
        self.sorting_algorithms = get_sorting_algorithms()
        self.performance_analyzer = PerformanceAnalyzer()
    
    # Simplified data loading and saving methods
    def _load_data(self, filename, from_dict_func):
        return [from_dict_func(item) for item in load_data(filename)]
    
    def _save_data(self, items, filename):
        save_data([item.to_dict() for item in items], filename)
    
    def _save_books(self):
        self._save_data(self.books, self.books_file)
    
    def _save_members(self):
        self._save_data(self.members, self.members_file)
    
    def _save_transactions(self):
        self._save_data(self.transactions, self.transactions_file)
    
    def add_book(self):
        print("\n--- Add New Book ---")
        
        title = get_valid_input(
            "Enter book title: ",
            validate_title,
            "Invalid title format. Must be between 1 and 100 characters."
        )
        
        author = get_valid_input(
            "Enter book author: ",
            validate_author,
            "Invalid author format. Use only letters, spaces, and common punctuation (length: 2-50 characters)."
        )
        
        isbn = get_valid_input(
            "Enter ISBN: ",
            validate_isbn,
            "Invalid ISBN format. Must be 10 or 13 digits."
        )
        
        book_id = 1 if not self.books else max(book.book_id for book in self.books) + 1
        self.books.append(Book(book_id, title, author, isbn))
        self._save_books()
        
        print(f"Book '{title}' added successfully with ID {book_id}!")
    
    def add_member(self):
        print("\n--- Add New Member ---")
        
        name = get_valid_input(
            "Enter member name: ",
            validate_name,
            "Invalid name format. Use only letters and spaces (length: 2-50 characters)."
        )
        
        contact = get_valid_input(
            "Enter contact (email or 10-digit phone): ",
            validate_contact,
            "Invalid contact format. Enter a valid email or 10-digit phone number."
        )
        
        member_id = 1 if not self.members else max(member.member_id for member in self.members) + 1
        self.members.append(Member(member_id, name, contact))
        self._save_members()
        
        print(f"Member '{name}' added successfully with ID {member_id}!")
    
    def list_items(self, items, header, empty_message):
        print(f"\n--- {header} ---")
        if not items:
            print(empty_message)
            return False
        
        for item in items:
            print(item.display_info())
        return True
    
    def list_books(self):
        return self.list_items(self.books, "Book List", "No books in the library.")
    
    def list_members(self):
        return self.list_items(self.members, "Member List", "No members registered.")
    
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
        
        # Get objects and perform validation
        book = next(book for book in self.books if book.book_id == book_id)
        member = next(member for member in self.members if member.member_id == member_id)
        
        if not book.available:
            print("This book is not available for borrowing.")
            return
        
        # Create transaction and update records
        transaction_id = 1 if not self.transactions else max(t.transaction_id for t in self.transactions) + 1
        self.transactions.append(Transaction(transaction_id, book_id, member_id))
        
        book.update_availability(False)
        member.borrow_book(book_id)
        
        # Save all updates
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
        
        # Display borrowed books
        print(f"\nBooks borrowed by {member.name}:")
        for book_id in member.borrowed_books:
            book = next(book for book in self.books if book.book_id == book_id)
            print(f"ID: {book.book_id}, Title: {book.title}")
        
        book_id = int(get_valid_input(
            "Enter book ID to return: ",
            lambda x: validate_integer(x) and int(x) in member.borrowed_books,
            "Invalid book ID or not borrowed by this member."
        ))
        
        # Process the return
        book = next(book for book in self.books if book.book_id == book_id)
        transaction = next((t for t in self.transactions 
                         if t.book_id == book_id and t.member_id == member_id 
                         and t.status == "borrowed"), None)
        
        if transaction:
            transaction.complete_return()
        
        book.update_availability(True)
        member.return_book(book_id)
        
        self._save_books()
        self._save_members()
        self._save_transactions()
        
        print(f"Book '{book.title}' has been returned by {member.name} successfully!")
    
    def list_transactions(self):
        self.list_items(self.transactions, "Transaction History", "No transactions recorded.")
    
    def sort_books(self):
        print("\n--- Sort Books ---")
        if not self.books:
            print("No books in the library.")
            return
        
        # Define options for sorting
        primary_key_options = {
            '1': ('book_id', 'Book ID'),
            '2': ('title', 'Title'),
            '3': ('author', 'Author'),
            '4': ('isbn', 'ISBN')
        }
        
        # Get user choices
        for key, (_, name) in primary_key_options.items():
            print(f"{key}. {name}")
        
        choice = get_valid_input(
            "Select primary sorting attribute (1-4): ",
            lambda x: x in primary_key_options,
            "Invalid choice. Please enter a number between 1 and 4."
        )
        
        primary_key = primary_key_options[choice][0]
        use_secondary = get_valid_input(
            "Use secondary sorting based on availability? (y/n): ",
            lambda x: x.lower() in ['y', 'n'],
            "Invalid choice."
        ).lower() == 'y'
        
        secondary_keys = [(logical_and, 'available', 'available')] if use_secondary else None
        
        # Select and execute sorting algorithm
        sorting_algorithm, algo_name = self._select_sorting_algorithm()
        sorted_books = self._perform_sort(self.books, sorting_algorithm, primary_key, secondary_keys, algo_name)
        
        # Display results
        print(f"\nBooks sorted by {primary_key_options[choice][1]}" + 
              (f" and availability (logical AND)" if use_secondary else ""))
        
        for book in sorted_books:
            print(book.display_info())
            print("-----")
    
    def sort_members(self):
        print("\n--- Sort Members ---")
        if not self.members:
            print("No members registered.")
            return
        
        # Define options for sorting
        primary_key_options = {
            '1': ('member_id', 'Member ID'),
            '2': ('name', 'Name'),
            '3': ('contact', 'Contact'),
            '4': ('borrowed_count', 'Number of Borrowed Books')
        }
        
        # Get user choices
        for key, (_, name) in primary_key_options.items():
            print(f"{key}. {name}")
        
        choice = get_valid_input(
            "Select primary sorting attribute (1-4): ",
            lambda x: x in primary_key_options,
            "Invalid choice. Please enter a number between 1 and 4."
        )
        
        primary_key = primary_key_options[choice][0]
        
        # Add calculated property if needed
        if primary_key == 'borrowed_count':
            for member in self.members:
                member.borrowed_count = len(member.borrowed_books)
        
        # Select and execute sorting algorithm
        sorting_algorithm, algo_name = self._select_sorting_algorithm()
        sorted_members = self._perform_sort(self.members, sorting_algorithm, primary_key, None, algo_name)
        
        # Display results
        print(f"\nMembers sorted by {primary_key_options[choice][1]}")
        
        for member in sorted_members:
            print(member.display_info())
            print("-----")
    
    def _select_sorting_algorithm(self):
        """Helper method to select a sorting algorithm"""
        print("\nSelect sorting algorithm:")
        algo_options = list(self.sorting_algorithms.items())
        
        for i, (name, _) in enumerate(algo_options, 1):
            print(f"{i}. {name}")
        
        algo_choice = int(get_valid_input(
            f"Enter your choice (1-{len(algo_options)}): ",
            lambda x: x.isdigit() and 1 <= int(x) <= len(algo_options),
            f"Invalid choice."
        ))
        
        algo_name, algo_func = algo_options[algo_choice-1]
        return algo_func, algo_name  # Return function first, then name
    
    def _perform_sort(self, items, sort_func, primary_key, secondary_keys, algo_name):
        """Helper method to perform sorting and record performance"""
        items_copy = items.copy()
        
        start_time = time.time()
        sort_func(items_copy, primary_key, secondary_keys)
        execution_time = time.time() - start_time
        
        self.performance_analyzer.analyze_algorithm(
            sort_func, items, primary_key, secondary_keys, algo_name
        )
        
        print(f"Using {algo_name} - Execution time: {execution_time:.6f} seconds")
        return items_copy
    
    def import_from_csv(self):
        print("\n--- Import Data from CSV ---")
        type_options = {'1': 'books', '2': 'members'}
        
        choice = get_valid_input(
            "What to import? (1: Books, 2: Members): ",
            lambda x: x in type_options,
            "Invalid choice."
        )
        
        data_type = type_options[choice]
        
        print("\nFile Path: Enter filename or full path (use ~ for home directory)")
        filename = input("Enter CSV filename: ")
        
        # Process the file
        if '~' in filename:
            filename = os.path.expanduser(filename)
        
        if not os.path.exists(filename):
            print(f"\nError: File '{filename}' not found.")
            return
        
        if data_type == 'books':
            self._import_books(filename)
        else:
            self._import_members(filename)
    
    def _import_books(self, filename):
        new_books = DataHandler.import_books_from_csv(filename)
        if not new_books:
            print("No books were imported. Check CSV format.")
            return
            
        # Update IDs and save
        max_id = max([book.book_id for book in self.books]) if self.books else 0
        for i, book in enumerate(new_books):
            book.book_id = max_id + i + 1
        
        self.books.extend(new_books)
        self._save_books()
        print(f"Successfully imported {len(new_books)} books from CSV.")
    
    def _import_members(self, filename):
        new_members = DataHandler.import_members_from_csv(filename)
        if not new_members:
            print("No members were imported. Check CSV format.")
            return
            
        # Update IDs and save
        max_id = max([member.member_id for member in self.members]) if self.members else 0
        for i, member in enumerate(new_members):
            member.member_id = max_id + i + 1
        
        self.members.extend(new_members)
        self._save_members()
        print(f"Successfully imported {len(new_members)} members from CSV.")
    
    def export_to_csv(self):
        print("\n--- Export Data to CSV ---")
        type_options = {'1': ('books', self.books), '2': ('members', self.members)}
        
        choice = get_valid_input(
            "What to export? (1: Books, 2: Members): ",
            lambda x: x in type_options,
            "Invalid choice."
        )
        
        data_type, data = type_options[choice]
        
        print("\nFile will be saved in the 'data' directory if no path specified.")
        filename = input("Enter output CSV filename: ")
        
        # Export the data
        export_func = getattr(DataHandler, f"export_{data_type}_to_csv")
        if export_func(data, filename):
            # Get full path for display
            if os.path.dirname(filename) == '' and '~' not in filename:
                full_path = os.path.join(DataHandler.get_default_data_dir(), filename)
            else:
                full_path = filename
            print(f"Successfully exported {len(data)} {data_type} to {full_path}")
        else:
            print(f"Failed to export {data_type}.")
    
    def analyze_sorting_performance(self):
        print("\n--- Analyze Sorting Performance ---")
        
        # Define data options
        data_options = {
            '1': (Book, 'title', 'Books'),
            '2': (Member, 'name', 'Members')
        }
        
        choice = get_valid_input(
            "Select data type (1: Books, 2: Members): ",
            lambda x: x in data_options,
            "Invalid choice."
        )
        
        class_type, primary_key, label = data_options[choice]
        
        # Configure secondary sorting for books
        secondary_keys = None
        if class_type == Book:
            if get_valid_input(
                "Include secondary sorting? (y/n): ",
                lambda x: x.lower() in ['y', 'n'],
                "Invalid choice."
            ).lower() == 'y':
                secondary_keys = [(logical_and, 'available', 'available')]
        
        # Run the performance analysis
        print(f"\nAnalyzing performance for {label} sorting...")
        self.performance_analyzer.compare_algorithms(
            self.sorting_algorithms,
            [10, 100, 500, 1000],  # Data sizes to test
            lambda size: DataHandler.get_sample_data(size, class_type),
            primary_key,
            secondary_keys
        )
        
        # Display results
        print("\nResults:")
        print(self.performance_analyzer.get_results_dataframe())
        
        print("\nTime Complexity Analysis:")
        for algo, complexity in self.performance_analyzer.get_time_complexity_analysis().items():
            print(f"- {algo}: {complexity}")
        
        viz_file = self.performance_analyzer.visualize_results()
        print(f"\nPerformance visualization saved as {viz_file}")
    
    def run(self):
        menu_options = [
            ('Add a Book', self.add_book),
            ('Add a Member', self.add_member),
            ('List all Books', self.list_books),
            ('List all Members', self.list_members),
            ('Borrow a Book', self.borrow_book),
            ('Return a Book', self.return_book),
            ('List all Transactions', self.list_transactions),
            ('Sort Books', self.sort_books),
            ('Sort Members', self.sort_members),
            ('Import from CSV', self.import_from_csv),
            ('Export to CSV', self.export_to_csv),
            ('Analyze Sorting Performance', self.analyze_sorting_performance),
            ('Exit', None)
        ]
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("\n===== Library Management System =====")
            for i, (text, _) in enumerate(menu_options, 1):
                print(f"{i}. {text}")
            
            choice = get_valid_input(
                f"\nEnter your choice (1-{len(menu_options)}): ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(menu_options),
                f"Invalid choice. Please enter a number between 1 and {len(menu_options)}."
            )
            
            choice_idx = int(choice) - 1
            if choice_idx == len(menu_options) - 1:  # Exit option
                print("\nThank you for using the Library Management System. Goodbye!")
                break
            
            menu_options[choice_idx][1]()
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    library = LibraryManagementSystem()
    library.run()

