from django.shortcuts import redirect, render
from django.http import HttpResponse

# Home view (the landing page after login)
def home(request):
    return render(request, 'wordle/home.html')  # Render home template

# Login view
def login_view(request):
    if request.method == 'POST':
        # Simple login logic: If username and password are correct
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'user' and password == 'password':
            return render(request, 'wordle/wordle_game.html')  # Redirect to the Wordle game page
        else:
            return 0

    return render(request, 'wordle/login.html')  # Show login form

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Add logic here to save the user to the database (e.g., using Django's User model)
        return redirect('login')  # Redirect to the login page

    return render(request, 'wordle/register.html')

# Logout view
def logout_view(request):
    return redirect('/')

# Wordle game view
def wordle_game(request):
    return render(request, 'wordle/wordle_game.html')  # Render Wordle game page
