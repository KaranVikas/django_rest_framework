from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
  # apply field value validation on serialsers
  class Meta:
    model = Product
    fields = (
      'description',
      'name',
      'price',
      'stock',
    )

  def validata_price(self,value):
    if value <=0:
      raise serializers.ValidationError("Price must be greater than 0")
    return

class OrderItemSerializer(serializers.ModelSerializer):
  product_name = serializers.CharField(source='product.name')
  product_price = serializers.DecimalField(source='product.price', decimal_places=2, max_digits=10)
  class Meta:
    model = OrderItem
    fields = (
      'order',
      'product_name',
      'product_price',
      'quantity',
      'item_subtotal',
    )

class OrderCreateSerializer(serializers.ModelSerializer):
  class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
      model = OrderItem
      fields = (
        'product',
        'quantity',
      )
  items = OrderItemCreateSerializer(many=True)
  user = serializers.HiddenField(
    default=serializers.CurrentUserDefault()
  )

  def create(self, validated_data):
    orderitem_data = validated_data.pop('items')
    order = Order.objects.create(**validated_data)

    for item in orderitem_data:
      OrderItem.objects.create(order=order, **item)

    return order

  class Meta:
    model = Order
    fields = (
      'user',
      'status',
      'items',
    )

class OrderSerializer(serializers.ModelSerializer):
  #  means we are returning the items not on read requests
  order_id = serializers.UUIDField(read_only=True)
  items = OrderItemSerializer(many=True, read_only=True)
  total_price = serializers.SerializerMethodField()

  def get_total_price(self, obj):
    order_items = obj.items.all()
    print("order_items", order_items)
    return sum(order_item.item_subtotal for order_item in order_items)

  class Meta:
    model = Order
    fields = (
      'order_id',
      'created_at',
      'user',
      'status',
      'items',
      'total_price'
    )

class ProductInfoSerializer(serializers.Serializer):
  #get all products , count of products, max price
  products = ProductSerializer(many=True)
  count = serializers.IntegerField()
  max_price = serializers.FloatField()




