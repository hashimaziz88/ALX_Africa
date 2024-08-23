
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
