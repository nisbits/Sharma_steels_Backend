from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OrderSummary, Order, OrderAddresses
from django.conf import settings

import razorpay
from payments.models import Payment
from .serializers import OrderSerializer
# Initialize Razorpay client (set your keys)
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
def create_order(request):
    # try:
        # Retrieve data from request
        order_summary_id = request.data.get("order_summary_id")
        payment_method = request.data.get("payment_method")  # "online" or "cod"
        
        if not order_summary_id:
            return Response({"error": "Order summary ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch the order summary
        try:
            order_summary = OrderSummary.objects.get(id=order_summary_id, user=request.user, is_confirmed=False)
        except OrderSummary.DoesNotExist:
            return Response({"error": "Invalid or already confirmed order summary."}, status=status.HTTP_404_NOT_FOUND)
        
        # Confirm the order summary
        order_summary.is_confirmed = True
        order_summary.calculate_total_price()
        order_summary.save()

        # Ensure address exists
        if not order_summary.address:
            return Response({"error": "Address is required to create an order."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the order
        order = Order.objects.create(
            user=request.user,
            order_summary=order_summary,
            status='pending',
            total_price=order_summary.total_price,
        )

        # Save the address for the order
        address = order_summary.address
        OrderAddresses.objects.create(
            order=order,
            receiver_name=address.receiver_name,
            receiver_phone_number=address.receiver_phone_number,
            address_line_1=address.address_line_1,
            address_line_2=address.address_line_2,
            landmark=address.landmark,
            city=address.city,
            state=address.state,
            zip_code=address.zip_code,
            country=address.country,
        )
        
        # Handle payment logic
        if payment_method == "online":
            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                "amount": int(order.total_price * 100),  # Amount in paise
                "currency": "INR",
                "receipt": f"order_rcptid_{order.id}",
            })
            
            # Save Razorpay order ID in the database
            order.razorpay_tracking_id = razorpay_order["id"]
            order.save()
            
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                razorpay_order_id=razorpay_order["id"],
                amount=order.total_price,
                payment_mode="online",
                status="created"
            )
            # Return Razorpay order details
            return Response({
                "message": "Order created successfully.",
                "order_id": order.id,
                "razorpay_order_id": razorpay_order["id"], # required for payment form
                "amount": razorpay_order["amount"], # required for payment form
                "currency": razorpay_order["currency"], # required for payment form
                "RAZORPAY_KEY_ID": settings.RAZORPAY_KEY_ID,  # required for payment form
            }, status=status.HTTP_201_CREATED)

        elif payment_method == "cod":
            # Directly confirm the order with COD
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                amount=order.total_price,
                payment_mode="cod",
                status="created"  # COD payments are marked created until delivery
            )
            
            return Response({
                "message": "Order created successfully (COD).",
                "order_id": order.id,
            }, status=status.HTTP_201_CREATED)

        else:
            return Response({"error": "Invalid payment method."}, status=status.HTTP_400_BAD_REQUEST)

    # except Exception as e:
    #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_user_orders(request):
    user = request.user  # current logged-in user
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
     
     