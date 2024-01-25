from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from .models import Expense, ExpenseCategory


def base(request):
    return render(request, 'base.html')


def newhome(request):
    return render(request, 'newhome.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Using the built-in User model for authentication
        user = User.objects.create_user(username=username, password=password)

        # Redirect to the login page after successful signup
        return redirect('login')

    return render(request, 'signup.html')


def custom_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('newhome')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login credentials. Please try again.'})

    return render(request, 'login.html')


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expense_list.html', {'expenses': expenses})


@method_decorator(login_required, name='dispatch')
class ExpenseCreateView(View):
    template_name = 'expense_form.html'

    def get(self, request):
        categories = ExpenseCategory.objects.all()
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        date = request.POST.get('date')
        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        description = request.POST.get('description')

        Expense.objects.create(
            user=request.user,
            date=date,
            amount=amount,
            category_id=category_id,
            description=description
        )

        return redirect('expense_list')


@method_decorator(login_required, name='dispatch')
class ExpenseUpdateView(View):
    template_name = 'expense_form.html'

    def get(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        categories = ExpenseCategory.objects.all()
        return render(request, self.template_name, {'expense': expense, 'categories': categories})

    def post(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        expense.date = request.POST.get('date')
        expense.amount = request.POST.get('amount')
        expense.category_id = request.POST.get('category')
        expense.description = request.POST.get('description')
        expense.save()

        return redirect('expense_list')


@method_decorator(login_required, name='dispatch')
class ExpenseDeleteView(View):
    def get(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        return render(request, 'expense_confirm_delete.html', {'expense': expense})

    def post(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id, user=request.user)
        expense.delete()
        return redirect('expense_list')


def custom_logout(request):
    logout(request)
    return redirect('base')