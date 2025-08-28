from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_id', 'quantity', 'price')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'user', 'status', 'total_amount', 
                 'shipping_address', 'notes', 'items', 'created_at', 'updated_at')
        read_only_fields = ('order_number', 'user')

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ('shipping_address', 'notes', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # 1. Calculate the total_amount from items_data
        total_amount = Decimal('0.00')
        for item_data in items_data:
            # You need the price from the related product, not the validated data
            # since price is not a writeable field on OrderItemSerializer
            # You should fetch the product price from the database
            from products.models import Product  # Import here to avoid circular dependencies
            product = Product.objects.get(pk=item_data['product_id'])
            total_amount += product.price * item_data['quantity']

        # 2. Add the calculated total_amount to validated_data before creating the order
        validated_data['total_amount'] = total_amount

        # 3. Create the Order instance with all required fields
        order = Order.objects.create(**validated_data)

        # 4. Now, create the OrderItem instances
        for item_data in items_data:
            # Fetch the product again to get the correct price
            from products.models import Product
            product = Product.objects.get(pk=item_data['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,  # Set the product foreign key
                quantity=item_data['quantity'],
                price=product.price  # Use the product's price, not the request's
            )

        return order