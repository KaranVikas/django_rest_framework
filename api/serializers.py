from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
  # apply field value validation on serialsers
  class Meta:
    model = Product
    fields = (
      'id',
      'name',
      'price',
      'stock',
    )

  def validata_price(self,value):
    if value <=0:
      raise serializers.ValidationError("Price must be greater than 0")
    return

class OrderItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = OrderItem
    fields = (
      'order',
      'product',
      'quantity'
    )

class OrderSerializer(serializers.ModelSerializer):
  #  means we are returning the items not on read requests
  items = OrderItemSerializer(many=True, read_only=True)
  class Meta:
    model = Order
    fields = (
      'order_id',
      'created_at',
      'user',
      'status',
      'items'
    )


