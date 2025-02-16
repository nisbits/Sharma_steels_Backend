from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import ContactInfo, ContactMessage
from .serializers import ContactInfoSerializer, ContactMessageSerializer

@api_view(["GET"])
def get_contact_info(request):
    """Returns business contact details for display on the 'Contact Us' page."""
    contact = ContactInfo.objects.first()  # Assuming only one record exists
    if not contact:
        return Response({"error": "No contact info found"}, status=404)
    return Response(ContactInfoSerializer(contact).data)

@api_view(["POST"])
def post_contact_message(request):
    """Handles user-submitted messages from the Contact Us form."""
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Your message has been sent successfully!"}, status=201)
    return Response(serializer.errors, status=400)
