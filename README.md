# Library Management System

A comprehensive Python application for managing library operations including books, members, and transactions with advanced sorting algorithms and performance analysis.

## Overview

This Library Management System (LMS) is designed to help librarians efficiently manage book inventory, member records, and lending operations. It features a command-line interface with support for data persistence, CSV import/export, and various sorting algorithms with performance analysis.

## Features

- **Book Management**: Add, list, and track availability of books
- **Member Management**: Register members and manage their borrowed books
- **Transaction Handling**: Process book borrowing and returns
- **Sorting Capabilities**: Sort books and members with different algorithms
- **Data Import/Export**: Import and export data in CSV format
- **Performance Analysis**: Compare and visualize sorting algorithm performance

## Requirements

- Python 3.6+
- pandas
- matplotlib
- numpy

## Installation

1. Clone the repository
2. Install required packages:
```
pip install pandas matplotlib numpy
```

## Usage

Run the application by executing the main script:
```
python main.py
```

The system presents a menu-driven interface with the following options:
1. Add a Book
2. Add a Member
3. List all Books
4. List all Members
5. Borrow a Book
6. Return a Book
7. List all Transactions
8. Sort Books
9. Sort Members
10. Import from CSV
11. Export to CSV
12. Analyze Sorting Performance
13. Exit

## File Structure

- book.py: Book class definition
- member.py: Member class definition
- transaction.py: Transaction class for managing borrowing/returns
- main.py: Main application with UI
- data_handler.py: CSV import/export functionality
- sorting.py: Sorting algorithms implementation
- performance.py: Performance analysis tools
- utils.py: Utility functions for validation

## Data Files

- Random_Books_List.csv: Sample book data
- Library_Members_List.csv: Sample member data

## CSV Format

### Books CSV Format
```
book_id,title,author,isbn,available
```

### Members CSV Format
```
member_id,name,contact,borrowed_books
```

## Features in Detail

### Sorting Algorithms
The system implements multiple sorting algorithms:
- Insertion Sort (loop-based)
- Merge Sort (recursive)

Both algorithms support secondary sorting keys with logical operations.

### Performance Analysis
The system can analyze and compare the performance of different sorting algorithms with varying data sizes, generating both statistics and visualizations.

## Data Persistence
Book, member, and transaction data is saved in JSON format for persistence between sessions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
