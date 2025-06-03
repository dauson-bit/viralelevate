from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .forms import PaymentSupportForm, OrderForm
from .models import Package, Service, Order
from django.urls import reverse
from .mpesa import MpesaAPI

def home(request):
  return render(request, 'home.html')

def social_media(request):
  return render(request, 'social_media_management.html')

@csrf_exempt
def submit_payment_support(request):
    if request.method == 'POST':
        form = PaymentSupportForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid request'})

def get_package_services(request, package_id):
    """API endpoint to fetch services associated with a package"""
    try:
        package = get_object_or_404(Package, id=package_id)
        services = Service.objects.filter(packages=package)
        
        services_data = [{
            'id': service.id,
            'name': service.name,
            'description': service.description,
            'price': float(service.price),  # Convert Decimal to float for JSON serialization
            'unit': service.unit
        } for service in services]
        
        return JsonResponse({
            'status': 'success',
            'services': services_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def one_time_growth(request):
    packages = Package.objects.all()
    return render(request, 'one_time_growth.html',{"packages": packages})

@csrf_exempt
def submit_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service_id = data.get('service_id')
            customer_name = data.get('customer_name')
            customer_email = data.get('customer_email')
            customer_phone = data.get('customer_phone')
            link = data.get('link')
            quantity = data.get('quantity')
            total_price = data.get('total_price')

            # Get the service object
            service = get_object_or_404(Service, id=service_id)

            # Create the order
            order = Order.objects.create(
                service=service,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                link=link,
                quantity=quantity,
                total_price=total_price,
                status='pending'
            )

            return JsonResponse({
                'status': 'success',
                'redirect_url': f'/payment-guide/{order.id}/'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'invalid request'})

def payment_guide(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        # Generate payment URL (you'll need to implement this based on your payment gateway)
        payment_url = f"/payment/{order.id}/"  # This should be replaced with your actual payment gateway URL
        
        return render(request, 'payment_guide.html', {
            'order': order,
            'payment_url': payment_url
        })
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('one_time_growth')

def payment_gateway(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'payment_gateway.html', {
            'order': order
        })
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('home')

@csrf_exempt
def initiate_payment(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            payment_method = request.POST.get('payment_method')
            
            if payment_method == 'mpesa':
                # Initialize M-PESA API
                mpesa = MpesaAPI()
                
                # Format phone number (remove + if present and ensure it starts with 254)
                phone_number = order.customer_phone.replace('+', '')
                if phone_number.startswith('0'):
                    phone_number = '254' + phone_number[1:]
                elif not phone_number.startswith('254'):
                    phone_number = '254' + phone_number
                
                # Convert amount to integer (M-PESA expects amount in KES)
                amount = int(float(order.total_price) * 100)  # Convert to cents
                
                # Initiate STK Push
                response = mpesa.initiate_stk_push(phone_number, amount, order.id)
                
                if response['status'] == 'success':
                    # Store checkout request ID in session for status checking
                    request.session[f'mpesa_checkout_{order.id}'] = response['checkout_request_id']
                    return JsonResponse({
                        'status': 'success',
                        'message': 'M-PESA payment initiated. Please check your phone.',
                        'checkout_request_id': response['checkout_request_id']
                    })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': response['message']
                    }, status=400)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid payment method'
                }, status=400)
                
        except Order.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Order not found'
            }, status=404)
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

@csrf_exempt
def mpesa_callback(request, order_id):
    """Handle M-PESA callback after payment"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order = Order.objects.get(id=order_id)
            
            # Check if payment was successful
            if data.get('Body', {}).get('stkCallback', {}).get('ResultCode') == 0:
                # Payment successful
                order.status = 'approved'
                order.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Payment processed successfully'
                })
            else:
                # Payment failed
                order.status = 'rejected'
                order.save()
                
                return JsonResponse({
                    'status': 'error',
                    'message': 'Payment failed'
                })
                
        except Order.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Order not found'
            }, status=404)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

@csrf_exempt
def check_payment_status(request, order_id):
    """Check the status of an M-PESA payment"""
    if request.method == 'GET':
        try:
            order = Order.objects.get(id=order_id)
            checkout_request_id = request.session.get(f'mpesa_checkout_{order.id}')
            
            if checkout_request_id:
                mpesa = MpesaAPI()
                response = mpesa.check_transaction_status(checkout_request_id)
                
                if response['status'] == 'success':
                    if response['result_code'] == 0:
                        order.status = 'approved'
                        order.save()
                        return JsonResponse({
                            'status': 'success',
                            'message': 'Payment successful',
                            'order_status': 'approved'
                        })
                    else:
                        return JsonResponse({
                            'status': 'pending',
                            'message': 'Payment pending',
                            'order_status': 'pending'
                        })
                else:
                    return JsonResponse({
                        'status': 'error',
                        'message': response['message']
                    }, status=400)
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No payment initiated for this order'
                }, status=400)
                
        except Order.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Order not found'
            }, status=404)
            
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)

def order_confirmation(request, order_id):
    """Display order confirmation page after successful payment"""
    try:
        order = Order.objects.get(id=order_id)
        return render(request, 'order_confirmation.html', {
            'order': order
        })
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('home')