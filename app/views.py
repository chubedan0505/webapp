from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags

from django.utils.encoding import smart_str 
from .models import Profile  
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from app.models import UserSession
import secrets
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
import uuid
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def generate_session_id():
    return str(uuid.uuid4())


def Email(request):
 if request.user.is_authenticated:
    context={}
    return render(request,'app/Email.html',context)
def homechat (request):
 if request.user.is_authenticated:
  context={}
  return render(request,'app/homechat.html',context)
 else : 
    return redirect('login')
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists. Please choose a different one.')
            elif email and User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already exists. Please choose a different one.')

            else:
                user = form.save()
                # Gửi email xác nhận, redirect, hoặc thực hiện các hành động khác ở đây
                current_site = get_current_site(request)
                mail_subject = 'Xác nhận đăng ký tài khoản'
                try:
                    message = render_to_string('app/Email.html', {
                        'user': user,
                        'domain': current_site.domain,  # Thay bằng đường dẫn xác thực thực tế
                    })
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()

                    return redirect('login')
                except Exception as e:
                    print(f"Error sending email: {e}")
                    # Log thông báo lỗi hoặc xử lý nếu có lỗi khi gửi email

    context = {'form': form}
    return render(request, 'app/register.html', context)
def logoutPage(request):
    # Tìm phiên đăng nhập hiện tại của người dùng và cập nhật thời gian logout
    try:
        user_session = UserSession.objects.get(user=request.user, logout_time__isnull=True)
        user_session.logout_time = timezone.now()
        user_session.save()
    except UserSession.DoesNotExist:
        pass

    django_logout(request)
    return redirect('login')



def loginPage(request):
    if request.user.is_authenticated: 
        return redirect('homechat')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Tạo một phiên đăng nhập mới cho người dùng
            new_session = UserSession.objects.create(user=user, session_token=generate_session_token())
            
            return redirect('homechat')  # Chuyển hướng sau khi xác thực và tạo phiên đăng nhập thành công
        else:
            messages.info(request, 'Username or password is incorrect.')

    return render(request, 'app/login.html')  # Trả về trang đăng nhập nếu xác thực không thành công
def create_user_session(user, session_token,session_id):
    
    new_session = UserSession.objects.create(user=user, session_token=session_token ,session_id=session_id)

    return new_session

# Hàm để cập nhật thông tin đăng xuất cho một phiên đăng nhập
def update_logout_time(session_id):
    try:
        session = UserSession.objects.get(session_id)
        session.logout_time = timezone.now()
        session.save()
        return True
    except UserSession.DoesNotExist:
        return False

# Hàm để lấy các phiên đăng nhập của một người dùng
def get_user_sessions(user):
    user_sessions = UserSession.objects.filter(user=user)

    return user_sessions

def generate_session_token():
    return secrets.token_hex(16) 



def send_confirmation_email(email):
    subject = 'Xác nhận đăng ký'
    message = 'Cảm ơn bạn đã đăng ký. Hãy xác nhận email của bạn.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

def send_verification_email(request):
    user = request.user  # Đây là user đã đăng ký thành công
    current_site = get_current_site(request)
    verification_link = f"http://{current_site.domain}/verify/{urlsafe_base64_encode(force_bytes(user.pk))}/"
    
    context = {
        'user': user,
        'verification_link': verification_link,
    }
    
    email_template = 'app/email_verification.html'
    email_content = render_to_string(email_template, context)
    
    # Tiếp theo, gửi email với nội dung email_content
    # Code gửi email sẽ được gọi ở đây
    
    return redirect('login')

def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        context = {'profile': profile}
        return render(request, 'app/profile.html', context)
    except Profile.DoesNotExist:
       
        messages.info(request, 'Bạn chưa có Profile. Vui lòng tạo Profile của bạn.')
        return redirect('edit')  # Chuyển hướng đến trang tạo Profile

@login_required
def edit(request):
    user = request.user

    # Kiểm tra xem người dùng đã có Profile hay chưa, nếu chưa thì tạo mới
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    if request.method == 'POST':
        # Lấy dữ liệu từ form và cập nhật Profile của người dùng
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        birthday = request.POST.get('birthday')
        image = request.FILES.get('image')
        aboutme = request.POST.get('aboutme')

        # Kiểm tra xem location có được cung cấp từ form không
        if 'location' in request.POST:
            location = request.POST.get('location')
            profile.location = location

        profile.first_name = first_name
        profile.last_name = last_name
        profile.phone = phone
        profile.birthday = birthday
        profile.image = image
        profile.aboutme = aboutme
        profile.save()

        return redirect('profile')  # Điều hướng đến trang chi tiết Profile

    context = {'profile': profile}
    return render(request, 'app/edit.html', context)