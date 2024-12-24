from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Product

@api_view(['POST'])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    print(user)
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=user)

    # Get the product
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if item already exists in cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        # If the item already exists, update quantity
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.price = product.selling_price  # Set the product's price at the time of adding to cart
        
    cart_item.total_price = cart_item.price * cart_item.quantity
    cart_item.save()
   

    return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)




from django.http import JsonResponse
from .models import Cart, CartItem
from .serializers import CartItemSerializer
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def cart_items_view(request):
    try:
        # Get the current user's cart
        cart = Cart.objects.get(user=request.user)

        # Get all items in the cart
        cart_items = CartItem.objects.filter(cart=cart)

        # Serialize the cart items
        serializer = CartItemSerializer(cart_items, many=True)

        # Return the serialized cart items
        return JsonResponse({"cart_items": serializer.data}, status=status.HTTP_200_OK, safe=False)

    except Cart.DoesNotExist:
        return JsonResponse({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer

@api_view(['POST'])
def update_cart_item_quantity(request):
    cart_item_id = request.data.get('cart_item_id')
    new_quantity = request.data.get('quantity')

    try:
         cart_item = CartItem.objects.get(id=cart_item_id)
         if int(new_quantity) == 0:
            # If quantity is zero, delete the item
            cart_item.delete()
            return Response({"message": "Cart item deleted as quantity is zero"}, status=status.HTTP_200_OK)
         
         else:
            # Fetch the cart item by its ID
           

            # Update the quantity
            cart_item.quantity = int(new_quantity)

            # Save the cart item (triggers total price recalculation in the save method if defined)
            cart_item.save()

            # Serialize the updated cart item and return the response
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_200_OK)

    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import CartItem

@api_view(['DELETE'])
def delete_cart_item(request):
    cart_item_id = request.data.get('cart_item_id')

    try:
        # Fetch the cart item by its ID
        cart_item = CartItem.objects.get(id=cart_item_id)

        # Delete the cart item
        cart_item.delete()

        return Response({"message": "Cart item deleted successfully"}, status=status.HTTP_200_OK)

    except CartItem.DoesNotExist:
        return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_cart_subtotal(request):
    cart = Cart.objects.get(user=request.user)
    subtotal = sum(item.total_price for item in cart.items.all())
    return Response({"subtotal": subtotal}, status=status.HTTP_200_OK)



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CartItem, OrderSummary, OrderSummaryItem, ExtraCharge
from .serializers import OrderSummarySerializer

from User_account.models import Address
@api_view(['POST'])
def create_order_summary(request):
    user = request.user  # Get the logged-in user
    cart_items = CartItem.objects.filter(cart__user=user)  # Fetch the user's cart items
    address_id = request.data.get('address_id')

    try:
         address_obj = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
    # Check if the cart is empty
    if not cart_items.exists():
        return Response({"error": "No items in the cart"}, status=status.HTTP_400_BAD_REQUEST)

    # Create Order Summary
    order_summary = OrderSummary.objects.create(user=user, address=address_obj)

    for cart_item in cart_items:
        # Create OrderSummaryItem for each cart item
        order_summary_item = OrderSummaryItem.objects.create(
            order_summary=order_summary,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.mrp

        )

        # Associate all extra charges for this item
        extra_charges = ExtraCharge.objects.filter(Product=cart_item.product)
        order_summary_item.extra_charges.set(extra_charges)
        order_summary_item.calculate_total_price()

    # Recalculate the total price of the order summary
    order_summary.calculate_total_price()

    # Serialize the data and include quantity for each item in the context
    order_summary_serializer = OrderSummarySerializer(
        order_summary,
        context={'quantity': cart_item.quantity}
    )
    return Response(order_summary_serializer.data, status=status.HTTP_201_CREATED)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, OrderSummary, OrderSummaryItem, ExtraCharge
from .serializers import OrderSummarySerializer

@api_view(['POST'])
def buy_now(request):
    user = request.user
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)
    
    address_id = request.data.get('address_id')

    try:
         address_obj = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    # Create a new OrderSummary
    order_summary = OrderSummary.objects.create(user=user, address=address_obj)

    # Create OrderSummaryItem
    order_summary_item = OrderSummaryItem.objects.create(
        order_summary=order_summary,
        product=product,
        quantity=quantity,
        price=product.selling_price  # Assuming `selling_price` is the effective price
    )

    # Add extra charges
    extra_charges = ExtraCharge.objects.filter(Product=product)
    order_summary_item.extra_charges.set(extra_charges)
    order_summary_item.calculate_total_price()

    # Calculate the total price of the order summary
    order_summary.calculate_total_price()

    # Serialize and return the order summary data
    order_summary_serializer = OrderSummarySerializer(order_summary)
    return Response(order_summary_serializer.data, status=status.HTTP_201_CREATED)