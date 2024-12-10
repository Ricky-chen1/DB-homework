from django.http import QueryDict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django.utils.timezone import now
from .models import Book, Category
from rest_framework_simplejwt.tokens import AccessToken
from utils.jwt import verify_and_refresh_token
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status

# Define Book creation form
class CreateBookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price']

@csrf_exempt
def create_book_view(request):
    """Create book view"""
    if request.method == 'POST':
        # Verify and refresh token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # Get data from the request
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        price = request.POST.get('price')
        categories = request.POST.getlist('categories')  # Get categories as list # Get categories as JSON string

        if not title or not author or not price:
            return JsonResponse({"code": 1, "msg": "Missing required parameters"})

        # Prepare book data
        book_data = {
            'publisher' : user_id,
            'title': title,
            'author': author,
            'description': description,
            'price': price,
            'status': 'available',  # Default status
        }

        # Create Book form instance and validate
        form = CreateBookForm(book_data)

        if form.is_valid():
            book = form.save(commit=False)
            book.publisher_id = user_id  # Set the publisher to the current user
            book.created_at = now()  # Set creation time

            book.save()  # Save the book instance

            # Handle categories
            if categories:
                category_ids = []
                for category_name in categories:
                    try:
                        # 查找类别名称对应的类别实例
                        category = Category.objects.get(name=category_name)
                        category_ids.append(category.id)  # 将类别 ID 加入列表
                    except Category.DoesNotExist:
                        # 如果类别不存在，则创建新的类别
                        category = Category.objects.create(name=category_name)
                        category_ids.append(category.id)

                book.categories.set(category_ids)  # Set categories for the book
            # Prepare response data, including categories
            categories_names = [category.name for category in book.categories.all()]

            return JsonResponse({
                "code": 0,
                "msg": "Book created successfully",
                "data": {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "categories": categories_names,
                    "price": str(book.price),
                    "status": book.status,
                    "created_at": book.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            })
        else:
            return JsonResponse({"code": 1, "msg": f"Book creation failed: {form.errors}"})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

@csrf_exempt
def book_list_view(request):
    """Book list view"""
    if request.method == 'GET':
        books = Book.objects.prefetch_related('categories') \
            .values(
                'id', 
                'title', 
                'author', 
                'price', 
                'status', 
                'created_at'
            )

        # 处理每本书，确保 categories 以正确的形式返回
        book_list = []
        for book in books:
            # 通过 book.categories.all() 提取类别名称
            categories_names = [category.name for category in Book.objects.get(id=book['id']).categories.all()]
            book_data = book
            book_data['categories'] = categories_names  # 只保留类别名称
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})


@csrf_exempt
def book_detail_view(request, book_id):
    """Book detail view"""
    if request.method == 'GET':
        try:
            # 使用 filter() 获取 Book，确保只获取一个
            book = Book.objects.prefetch_related('categories') \
                .values(
                    'id', 
                    'title', 
                    'author', 
                    'description', 
                    'price', 
                    'status', 
                    'created_at'
                ).filter(id=book_id).first()  # 只取第一个匹配的书籍

            if not book:
                return JsonResponse({"code": 1, "msg": "Book does not exist"})

            # 获取类别名称
            categories_names = [category.name for category in Book.objects.get(id=book['id']).categories.all()]

            # 返回书籍数据
            book_data = book
            book_data['categories'] = categories_names  # 添加类别名称

            return JsonResponse({"code": 0, "data": book_data})

        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Error: {str(e)}"})

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
