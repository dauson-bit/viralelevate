from django import forms

class RequestForm(forms.Form):
  name=forms.CharField(label=' Name',max_length=100)
  phone_no=forms.CharField(label='Phone No',max_length=15)
  email=forms.EmailField(label='Email')
  description=forms.CharField(label='description')
  location=forms.CharField(label='Location',max_length=100)

class CreateForm(forms.Form):
  title=forms.CharField(label=' title')
  description=forms.CharField(label='description')
  image=forms.ImageField(label='upload an image')

class PurchaseForm(forms.Form):
  name=forms.CharField(label=' name')
  phone_no=forms.CharField(label='Phone No',max_length=15)
  email=forms.EmailField(label='Email')
  order_list=forms.CharField(label='order list')
  location=forms.CharField(label='Location',max_length=100)

  