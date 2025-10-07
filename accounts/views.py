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
from carts.models import Cart,CartItem
from carts.views import _cart_id 
from .models import Account

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
                'domain':current_site.domain,  # <-- changed from current_site to current_site.domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            }) #the content we need to send in the email     
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()                                    
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address.')
            return redirect('/accounts/login/?command=verification&email='+email)
            
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
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) #if any item is present in the cart
                is_cart_item_exists= CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()

            except: #if there is no item
                pass

            auth.login(request, user)
            messages.success(request, 'You have logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login Credentials')
            return redirect('login')
    
    return render(request,'accounts/login.html')

@login_required(login_url='login')

def logout(request):
    auth.logout(request)
    messages.success(request, "You have logged out successfully")
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
     
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Your account is activated!")
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')    

@login_required(login_url='login')
def dashboard(request):
    current_site = get_current_site(request)
    context = {
        'domain': current_site.domain,  # <-- add this line
    }
    return render(request, 'accounts/dashboard.html', context)

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']  
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subject = "Reset your Password"
            message = render_to_string('accounts/reset_email.html',{
                'user':user,
                'domain':current_site.domain,  # <-- changed from current_site to current_site.domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),

            }) #the content we need to send in the email     
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()     

            messages.success(request, 'Password reset email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotpassword')
    return render(request,'accounts/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, "The link has been expired")
        return redirect('login')   
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successful!")
            return redirect('login')
        else:
            messages.error(request, 'Password does not match')
            return redirect('resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')
    
# Register
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_web(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
#     return Response(serializer.errors, status=400)

# # Login
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_web(request):
#     from django.contrib.auth import authenticate
#     from django.db.models import Q
#     from .models import Account

#     identifier = (request.data.get('username') or request.data.get('email') or '').strip()
#     password = (request.data.get('password') or '').strip()

#     if not identifier or not password:
#         return Response({'error': 'username/email and password are required'}, status=400)

#     # Resolve identifier to the custom user model's credential field (email)
#     resolved_email = None
#     try:
#         # Try to find by username first; if identifier is an email, the username filter will not match
#         user_obj = Account.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).first()
#         if user_obj:
#             resolved_email = user_obj.email
#     except Exception:
#         resolved_email = None

#     if not resolved_email:
#         return Response({'error': 'Invalid Credentials'}, status=400)

#     user = authenticate(email=resolved_email, password=password)
#     if user:
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
#     return Response({'error': 'Invalid Credentials'}, status=400)

# # Protected Route
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def profile_web(request):
#     return Response({'user': request.user.username, 'email': request.user.email})




 

    
