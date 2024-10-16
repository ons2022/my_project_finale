from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cart, CartItem, Order, OrderItem
from foods.models import Food

@api_view(['POST'])
def add_to_cart(request):
    user = request.user
    food_id = request.data.get('food_id')
    quantity = request.data.get('quantity', 1)
    
    cart, created = Cart.objects.get_or_create(user=user)
    food = Food.objects.get(id=food_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, food=food)
    cart_item.quantity = quantity
    cart_item.save()
    
    cart.total_price += food.price * quantity
    cart.save()
    
    return Response({'message': 'Item added to cart'})

@api_view(['POST'])
def place_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    order = Order.objects.create(user=user, total_price=cart.total_price)
    
    for cart_item in cart.items.all():
        OrderItem.objects.create(order=order, food=cart_item.food, quantity=cart_item.quantity)
    
    cart.items.clear()
    cart.total_price = 0.00
    cart.save()

    return Response({'message': 'Order placed successfully'})
