# urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import base, newhome, signup, custom_login, expense_list, ExpenseCreateView, ExpenseUpdateView, \
    ExpenseDeleteView, custom_logout

urlpatterns = [
    path('', base, name='base'),
    path('newhome/', newhome, name='newhome'),
    path('signup/', signup, name='signup'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

    path('expenses/', expense_list, name='expense_list'),
    path('expenses/add/', ExpenseCreateView.as_view(), name='expense_add'),
    path('expenses/edit/<int:expense_id>/', ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expenses/delete/<int:expense_id>/', ExpenseDeleteView.as_view(), name='expense_delete'),
]
