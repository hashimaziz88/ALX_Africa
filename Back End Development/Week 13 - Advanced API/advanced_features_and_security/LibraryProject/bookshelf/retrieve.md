
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
