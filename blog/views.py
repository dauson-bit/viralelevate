from django.shortcuts import render,redirect
from .forms import RequestForm, CreateForm, PurchaseForm
from django.conf import settings
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def request_service(request):
    form=RequestForm()
    if request.method=="POST":
        form=RequestForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            phone_no=form.cleaned_data['phone_no']
            email=form.cleaned_data['email']
            description=form.cleaned_data['description']
            location=form.cleaned_data['location']

            messages.success(request, "Ombi lako limetumwa utapokea ujumbe mfupi kwa njia ya sms")
            return redirect( 'request_service')
        else:
            form=RequestForm()
    return render(request, 'request_service.html',{'form':form})

def create_post(request):
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = request.FILES['image']
            return redirect('create_post')
    else:
        form = CreateForm()
    
    return render(request, 'create_post.html', {'form': form})

def purchase(request):
    form=PurchaseForm()
    if request.method=="POST":
        form=PurchaseForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            phone_no=form.cleaned_data['phone_no']
            email=form.cleaned_data['email']
            order_list=form.cleaned_data['order_list']
            location=form.cleaned_data['location']

            messages.success(request, "you have successfully placed your order you will receive a confirmation message via email")
            return redirect( 'purchase')
        else:
            form=PurchaseForm()
    return render(request, 'purchase.html', {'form':form})

def shop_store(request):
    return render(request, 'shop_store.html')

def about_us(request):
    return render(request, 'about_us.html')