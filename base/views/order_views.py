from rest_framework import response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import serializers, status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from base.serializers import UserSerializer, UserSerializerWithToken, OrderSerializer
from base.models import Product, Order, OrderItem, ShippingAddress

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import date, datetime


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    orderItems = data["orderItems"]

    if orderItems and len(orderItems) == 0:
        return Response(
            {"detail": "No Order Items", "status": status.HTTP_400_BAD_REQUEST}
        )
    else:
        # 1. Create order
        order = Order.objects.create(
            user=user,
            paymentMethod=data["paymentMethod"],
            taxPrice=data["taxPrice"],
            shippingPrice=data["shippingPrice"],
            totalPrice=data["totalPrice"],
        )
        # 2. Create shipping address
        shipping_address = ShippingAddress.objects.create(
            order=order,
            address=data["shippingAddress"]["address"],
            city=data["shippingAddress"]["city"],
            postalCode=data["shippingAddress"]["postalCode"],
            country=data["shippingAddress"]["country"],
        )
        # 3. Create order items and set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i["product"])
            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i["qty"],
                price=i["price"],
                image=product.image.url,
            )
            # 4. Update stock
            product.countInStock -= item.qty
            product.save()
        serializer = OrderSerializer(order, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    user = request.user
    order = Order.objects.get(_id=pk)
    try:
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response(
                {
                    "detail": "Not authorized to view this order",
                    status: status.HTTP_400_BAD_REQUEST,
                }
            )
    except:
        return Response(
            {"detail": "Order does not exist", status: status.HTTP_400_BAD_REQUEST}
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order_to_paid(request, pk):
    order = Order.objects.get(_id=pk)
    order.isPaid = True
    order.paidAt = datetime.utcnow()
    order.save()
    return Response("Order was paid")
