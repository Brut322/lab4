from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Publisher(models.Model):
    """
    Модель Видавця.
    Поля:
    - name (назва)
    - logo (лого)
    """
    name = models.CharField(max_length=255, verbose_name="Назва видавця")
    logo = models.ImageField(
        upload_to="publishers_logos/",
        verbose_name="Логотип видавця",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Category(models.TextChoices):
    STRATEGII = "Стратегії", "Стратегії"
    EKONOMIKA = "Економіка", "Економіка"
    VIISKOVI = "Військові", "Військові"
    AMERITRESH = "Америтреш", "Америтреш"
    EVRO = "Євро", "Євро"
    ABSTRACT = "Абстракти", "Абстракти"
    PRYGODY = "Пригоди", "Пригоди"
    COOPERATIVE = "Кооперативні", "Кооперативні"
    ONE_VS_ALL = "Один проти всіх", "Один проти всіх"
    NA_UDACHU = "На удачу", "На удачу"
    NA_KUBYKAH = "На кубиках", "На кубиках"
    NA_SPRYTNIST = "На спритність", "На спритність"
    LOGICHNI = "Логічні", "Логічні"
    VIKTORINA = "Вікторина", "Вікторина"
    MAFIYA = "Мафія", "Мафія"
    MISTOBUDIVNI = "Містобудівні", "Містобудівні"
    TVORCHI = "Творчі", "Творчі"
    NA_ASOTSIATSIYI = "На асоціації", "На асоціації"
    ROZMOVNI = "Розмовні", "Розмовні"
    KLASIKA = "Класика", "Класика"
    KVESTY = "Квести", "Квести"
    ISTORIYA = "Історія", "Історія"
    FANTASTYKA = "Фантастика", "Фантастика"
    FENTEZI = "Фентезі", "Фентезі"
    ZHAHALKY = "Жахалки", "Жахалки"
    MITY_KTULHU = "Міти Ктулху", "Міти Ктулху"
    ZOMBI = "Зомбі", "Зомбі"
    POSTAPOKALIPSYS = "Постапокаліпсис", "Постапокаліпсис"
    TSYVILIZATSIYA = "Цивілізація", "Цивілізація"
    HUMOR = "Гумор", "Гумор"
    HOLOVOLOMKY = "Головоломки", "Головоломки"
    SPORT = "Спорт", "Спорт"
    GONKY = "Гонки", "Гонки"
    COLLECTION_CARDS = "Колекційні карткові ігри", "Колекційні карткові ігри"
    MAGIC_GATHERING = "Magic The Gathering", "Magic The Gathering"


class Age(models.TextChoices):
    AGE_2_3 = "2-3 роки", "2-3 роки"
    AGE_4_5 = "4-5 років", "4-5 років"
    AGE_6_7 = "6-7 років", "6-7 років"
    AGE_8_9 = "8-9 років", "8-9 років"
    AGE_10_13 = "10-13 років", "10-13 років"
    AGE_14p = "14+ років", "14+ років"


class BoardGame(models.Model):
    """
    Модель Настільної гри.
    Поля:
    - name (назва)
    - price (ціна)
    - description (опис)
    - image (картинка)
    - category (категорія, через choices)
    - age (вік, через choices)
    - publisher (ForeignKey на Publisher)
    """
    name = models.CharField(max_length=255, verbose_name="Назва гри")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Ціна"
    )
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    image = models.ImageField(
        upload_to="board_games_images/",
        verbose_name="Картинка гри",
        null=True,
        blank=True
    )
    category = models.CharField(
        max_length=50,
        choices=Category.choices,
        verbose_name="Категорія"
    )
    age = models.CharField(
        max_length=20,
        choices=Age.choices,
        verbose_name="Вік"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name="board_games",
        verbose_name="Видавець"
    )

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомна модель користувача, де логін здійснюється за email.
    """
    email = models.EmailField(verbose_name='Електронна адреса', max_length=60, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    favorites = models.ManyToManyField(
        BoardGame, 
        blank=True, 
        related_name='favorited_by'
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True