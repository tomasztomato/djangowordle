import json
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    return render(request, 'wordle/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

            if check_password(password, user.password):
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'wordle/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')

def home_view(request):
    return render(request, 'wordle/home.html')



def load_words():
    with open('wordle/words.json', 'r') as f:
        data = json.load(f)
        return data['words']



@login_required
def game_view(request):
    word_list = load_words()

    if 'refresh_game' in request.POST:
        del request.session['secret_word']
        request.session['guess_history'] = []
        return redirect('/wordle')  # Redirect after handling refresh

    if 'secret_word' not in request.session:
        request.session['secret_word'] = random.choice(word_list)

    SECRET_WORD = request.session['secret_word']
    guessed_word = None
    result = None
    guess_history = request.session.get('guess_history', [])

    if request.method == 'POST' and 'submit_guess' in request.POST:
        guess = request.POST.get('guess', '').lower()

        if len(guess) == 5:
            if guess == SECRET_WORD:
                guessed_word = guess
                result = [(letter, 'g') for letter in guess]
                messages.success(request, "Congratulations! You guessed the word.")

                guess_history.append({'guess': guess, 'result': result})
                request.session['guess_history'] = guess_history
                guess_history.clear()
                del request.session['secret_word']
            else:
                result = []
                secret_word_list = list(SECRET_WORD)
                guess_list = list(guess)

                matched_indices = []

                for i in range(5):
                    if guess_list[i] == secret_word_list[i]:
                        result.append((guess_list[i], 'g'))
                        matched_indices.append(i)
                    else:
                        result.append((guess_list[i], 'r'))

                for i in range(5):
                    if result[i][1] == 'r' and guess_list[i] in secret_word_list:
                        if guess_list[i] != secret_word_list[i] and guess_list[i] not in [
                            guess_list[j] for j in matched_indices]:
                            result[i] = (guess_list[i], 'y')
                            matched_indices.append(secret_word_list.index(guess_list[i]))

                messages.error(request, "Try again! Incorrect guess.")

                guess_history.append({'guess': guess, 'result': result})
                request.session['guess_history'] = guess_history

            return redirect('/wordle')  # Redirect after handling a guess

        else:
            messages.error(request, "Please enter a valid 5-letter word.")

    return render(request, 'wordle/wordle_game.html', {
        'messages': messages,
        'guessed_word': guessed_word,
        'guess_history': guess_history[::-1]
    })
