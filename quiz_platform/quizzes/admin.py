from django.contrib import admin
from .models import Quiz, Question, Result, UserAnswer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(UserAnswer)