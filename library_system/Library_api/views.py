from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from .models import Book, Member, BorrowingRecord
from .serializers import BookSerializer, MemberSerializer, BorrowingRecordSerializer
import logging, os

# Logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file_path = os.path.join(os.path.dirname(__file__), 'library_api.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# BOOK VIEWS
class BookListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            books = Book.objects.all()
            page = request.GET.get('page', 1)
            size = int(request.GET.get('size', 10))
            paginator = Paginator(books, size)
            page_obj = paginator.get_page(page)
            serializer = BookSerializer(page_obj, many=True)
            return Response({
                "count": paginator.count,
                "next": f"/api/books/?page={page_obj.next_page_number()}" if page_obj.has_next() else None,
                "previous": f"/api/books/?page={page_obj.previous_page_number()}" if page_obj.has_previous() else None,
                "results": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Book GET error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

    def post(self, request):
        try:
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Book POST error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return None

    def put(self, request, pk):
        try:
            book = self.get_object(pk)
            if not book:
                return Response({"error": "Book not found"}, status=404)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Book PUT error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

    def delete(self, request, pk):
        try:
            book = self.get_object(pk)
            if not book:
                return Response({"error": "Book not found"}, status=404)
            book.delete()
            return Response(status=204)
        except Exception as e:
            logger.error(f"Book DELETE error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

# MEMBER VIEWS
class MemberListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            members = Member.objects.all()
            page = request.GET.get('page', 1)
            size = int(request.GET.get('size', 10))
            paginator = Paginator(members, size)
            page_obj = paginator.get_page(page)
            serializer = MemberSerializer(page_obj, many=True)
            return Response({
                "count": paginator.count,
                "next": f"/api/members/?page={page_obj.next_page_number()}" if page_obj.has_next() else None,
                "previous": f"/api/members/?page={page_obj.previous_page_number()}" if page_obj.has_previous() else None,
                "results": serializer.data
            }, status=200)
        except Exception as e:
            logger.error(f"Member GET error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

    def post(self, request):
        try:
            serializer = MemberSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Member POST error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

class MemberDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            return None

    def put(self, request, pk):
        try:
            member = self.get_object(pk)
            if not member:
                return Response({"error": "Member not found"}, status=404)
            serializer = MemberSerializer(member, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Member PUT error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

    def delete(self, request, pk):
        try:
            member = self.get_object(pk)
            if not member:
                return Response({"error": "Member not found"}, status=404)
            member.delete()
            return Response(status=204)
        except Exception as e:
            logger.error(f"Member DELETE error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

# BORROWING RECORD VIEWS
class BorrowingRecordListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            records = BorrowingRecord.objects.all()
            serializer = BorrowingRecordSerializer(records, many=True)
            return Response(serializer.data, status=200)
        except Exception as e:
            logger.error(f"BorrowingRecord GET error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

    def post(self, request):
        try:
            serializer = BorrowingRecordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"BorrowingRecord POST error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

class BorrowingRecordDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            record = get_object_or_404(BorrowingRecord, pk=pk)
            serializer = BorrowingRecordSerializer(record)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"BorrowingRecord GET detail error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

    def put(self, request, pk):
        try:
            record = get_object_or_404(BorrowingRecord, pk=pk)
            serializer = BorrowingRecordSerializer(record, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"BorrowingRecord PUT error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)

    def delete(self, request, pk):
        try:
            record = get_object_or_404(BorrowingRecord, pk=pk)
            record.delete()
            return Response(status=204)
        except Exception as e:
            logger.error(f"BorrowingRecord DELETE error: {str(e)}")
            return Response({"error": "Something went wrong!"}, status=500)