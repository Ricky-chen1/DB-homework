# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from utils.jwt import generate_jwt_token
from django.core.mail import send_mail
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from .models import User
import random
from backend.settings import EMAIL_FROM

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        # 检查是否提供了 username 和 password
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

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

# 生成验证码的辅助函数
def generate_verification_code():
    return ''.join(random.choices('0123456789', k=6))

# 发送验证邮件视图
@csrf_exempt
def send_verification_email(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        # 检查用户名和邮箱是否提供
        if not username:
            return JsonResponse({"code": 1, "msg": "用户名不能为空"})
        if not email:
            return JsonResponse({"code": 1, "msg": "邮箱不能为空"})

        try:
            # 从数据库查询用户
            user = User.objects.get(username=username)

            # 验证邮箱是否匹配
            if user.email != email:
                return JsonResponse({"code": 1, "msg": "邮箱与用户名不匹配"})

        except ObjectDoesNotExist:
            return JsonResponse({"code": 1, "msg": "用户名不存在"})

        # 生成验证码
        verification_code = generate_verification_code()

        # 保存验证码到缓存，超时时间为 5 分钟
        cache.set(f'verification_code_{email}', verification_code, timeout=120)

        # 发送邮件
        try:
            send_mail(
                subject="密码重置验证码",  # 邮件主题
                message=f"您的验证码是：{verification_code}",  # 邮件内容
                from_email=EMAIL_FROM,  # 使用默认发件人
                recipient_list=[email],  # 收件人列表
                fail_silently=False,  # 出现错误时不忽略
            )
            return JsonResponse({"code": 0, "msg": "验证码已发送，请检查您的邮箱"})
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"code": 1, "msg": "邮件发送失败，请稍后再试"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})

# 重置密码视图
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        new_password = request.POST.get('new_password')

        if not email or not code or not new_password:
            return JsonResponse({"code": 1, "msg": "参数不完整"})

        # 验证验证码
        cached_code = cache.get(f'verification_code_{email}')
        if cached_code != code:
            return JsonResponse({"code": 1, "msg": "验证码无效或已过期"})

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return JsonResponse({"code": 0, "msg": "密码重置成功"})
        except User.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "用户不存在"})
    return JsonResponse({"code": 1, "msg": "无效的请求方法"})
