from rest_framework import serializers
from .models import Book, Member, BorrowingRecord
from django.utils import timezone
# Serializer for Book model
# Serializer for Member model
# Serializer for BorrowingRecord model

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_published_date(self, value):
        # Ensure published date is not in the future
        if value > timezone.now().date():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

    def validate_email(self, value):
        # Ensure email is lowercase and clean
        return value.lower()

class BorrowingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingRecord
        fields = '__all__'

    def validate(self, data):
        # Ensure returned_date is not before borrowed_date
        borrowed_date = data.get('borrowed_date', None)
        returned_date = data.get('returned_date', None)

        # borrowed_date will be auto_now_add, but check if provided manually (admin/API override)
        if returned_date and borrowed_date and returned_date < borrowed_date:
            raise serializers.ValidationError("Returned date cannot be before borrowed date.")

        return data

    def create(self, validated_data):
        # Set book availability to False when borrowed
        book = validated_data['book']
        if not book.is_available:
            raise serializers.ValidationError("This book is currently unavailable.")

        book.is_available = False
        book.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # When a book is returned, set its availability to True
        returned_date = validated_data.get('returned_date', None)
        if returned_date and not instance.returned_date:
            book = instance.book
            book.is_available = True
            book.save()
        return super().update(instance, validated_data)