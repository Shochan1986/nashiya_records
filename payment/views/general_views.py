from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    # IsAuthenticated, 
    IsAdminUser
    )
from rest_framework.response import Response
from rest_framework import status
import stripe
from environs import Env 

env = Env() 
env.read_env()

stripe.api_key = env.str('STRIPE_API_KEY')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
    amount=1000, 
    currency='jpy', 
    payment_method_types=['card'],
    receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def save_stripe_info(request):
    data = request.data
    email = data['email']
    payment_method_id = data['payment_method_id']
    extra_msg = 'お客様の決済情報を登録しました。' 

    customer_data = stripe.Customer.list(email=email).data   

    if len(customer_data) == 0:
        customer = stripe.Customer.create(
            email=email, payment_method=payment_method_id,
            invoice_settings={
            'default_payment_method': payment_method_id
            },)
    
    else:
        customer = customer_data[0]
        extra_msg = "お客様のデータは既に存在しています."
    
    stripe.PaymentIntent.create(
        customer=customer, 
        payment_method=payment_method_id, 
        currency='jpy', 
        amount=999,
        confirm=True)   

    stripe.Subscription.create(
    customer=customer,
    items=[
        {'price': env.str("STRIPE_SUBSCRIPTION_KEY"),}
        ]
    )  
     
    return Response(status=status.HTTP_200_OK, 
      data={
        'message': 'Success', 'extra_msg': extra_msg,
        'data': { 'customer_id': customer.id }   
        }
    )