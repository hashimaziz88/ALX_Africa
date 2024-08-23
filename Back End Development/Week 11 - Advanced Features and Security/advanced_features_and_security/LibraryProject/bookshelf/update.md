
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
