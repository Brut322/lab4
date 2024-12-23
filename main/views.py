from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import BoardGame, Publisher, Category, Age
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required


def board_game_list(request):
    """Список настільних ігор з фільтрацією та пошуком."""

    games = BoardGame.objects.select_related('publisher').all()

    # Отримуємо фільтри з GET-запиту
    search_query = request.GET.get('search', '').strip()
    category = request.GET.get('category', '')
    age = request.GET.get('age', '')
    publisher_id = request.GET.get('publisher', '')

    # Фільтр по назві (пошук)
    if search_query:
        games = games.filter(name__icontains=search_query)

    # Фільтр по категорії
    if category:
        games = games.filter(category=category)

    # Фільтр по віку
    if age:
        games = games.filter(age=age)

    # Фільтр по видавцю
    if publisher_id:
        games = games.filter(publisher_id=publisher_id)

    # Для select'ів у шаблоні передамо список категорій, вікових обмежень та видавців
    context = {
        'games': games,
        'games_categories': Category.choices,  # Список кортежів (ключ, значення)
        'games_ages': Age.choices,            # Аналогічно
        'publishers': Publisher.objects.all(),
    }
    return render(request, 'main/list.html', context)


def board_game_detail(request, game_id):
    """Детальний перегляд настільної гри."""
    game = get_object_or_404(BoardGame, id=game_id)
    return render(request, 'main/detail.html', {'game': game})


@login_required
def toggle_favorite(request, game_id):
    """Додає або видаляє гру з "улюблених" поточного користувача."""
    game = get_object_or_404(BoardGame, id=game_id)
    user = request.user

    if game in user.favorites.all():
        # Якщо вже в улюблених, то видаляємо
        user.favorites.remove(game)
        messages.info(request, f"Гру '{game.name}' видалено з улюблених.")
    else:
        # Якщо немає в улюблених, то додаємо
        user.favorites.add(game)
        messages.success(request, f"Гру '{game.name}' додано до улюблених!")

    return redirect('detail', game_id=game_id)


@login_required
def profile_view(request):
    user = request.user
    # user.favorites містить усі його улюблені ігри
    favorites = user.favorites.select_related('publisher').all()

    return render(request, 'main/profile.html', {
        'user': user,
        'favorites': favorites,
    })


def register_view(request):
    if request.user.is_authenticated:
        return redirect('list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація пройшла успішно! Ви увійшли в систему.")
            return redirect('list')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('list')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Ви успішно увійшли.")
                return redirect('list')
            else:
                messages.error(request, "Неправильний email або пароль.")
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('list')