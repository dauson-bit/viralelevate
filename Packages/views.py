from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
from .forms import  OrderForm
from .models import Package, Service, Order
from django.urls import reverse
import uuid

def home(request):
  return render(request, 'home.html')


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
        # Generate transaction ID if it doesn't exist
        if not order.transaction_id:
            if not order.customer_phone or len(order.customer_phone) < 4:
                messages.error(request, 'Invalid customer phone number.')
                return redirect('home')
            import uuid
            transaction_id = f"TX-{uuid.uuid4().hex[:10].upper()}-{order.customer_phone[-4:]}"
            order.transaction_id = transaction_id
            order.save()
        payment_url = f"/payment/{order.id}/"  # This can be removed if not needed
        return render(request, 'payment_guide.html', {
            'order': order,
            'payment_url': payment_url
        })
    except Order.DoesNotExist:
        messages.error(request, 'Order not found')
        return redirect('one_time_growth')

def payment_gateway(request, order_id):
    # Step 1: Fetch the order or 404
    order = get_object_or_404(Order, id=order_id)

    # Step 2: Generate transaction ID if it doesn't exist (for both GET and POST)
    if not order.transaction_id:
        # Ensure customer_phone is present
        if not order.customer_phone or len(order.customer_phone) < 4:
            messages.error(request, 'Invalid customer phone number.')
            return redirect('home')

        # Generate transaction ID
        transaction_id = f"TX-{uuid.uuid4().hex[:10].upper()}-{order.customer_phone[-4:]}"
        order.transaction_id = transaction_id
        order.save()
        
        if request.method == 'POST':
            messages.success(request, 'Transaction ID generated successfully!')
    elif request.method == 'POST':
        messages.info(request, 'Transaction ID already exists for this order.')

    # Step 3: Render the payment page
    return render(request, 'payment_gateway.html', {
        'order': order,
        'transaction_id': order.transaction_id
    })
