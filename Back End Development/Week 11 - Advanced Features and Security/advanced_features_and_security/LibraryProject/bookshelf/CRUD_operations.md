# Create a Book Instance

````python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)

# Expected Output
<Book: 1984>

### `retrieve.md`

```markdown
# Retrieve the Book Instance

```python
from bookshelf.models import Book

# Retrieve the book you created
book = Book.objects.get(id=1)
print(book)

# Expected Output
<Book: 1984>

### `update.md`

```markdown
# Update the Book Title

```python
from bookshelf.models import Book

# Retrieve the book you created
book = Book.objects.get(id=1)

# Update the title of the created book
book.title = "Nineteen Eighty-Four"
book.save()
print(book)

# Expected Output
<Book: Nineteen Eighty-Four>

### `delete.md`

```markdown
# Delete the Book Instance

```python
from bookshelf.models import Book

# Retrieve the book you created
book = Book.objects.get(id=1)

# Delete the book instance
book.delete()

# Try to retrieve all books again to confirm deletion
books = Book.objects.all()
print(books)

# Expected Output
[]
````
