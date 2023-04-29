from django.contrib import admin

from reviews.models import Category, Comments, Genre, Review, Title
from users.models import User

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Review)
