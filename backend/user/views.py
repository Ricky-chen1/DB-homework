# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import User
from utils.jwt import generate_jwt_token

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        # 检查是否提供了 username 和 password
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({"code": 1, "msg": "用户名和密码不能为空！"})

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()  # 保存表单数据到数据库
            return JsonResponse({"code": 0, "msg": "success"})
        else:
            return JsonResponse({"code": 1, "msg": f"注册失败: {form.errors}"})
    
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


# 登录视图
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({"code": 1, "msg": "用户名和密码不能为空"})

        # 使用 authenticate 函数验证用户名和密码
        user = authenticate(request, username=username, password=password)
        
        # Debugging: Check if user is None and print additional information
        if user is None:
            print(f"Authentication failed for username: {username}")
            try:
                user_obj = User.objects.get(username=username)
                print(f"User found in database: {user_obj}")
            except User.DoesNotExist:
                print("User does not exist in the database.")
        
        if user is not None:
            login(request, user)  # 登录用户
            token = generate_jwt_token(user)
            return JsonResponse({
                "code": 0,
                "msg": "登录成功",
                "token": token
            })
        else:
            return JsonResponse({"code": 1, "msg": "用户名或密码错误"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

@csrf_exempt
def get_user_name(request, user_id):
    try:
        # 查询数据库获取用户
        user = User.objects.get(id=user_id)
        return JsonResponse({"code": 0, "msg": "success", "username": user.username})
    except User.DoesNotExist:
        return JsonResponse({"code": 1, "msg": "用户不存在"})