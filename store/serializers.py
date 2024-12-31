from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_vat']

    price_with_vat = serializers.SerializerMethodField(
        method_name='calculate_vat')

    def calculate_vat(self, product: Product):
        return product.unit_price * Decimal(0.1)

class SimplerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimplerProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class CreateCartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def save(self, **kwargs): #Overriding the Save
        with transaction.atomic():
            customer_id = Customer.objects.only('id').get(user_id=self.context['user_id']) #TBD Check if exists 
            cart = Cart.objects.create(customer=customer_id)
            return cart
        
    class Meta:
        model = Cart
        fields = ['id']

class CartSerializer(serializers.ModelSerializer):
    total_order_price = serializers.SerializerMethodField()

    def get_total_order_price(self, items):
       return 100
    
    class Meta:
        model = Cart
        fields = ['id', 'total_order_price']  

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try: 
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only = True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date']  

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimplerProductSerializer()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    total_order_price = serializers.SerializerMethodField()

    def get_total_order_price(self, items):
       return sum([item.quantity * item.unit_price for item in items.items.all()])
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status','items','total_order_price']  

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with given cart ID.')
        
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('No items in cart.')
        return cart_id
    

    def save(self, **kwargs): #Overriding the Save
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            customer_id = Customer.objects.only('id').get(user_id=self.context['user_id']) #TBD Check if exists 
            order = Order.objects.create(customer=customer_id)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items) #used for more than one
            
            Cart.objects.filter(pk=cart_id).delete()

            return order