from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) #it will contain all field_values
        if form.is_valid():
            first_name = form.cleaned_data['first_name'] #fetch the value from the request
            last_name = form.cleaned_data['last_name']
            phone_num = form.cleaned_data['phone_num']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,phone_num=phone_num,username=username,password=password,email=email)
            user.phone_num = phone_num
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string('accounts/verify_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            }) #the content we need to send in the email     
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
                                                     
            messages.success(request, 'Registration successfully done!')
            return redirect('register')
            
    else:
        form = RegistrationForm()
    context ={
        'form': form,
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.error(request, 'Invalid login Credentials')
            return redirect('login')
    
    return render(request,'accounts/login.html')
@login_required(login_url='login')

def logout(request):
    auth.logout(request)
    messages.success(request, "You have logged out successfully")
    return redirect('login')
