from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from store.permissions import IsAdminOrReadOnly
from .models import Cart, CartItem, Customer, Order, Product
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CreateCartSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, UpdateCartItemSerializer, UpdateOrderSerializer
import logging
logger = logging.getLogger(__name__) 

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_context(self):
        return {'request': self.request}    

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0: #TBD--and the status is pending
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self,request, *args, **kwargs): #Overriding the create
        serializer = CreateCartSerializer(data = request.data,
                                           context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception = True)

        try:
            customer = Customer.objects.only('id').get(user_id=self.request.user.id)
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found for the current user.")

        if Cart.objects.filter(customer=customer).exists():
            raise ValidationError(detail="Customer already has a cart.")
        
        cart  = serializer.save()
        serializer = CreateCartSerializer(cart)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartSerializer
        return CartSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id} #has to be passed then only its available

    def get_queryset(self):
        user = self.request.user
        try:
            customer_id = Customer.objects.only('id').get(user_id=user.id).id
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found for the current user.")

        return Cart.objects.filter(customer_id = customer_id)
    
    
class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
   
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']) .select_related('product')
    
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):

        try:
            customer = Customer.objects.only('id').get(user_id=request.user.id).id
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found for the current user.")
                
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self,request, *args, **kwargs): #Overriding the create
        serializer = CreateOrderSerializer(data = request.data,
                                           context={'user_id': self.request.user.id})
        serializer.is_valid(raise_exception = True)
        order  = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id} #has to be passed then only its available

    def get_queryset(self):
        user = self.request.user

        try:
            customer_id = Customer.objects.only('id').get(user_id=user.id).id
        except Customer.DoesNotExist:
            raise NotFound(detail="Customer not found for the current user.")
    
        return Order.objects.filter(customer_id = customer_id)


    