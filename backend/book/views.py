import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django.utils.timezone import now
from .models import Book, Category
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
    """Create book view"""
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取请求数据
        title = request.POST.get('title')
        author = request.POST.get('author')
        cover = request.FILES.get('cover')  # 获取上传的文件
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        categories = request.POST.getlist('categories')

        if not title or not author or not price:
            return JsonResponse({"code": 1, "msg": "Missing required parameters"})

        # 保存图书数据
        book_data = {
            'publisher': user_id,
            'title': title,
            'author': author,
            'description': description,
            'price': price,
            'status': 'available',
        }

        form = CreateBookForm(book_data)

        if form.is_valid():
            book = form.save(commit=False)
            book.publisher_id = user_id
            book.created_at = now()

            # 上传封面图片到 PicGo 服务器
            cover_url = None
            if cover:
                cover_url = upload_image_to_picgo(cover)

            if cover_url:
                book.cover_url = cover_url  # 将 PicGo 返回的 URL 存储到数据库

            book.save()

            # 处理类别
            if categories:
                category_ids = []
                for category_name in categories:
                    try:
                        category = Category.objects.get(name=category_name)
                        category_ids.append(category.id)
                    except Category.DoesNotExist:
                        category = Category.objects.create(name=category_name)
                        category_ids.append(category.id)

                book.categories.set(category_ids)

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
                    "cover_url": book.cover_url,
                }
            })
        else:
            return JsonResponse({"code": 1, "msg": f"Book creation failed: {form.errors}"})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

def upload_image_to_picgo(cover_file):
    """将文件上传到 PicGo 服务器并返回 URL"""
    try:
        # 获取用户上传文件的扩展名
        original_extension = os.path.splitext(cover_file.name)[1]  # 获取上传文件的扩展名
        if not original_extension:
            raise ValueError("Uploaded file does not have a valid extension.")

        # 创建临时文件，并确保使用正确的扩展名
        with tempfile.NamedTemporaryFile(suffix=original_extension, delete=False) as temp_file:
            for chunk in cover_file.chunks():
                temp_file.write(chunk)
            
            temp_file_path = temp_file.name  # 临时文件路径
            print(f"Uploading file from path: {temp_file_path}")

            # 构建 JSON 请求体
            data = json.dumps({'list': [temp_file_path]})  # 文件路径以 JSON 格式传递
            
            headers = {'Content-Type': 'application/json'}

            # 发送 POST 请求到 PicGo
            response = requests.post(PICGO_UPLOAD_URL, data=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                print(f"PicGo response: {result}")
                if result.get('success'):
                    return result.get('result')[0]  # 返回上传后的图片 URL
                else:
                    print(f"PicGo upload failed: {result.get('message')}")
                    return None
            else:
                print(f"HTTP Error from PicGo: {response.status_code}")
                return None

    except Exception as e:
        print(f"Error uploading file: {e}")
        return None
    finally:
        # 删除临时文件
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

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
                'created_at',
                'cover_url'
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
                    'created_at',
                    'cover_url'
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

@csrf_exempt
def search_books_view(request):
    """通过一个 query 参数模糊匹配书籍的标题或类别"""
    if request.method == 'GET':
        query = request.GET.get('query', '').strip()  # 获取查询参数

        if not query:
            return JsonResponse({"code": 1, "msg": "必须提供查询参数"})

        # 构建查询过滤条件，title 和 categories 都进行模糊匹配
        filter_args = (
            Q(title__icontains=query) | Q(categories__name__icontains=query)  # 标题和类别名模糊匹配
        )

        # 获取符合条件的书籍，预加载 categories 字段，并去重
        books = Book.objects.prefetch_related('categories') \
            .filter(filter_args) \
            .distinct()  # 去重，避免重复返回相同书籍
        # 使用 values 获取书籍数据和类别名称
        books = books.values(
            'id', 
            'title', 
            'author', 
            'price', 
            'status', 
            'cover_url',
            'created_at'
        )

        # 处理书籍数据并将类别名称添加到书籍信息中
        book_list = []
        for book in books:
            categories_names = [category.name for category in Book.objects.get(id=book['id']).categories.all()]
            book_data = book
            book_data['categories'] = categories_names  # 添加类别名称
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt
def published_books_view(request):
    """Get list of all published books by current user"""
    if request.method == 'GET':
        # Verify and refresh token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Get the user_id from the token
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token verification failed: {str(e)}"})

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

        # Process the books and include category names
        book_list = []
        for book in books:
            categories_names = [category.name for category in Book.objects.get(id=book['id']).categories.all()]
            book_data = book
            book_data['categories'] = categories_names
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})

@csrf_exempt
def sold_out_books_view(request):
    """Get sold-out books published by current user"""
    if request.method == 'GET':
        # Verify and refresh token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Get the user_id from the token
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token verification failed: {str(e)}"})

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

        # Process the books and include category names
        book_list = []
        for book in books:
            categories_names = [category.name for category in Book.objects.get(id=book['id']).categories.all()]
            book_data = book
            book_data['categories'] = categories_names
            book_list.append(book_data)

        return JsonResponse({"code": 0, "data": book_list})

    return JsonResponse({"code": 1, "msg": "Invalid request method"})


