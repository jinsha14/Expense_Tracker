from django.contrib import admin
from .models import Profile, ExpenseCategory, Expense

# Register your models here.
admin.site.register(Profile)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)