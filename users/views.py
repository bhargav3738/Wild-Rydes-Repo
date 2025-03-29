from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .forms import UserRegistrationForm


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required #new decorator
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK", status=200)

# testing 
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to dashboard or home page
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html') 

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('login')  # Redirect to dashboard or home page
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def home_view(request):
    """
    Render the home page for authenticated users.
    Redirect to login page if the user is not authenticated.
    """
    return render(request, 'users/home.html')




def logout_view(request):
    """
    Log out the current user and redirect to the login page.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')  # Replace 'login' with the name of your login URL pattern






















class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'uuid'

class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED, headers=headers)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['uuid'] = str(user.uuid)
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
