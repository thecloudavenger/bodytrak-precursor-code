from decimal import Decimal
from store.models import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_vat']

    price_with_vat = serializers.SerializerMethodField(
        method_name='calculate_vat')

    def calculate_vat(self, product: Product):
        return product.unit_price * Decimal(0.1)