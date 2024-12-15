import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django.utils.timezone import now
from .models import Book, Category, BookCategory
from rest_framework_simplejwt.tokens import AccessToken
from utils.jwt import verify_and_refresh_token
from django.db.models import Q
import json
import os
import tempfile

PICGO_UPLOAD_URL = "http://127.0.0.1:36677/upload"

# Define Book creation form
class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price']

@csrf_exempt
def create_book_view(request):
    """Handle book creation via POST request"""
    if request.method == 'POST':
        # Validate and refresh the token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Extract user ID from the token
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token validation failed: {str(e)}"})

        # Extract data from the POST request
        title = request.POST.get('title')
        author = request.POST.get('author')
        cover = request.FILES.get('cover')  # Uploaded cover file
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        categories = request.POST.getlist('categories')

        if not title or not author or not price:
            return JsonResponse({"code": 1, "msg": "Missing required parameters"})

        # Prepare book data for creation
        book_data = {
            'publisher': user_id,
            'title': title,
            'author': author,
            'description': description,
            'price': price,
            'status': 'available',
        }

        # Validate data using the form
        form = CreateBookForm(book_data)
        if form.is_valid():
            book = form.save(commit=False)  # Create a book instance without saving
            book.publisher_id = user_id
            book.created_at = now()  # Set the creation timestamp

            # Upload cover image to PicGo server
            cover_url = None
            if cover:
                cover_url = upload_image_to_picgo(cover)

            if cover_url:
                book.cover_url = cover_url  # Save the PicGo URL

            book.save()  # Save the book instance to the database

            # Handle categories
            if categories:
                for category_name in categories:
                    category, _ = Category.objects.get_or_create(name=category_name)
                    BookCategory.objects.create(book=book, category=category)

            return JsonResponse({
                "code": 0,
                "msg": "Book created successfully",
                "data": {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "categories": categories,
                    "price": str(book.price),
                    "status": book.status,
                    "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "cover_url": book.cover_url,
                }
            })
        else:
            return JsonResponse({"code": 1, "msg": f"Book creation failed: {form.errors}"})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

def upload_image_to_picgo(cover_file):
    """Upload a file to PicGo server and return its URL"""
    try:
        # Get the original file extension
        original_extension = os.path.splitext(cover_file.name)[1]
        if not original_extension:
            raise ValueError("Uploaded file does not have a valid extension.")

        # Create a temporary file with the correct extension
        with tempfile.NamedTemporaryFile(suffix=original_extension, delete=False) as temp_file:
            for chunk in cover_file.chunks():
                temp_file.write(chunk)  # Write chunks to the temporary file
            
            temp_file_path = temp_file.name  # Path to the temporary file

            # Prepare JSON request body
            data = json.dumps({'list': [temp_file_path]})
            headers = {'Content-Type': 'application/json'}

            # Send POST request to PicGo
            response = requests.post(PICGO_UPLOAD_URL, data=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return result.get('result')[0]  # Return the uploaded image URL
                else:
                    return None
            else:
                return None

    except Exception as e:
        return None
    finally:
        # Clean up the temporary file
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@csrf_exempt
def book_list_view(request):
    """Return a list of books via GET request"""
    if request.method == 'GET':
        books = Book.objects.prefetch_related('categories') \
            .values(
                'id', 
                'title',
                'publisher_id', 
                'author', 
                'price', 
                'status', 
                'created_at',
                'cover_url'
            )

        # Build the response with category names for each book
        book_list = []
        for book in books:
            categories_names = [
                category.name for category in 
                Category.objects.filter(bookcategory__book_id=book['id'])
            ]
            book_data = book
            book_data['categories'] = categories_names  # Include category names
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

@csrf_exempt
def book_detail_view(request, book_id):
    """Return details of a single book via GET request"""
    if request.method == 'GET':
        try:
            book = Book.objects.filter(id=book_id).values(
                'id', 
                'title',
                'publisher_id',
                'author', 
                'description', 
                'price', 
                'status', 
                'created_at',
                'cover_url'
            ).first()

            if not book:
                return JsonResponse({"code": 1, "msg": "Book does not exist"})

            # Retrieve categories associated with the book
            categories_names = [
                category.name for category in 
                Category.objects.filter(bookcategory__book_id=book['id'])
            ]

            book['categories'] = categories_names

            return JsonResponse({"code": 0, "data": book})

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Error: {str(e)}"})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

@csrf_exempt
def search_books_view(request):
    """Search books by title or category name using a query parameter"""
    if request.method == 'GET':
        query = request.GET.get('query', '').strip()  # Get the search query

        if not query:
            return JsonResponse({"code": 1, "msg": "Query parameter is required"})

        # Build filter criteria for title and category name
        filter_args = (
            Q(title__icontains=query) | Q(bookcategory__category__name__icontains=query)
        )

        # Fetch matching books with related categories
        books = Book.objects.prefetch_related('categories') \
            .filter(filter_args) \
            .distinct()  # Avoid duplicate results

        # Extract book details and category names
        book_list = []
        for book in books:
            categories_names = [
                category.name for category in 
                Category.objects.filter(bookcategory__book_id=book.id)
            ]
            book_data = {
                "id": book.id,
                "title": book.title,
                "publisher_id": book.publisher_id,
                "author": book.author,
                "price": str(book.price),
                "status": book.status,
                "cover_url": book.cover_url,
                "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "categories": categories_names,
            }
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

@csrf_exempt
def published_books_view(request):
    """Get list of all published books by the current user"""
    if request.method == 'GET':
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Extract user ID from the token
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token verification failed: {str(e)}"})

        # Fetch books published by the user
        books = Book.objects.prefetch_related('categories') \
            .filter(publisher_id=user_id) \
            .values(
                'id', 
                'title', 
                'author', 
                'price', 
                'status', 
                'cover_url',
                'created_at'
            )

        # Include category names
        book_list = []
        for book in books:
            categories_names = [
                category.name for category in 
                Category.objects.filter(bookcategory__book_id=book['id'])
            ]
            book_data = book
            book_data['categories'] = categories_names
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

@csrf_exempt
def sold_out_books_view(request):
    """Get sold-out books published by the current user"""
    if request.method == 'GET':
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Extract user ID from the token
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token verification failed: {str(e)}"})

        # Fetch sold books published by the user
        books = Book.objects.prefetch_related('categories') \
            .filter(publisher_id=user_id, status='sold') \
            .values(
                'id', 
                'title', 
                'author', 
                'price', 
                'status', 
                'cover_url',
                'created_at'
            )

        # Include category names
        book_list = []
        for book in books:
            categories_names = [
                category.name for category in 
                Category.objects.filter(bookcategory__book_id=book['id'])
            ]
            book_data = book
            book_data['categories'] = categories_names
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

# 定义更新书籍的表单
class UpdateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['description']

@csrf_exempt
def update_book_view(request, book_id):
    # Verify and refresh token
    try:
        token = verify_and_refresh_token(request)
        access_token = AccessToken(token)
        user_id = access_token['user_id']  # 从 token 中获取 user_id
    except Exception as e:
        return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

    # 检查书籍是否存在
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return JsonResponse({"code": 1, "msg": "书籍不存在"}, status=404)

    # 从表单数据中获取字段
    description = request.POST.get('description')
    categories = request.POST.getlist('categories')  # 从表单获取类别列表

    # 创建表单实例并验证
    form_data = {'description': description}
    form = UpdateBookForm(form_data, instance=book)

    if form.is_valid():
        book = form.save(commit=False)
        book.save()  # 保存更新的书籍描述

        # 更新书籍类别
        if categories:
            category_objects = []
            for name in categories:
                category, _ = Category.objects.get_or_create(name=name)  # 创建或获取类别
                category_objects.append(category)

            book.categories.set(category_objects)  # 更新类别关联

        # 序列化书籍数据
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "description": book.description,
            "price": str(book.price),
            "status": book.status,
            "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "categories": [category.name for category in book.categories.all()],
            "publisher_id": user_id,
            "cover_url":book.cover_url,
        }

        return JsonResponse({"code": 0, "msg": "书籍更新成功", "data": book_data})
    else:
        return JsonResponse({"code": 1, "msg": f"表单验证失败: {form.errors}"})


@csrf_exempt
def delete_book_view(request, book_id):
    """删除书籍视图"""
    if request.method == 'DELETE':
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        try:
            # 获取书籍
            book = Book.objects.get(id=book_id)
            book.delete()  # 删除书籍
            return JsonResponse({"code": 0, "msg": "书籍删除成功","data":{
                "publisher_id":user_id,
                "book_id":book_id,
            }})
        except Book.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "书籍不存在"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

