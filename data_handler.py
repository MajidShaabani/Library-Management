import pandas as pd
import os
from book import Book
from member import Member

class DataHandler:
    @staticmethod
    def get_default_data_dir():
        """Return the default directory for data files"""
        # Use a 'data' directory in the current working directory
        data_dir = os.path.join(os.getcwd(), 'data')
        if not os.path.exists(data_dir):
            try:
                os.makedirs(data_dir)
            except OSError:
                # If cannot create directory, use current directory
                data_dir = os.getcwd()
        return data_dir
        
    @staticmethod
    def import_books_from_csv(filename):
        """
        Import books from a CSV file
        
        Args:
            filename: Path to the CSV file
                - Must contain columns: 'title', 'author', 'isbn'
                - Optional column: 'available' (boolean)
        """
        books = []
        try:
            # Expand user directory if path contains ~
            if '~' in filename:
                filename = os.path.expanduser(filename)
                
            if not os.path.exists(filename):
                print(f"File not found: {filename}")
                return []
                
            df = pd.read_csv(filename)
            required_columns = ['title', 'author', 'isbn']
            
            # Check if all required columns are present
            if not all(col in df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in df.columns]
                raise ValueError(f"CSV is missing required columns: {missing}")
            
            # Generate book IDs starting from max current ID + 1
            next_id = 1
            for index, row in df.iterrows():
                book = Book(
                    book_id=next_id,
                    title=row['title'],
                    author=row['author'],
                    isbn=row['isbn'],
                    available=True if 'available' not in df.columns else bool(row['available'])
                )
                books.append(book)
                next_id += 1
                
            return books
        except Exception as e:
            print(f"Error importing books: {e}")
            return []
    
    @staticmethod
    def import_members_from_csv(filename):
        """
        Import members from a CSV file
        
        Args:
            filename: Path to the CSV file
                - Must contain columns: 'name', 'contact'
        """
        members = []
        try:
            # Expand user directory if path contains ~
            if '~' in filename:
                filename = os.path.expanduser(filename)
                
            if not os.path.exists(filename):
                print(f"File not found: {filename}")
                return []
                
            df = pd.read_csv(filename)
            required_columns = ['name', 'contact']
            
            # Check if all required columns are present
            if not all(col in df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in df.columns]
                raise ValueError(f"CSV is missing required columns: {missing}")
            
            # Generate member IDs starting from max current ID + 1
            next_id = 1
            for index, row in df.iterrows():
                member = Member(
                    member_id=next_id,
                    name=row['name'],
                    contact=row['contact'],
                    borrowed_books=[]
                )
                members.append(member)
                next_id += 1
                
            return members
        except Exception as e:
            print(f"Error importing members: {e}")
            return []
    
    @staticmethod
    def export_books_to_csv(books, filename):
        """Export books to a CSV file"""
        try:
            # Expand user directory if path contains ~
            if '~' in filename:
                filename = os.path.expanduser(filename)
                
            # If no directory specified, use the default data directory
            if os.path.basename(filename) == filename:
                data_dir = DataHandler.get_default_data_dir()
                filename = os.path.join(data_dir, filename)
            
            data = []
            for book in books:
                data.append({
                    'book_id': book.book_id,
                    'title': book.title,
                    'author': book.author,
                    'isbn': book.isbn,
                    'available': book.available
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            return True
        except Exception as e:
            print(f"Error exporting books: {e}")
            return False
    
    @staticmethod
    def export_members_to_csv(members, filename):
        """Export members to a CSV file"""
        try:
            # Expand user directory if path contains ~
            if '~' in filename:
                filename = os.path.expanduser(filename)
                
            # If no directory specified, use the default data directory
            if os.path.basename(filename) == filename:
                data_dir = DataHandler.get_default_data_dir()
                filename = os.path.join(data_dir, filename)
            
            data = []
            for member in members:
                data.append({
                    'member_id': member.member_id,
                    'name': member.name,
                    'contact': member.contact,
                    'borrowed_books': ','.join(map(str, member.borrowed_books))
                })
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            return True
        except Exception as e:
            print(f"Error exporting members: {e}")
            return False
            
    @staticmethod
    def get_sample_data(size, class_type):
        """Generate sample data for performance testing"""
        import random
        import string
        
        if class_type == Book:
            items = []
            for i in range(size):
                # Generate random book data
                title = ''.join(random.choices(string.ascii_letters, k=10))
                author = ''.join(random.choices(string.ascii_letters, k=8))
                isbn = ''.join(random.choices(string.digits, k=13))
                available = random.choice([True, False])
                
                book = Book(i+1, title, author, isbn, available)
                items.append(book)
            return items
        
        elif class_type == Member:
            items = []
            for i in range(size):
                # Generate random member data
                name = ''.join(random.choices(string.ascii_letters, k=8))
                contact = ''.join(random.choices(string.digits, k=10))
                borrowed = random.sample(range(1, size//2 + 1), random.randint(0, min(5, size//10)))
                
                member = Member(i+1, name, contact, borrowed)
                items.append(member)
            return items
        
        return []
