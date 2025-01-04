# import razorpay
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# import razorpay
# from django.conf import settings
# from django.http import JsonResponse
# from .models import Payment

# client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# def create_order(request):
#     if request.method == "POST":
#         amount = int(request.POST.get('amount')) * 100  # Convert to paise
#         user = request.user

#         # Create Razorpay order
#         razorpay_order = client.order.create({
#             "amount": amount,
#             "currency": "INR",
#             "payment_capture": "1",
#         })

#         # Save order details in the database
#         payment = Payment.objects.create(
#             user=user,
#             order_id=razorpay_order['id'],
#             amount=amount / 100  # Convert back to rupees
#         )

#         return JsonResponse({
#             "order_id": razorpay_order['id'],
#             "amount": amount,
#             "currency": "INR",
#             "key": settings.RAZORPAY_KEY_ID,
#         })

# from django.http import JsonResponse
# from razorpay import Client
# from django.conf import settings
# from .models import Payment

# client = Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# def verify_payment(request):
#     if request.method == "POST":
#         try:
#             # Retrieve data from the POST request
#             data = {
#                 "razorpay_order_id": request.POST.get('razorpay_order_id'),
#                 "razorpay_payment_id": request.POST.get('razorpay_payment_id'),
#                 "razorpay_signature": request.POST.get('razorpay_signature'),
#             }

#             # Verify payment signature
#             client.utility.verify_payment_signature(data)

#             # Update payment status in the database
#             payment = Payment.objects.get(order_id=data['razorpay_order_id'])
#             payment.payment_id = data['razorpay_payment_id']
#             payment.status = "SUCCESS"
#             payment.save()

#             return JsonResponse({"status": "success"})

#         except Payment.DoesNotExist:
#             return JsonResponse({"status": "failure", "error": "Payment record not found"})

#         except Exception as e:
#             # Handle invalid signature or other errors
#             return JsonResponse({"status": "failure", "error": str(e)})


import razorpay
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from order.models import Order

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
def verify_payment(request):
    try:
        # Extract data from request
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_signature = request.data.get("razorpay_signature")

        # Verify the payment signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            return Response({"error": "Invalid payment signature."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the related order
        order = Order.objects.get(razorpay_tracking_id=razorpay_order_id)
        payment = Payment.objects.get(order=order, razorpay_order_id=razorpay_order_id, user=request.user)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = "successful"
        # Save payment details in the database
        payment.save()

        # Update order status
        # order.status = "successful"
        # order.save()

        return Response({"success": "Payment verified and saved successfully."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
