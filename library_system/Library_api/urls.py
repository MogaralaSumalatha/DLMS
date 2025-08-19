from django.urls import path
from .views import BookListCreateView, BookDetailView
from .views import MemberListCreateView, MemberDetailView
from .views import BorrowingRecordListCreateView, BorrowingRecordDetailView


urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('members/', MemberListCreateView.as_view(), name='member-list-create'),
    path('members/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('borrowings/', BorrowingRecordListCreateView.as_view(), name='borrowing-list-create'),
    path('borrowings/<int:pk>/', BorrowingRecordDetailView.as_view(), name='borrowing-detail'),
]