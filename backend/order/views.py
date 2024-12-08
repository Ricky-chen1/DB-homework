from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms import ModelForm
from django.utils.timezone import now
from order.models import Order
from book.models import Book
from rest_framework_simplejwt.tokens import AccessToken
from utils.jwt import verify_and_refresh_token

# 定义 Order 创建表单
class CreateOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['buyer', 'seller', 'book', 'price', 'status']

@method_decorator(csrf_exempt, name='dispatch')
def create_order_view(request):
    """创建订单视图"""
    if request.method == 'POST':
        # 验证并刷新 token
        try:
            token = verify_and_refresh_token(request)
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取前端请求数据
        book_id = request.POST.get('book_id')
        price = request.POST.get('price')
        seller_id = request.POST.get('seller_id')

        if not book_id or not seller_id or not price:
            return JsonResponse({"code": 1, "msg": "请求参数缺失"})

        # 确认图书是否存在
        try:
            book = Book.objects.get(id=book_id, status='available')  # 确保书籍状态可用
        except Book.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "书籍不存在或不可用"})

        # 构建包含所有字段数据的字典
        order_data = {
            'buyer': user_id,
            'seller': seller_id,
            'book': book_id,
            'price': price,
            'status': 'pending',  # 默认状态为待支付
        }

        # 创建 Order 表单实例并传入数据
        form = CreateOrderForm(order_data)

        if form.is_valid():
            # 保存订单时，先不要提交到数据库
            order = form.save(commit=False)
            order.created_at = now()  # 设置订单创建时间
            order.save()  # 保存订单实例

            # 返回成功的响应
            return JsonResponse({
                "code": 0,
                "msg": "订单创建成功",
                "data": {
                    "id": order.id,
                    "buyer_id": order.buyer_id,
                    "seller_id": order.seller_id,
                    "book_id": order.book_id,
                    "price": str(order.price),  # DecimalField 转为字符串
                    "status": order.status,
                    "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": order.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            })
        else:
            return JsonResponse({"code": 1, "msg": f"订单创建失败: {form.errors}"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


@method_decorator(csrf_exempt, name='dispatch')
def order_list_view(request):
    """订单列表视图"""
    if request.method == 'GET':
        try:
            token = verify_and_refresh_token(request)
            user_id = token.get('user_id')  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        # 获取当前用户作为买家或卖家的所有订单
        orders = Order.objects.filter(buyer_id=user_id).union(
            Order.objects.filter(seller_id=user_id)
        ).values(
            'id', 'buyer_id', 'seller_id', 'book_id', 'price', 'status', 'created_at', 'updated_at'
        )
        return JsonResponse({"code": 0, "data": list(orders)})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})


@method_decorator(csrf_exempt, name='dispatch')
def order_detail_view(request, order_id):
    """订单详情视图"""
    if request.method == 'GET':
        try:
            token = verify_and_refresh_token(request)
            user_id = token.get('user_id')  # 从 token 中获取 user_id
        except Exception as e:
            return JsonResponse({"code": 1, "msg": f"Token 验证失败: {str(e)}"})

        try:
            # 查找订单
            order = Order.objects.values(
                'id', 'buyer_id', 'seller_id', 'book_id', 'price', 'status', 'created_at', 'updated_at'
            ).get(id=order_id)

            # 确认用户是否有权限查看订单
            if order['buyer_id'] != user_id and order['seller_id'] != user_id:
                return JsonResponse({"code": 1, "msg": "无权查看该订单"})

            return JsonResponse({"code": 0, "data": order})

        except Order.DoesNotExist:
            return JsonResponse({"code": 1, "msg": "订单不存在"})

    return JsonResponse({"code": 1, "msg": "无效的请求方法"})
