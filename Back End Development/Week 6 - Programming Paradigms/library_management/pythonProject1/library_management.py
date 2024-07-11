class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self._is_checked_out = False

        def check_out(self):
            if not self._is_checked_out:
                self._is_checked_out = True
                return True
            return False

        def return_book(self):
            if self._is_checked_out:
                self._is_checked_out = False
                return True
            return False

        def is_available(self):
            return not self._is_checked_out

        def __str__(self):
            return f"{self.title} by {self.author}"
