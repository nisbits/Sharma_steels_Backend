from rest_framework import serializers
from .models import CartItem
from products.models import ExtraCharge
from .models import OrderSummaryItem, OrderSummary
from products.serializers import ProductListingSerializer
class CartItemSerializer(serializers.ModelSerializer):
    product_details=ProductListingSerializer(source='product', read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product_details', 'quantity', 'price', 'total_price']




from rest_framework import serializers

class ExtraChargeBreakdownSerializer(serializers.ModelSerializer):
    # Serializes the extra charge name and amount, with quantity adjustment
    total_amount_for_quantity = serializers.SerializerMethodField()

    class Meta:
        model = ExtraCharge
        fields = ('name', 'amount', 'total_amount_for_quantity')

    # def get_total_amount_for_quantity(self, extra_charge):
    #     # Get the quantity from the context passed to the serializer
    #     quantity = self.context.get('quantity', 1)
    #     # Calculate total amount of this charge based on the quantity
    #     if extra_charge.amount_known:
    #          return extra_charge.amount * quantity
    #     else:
    #         return "This charge will be collected at the time of delivery"
        
    def get_total_amount_for_quantity(self, extra_charge):
            # Access the parent OrderSummaryItem's quantity
            order_summary_item = self.context.get('order_summary_item')

            # If the charge is known and fixed, multiply by quantity; otherwise, provide a message
            if extra_charge.amount_known:
                return extra_charge.amount * order_summary_item.quantity
            else:
                return "This charge will be collected at the time of delivery"

class OrderSummaryItemSerializer(serializers.ModelSerializer):
    # extra_charges_breakdown = ExtraChargeBreakdownSerializer(source='extra_charges', many=True, read_only=True)
    
    base_price = serializers.SerializerMethodField()
    extra_charges_breakdown = serializers.SerializerMethodField()
    product_details=ProductListingSerializer(source='product', read_only=True)
    class Meta:
        model = OrderSummaryItem
        fields = ('product_details', 'quantity', 'price' ,'base_price', 'extra_charges_breakdown', 'total_price')
    def get_extra_charges_breakdown(self, obj):
        # Pass the current OrderSummaryItem instance in context to ExtraChargeBreakdownSerializer
        return ExtraChargeBreakdownSerializer(obj.extra_charges, many=True, context={'order_summary_item': obj}).data
    def get_base_price(self, obj):
        # quantity = self.context.get('quantity', 1)
        return obj.price * obj.quantity

class OrderSummarySerializer(serializers.ModelSerializer):
    items = OrderSummaryItemSerializer(many=True)

    class Meta:
        model = OrderSummary
        fields = ('user', 'created_at', 'total_price', 'items')