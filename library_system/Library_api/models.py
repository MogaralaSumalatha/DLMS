from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Book(models.Model):
    # Represents a book in the library, including details like title, author, publication date, and availability status.
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title

class Member(models.Model):
    # Represents a library member with basic information like name and email, along with the date they joined.
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    joined_date = models.DateField(auto_now_add=True)

    def _str_(self):
        return self.name

class BorrowingRecord(models.Model):
    # Represents a record of a book being borrowed by a member, including borrowed and returned dates.
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    def clean(self):
        # Ensure the returned_date is not before the borrowed_date
        if self.returned_date and self.returned_date < self.borrowed_date:
            raise ValidationError("Returned date cannot be before borrowed date.")

    def _str_(self):
        return f"{self.book.title} borrowed by {self.member.name}"

    def save(self, *args, **kwargs):
        # Call clean() before saving
        self.full_clean()
        super().save(*args, **kwargs)