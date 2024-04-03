from django.shortcuts import render
from account.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import razorpay
# Create your views here.
class create_payment_order(APIView):
    def post(self, request, format=None):
        context = {}
        skey='rzp_live_iz6Zo5rYZvS5hw'
        scrt='1G167WSywSWzWiHqKPu72BXb'
        print("INSIDE Create Order!!!",skey,scrt)
        client = razorpay.Client(auth=(skey, scrt))
        phone = request.data.get('phone')
        amount=request.data.get('amount')
        order_amount=int(amount)*100
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        notes = {
            'Shipping address': 'SSTPL sodala, Jaipur'}

        # CREAING ORDER
        response = client.order.create(dict(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes, payment_capture='0'))
        order_id = response['id']
        order_status = response['status']
        print(response,'dddddddddddddddd')
        if order_status=='created':

            # Server data for user convinience
            context['price'] = amount
            context['phone'] = phone
            context['skeyvalue']=skey
            context['ssec']=scrt
            context['order_id'] = order_id
            print(context,'order_status')
            return Response(context,status=status.HTTP_200_OK)        
        else:
            return Response({'error':'Error in  create order'}, status=status.HTTP_400_BAD_REQUEST)
        

# class order_check(APIView):
#     def post(self, request, format=None): 
#         print(request.data)
#         razorpay_order_id = request.data.get('order_id')    
#         razorpay_payment_id = request.data.get('payment_id')    
#         razorpay_signature = request.data.get('signature')    
#         print(razorpay_order_id)
#         print(razorpay_payment_id)
#         print(razorpay_signature)
#         skey='rzp_live_iz6Zo5rYZvS5hw'
#         scrt='1G167WSywSWzWiHqKPu72BXb'
#         print("INSIDE Create Order!!!",skey,scrt)
#         client = razorpay.Client(auth=(skey, scrt))

#         try:
#             client.utility.verify_payment_signature({
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': razorpay_payment_id,
#                 'razorpay_signature': razorpay_signature
#             })
#             print("SUCCESSsfggggggggggggggg")
#         except SignatureVerificationError as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#         # Handle other exceptions if necessary

#         # If no exceptions occurred, return a success response
#         return Response({'message': 'Payment verification successful'}, status=status.HTTP_200_OK)
        
            

 