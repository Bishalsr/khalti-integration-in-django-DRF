import uuid
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# 1️⃣ Initiate Payment
class KhaltiInitiateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        amount = request.data.get("amount", 1000)  # minimum 1000 paisa
        purchase_order_id = str(uuid.uuid4())

        payload = {
            "return_url": "http://localhost:8000/api/khalti/return/",
            "website_url": "http://localhost:8000/",
            "amount": amount,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": request.data.get("purchase_order_name", "Test Product"),
            "customer_info": {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "9800000005"
            }
        }

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            settings.KHALTI_BASE_URL + "initiate/",
            json=payload,
            headers=headers
        )

        data = response.json()

        if response.status_code == 200:
            Payment.objects.create(
                purchase_order_id=purchase_order_id,
                pidx=data.get("pidx"),
                amount=amount,
                status="Initiated"
            )

        return Response(data, status=response.status_code)


# 2️⃣ Lookup / Verify Payment
class KhaltiLookupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        pidx = request.data.get("pidx")

        if not pidx:
            return Response({"error": "pidx required"}, status=400)

        headers = {
            "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            settings.KHALTI_BASE_URL + "lookup/",
            json={"pidx": pidx},
            headers=headers
        )

        data = response.json()

        try:
            payment = Payment.objects.get(pidx=pidx)
            payment.status = data.get("status", payment.status)
            payment.transaction_id = data.get("transaction_id")
            payment.save()
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        return Response(data, status=response.status_code)




@csrf_exempt
def khalti_return_view(request):
    
    return JsonResponse({
        "message": "Khalti redirected here",
        "data": request.GET
    })
