from django.contrib import admin
from .models import BoardGame, Publisher, User


admin.site.register(User)
admin.site.register(BoardGame)
admin.site.register(Publisher)
