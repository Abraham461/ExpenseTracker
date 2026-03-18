from django import forms
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Expense, UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '').strip()
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if not email:
            raise forms.ValidationError('Email is required.')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = Category
        fields = ('name', 'description')

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        if not name:
            raise forms.ValidationError('Category name is required.')
        if self.user and Category.objects.filter(user=self.user, name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('You already have a category with this name.')
        return name


class ExpenseForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user).order_by('name')
        self.fields['category'].empty_label = 'Uncategorized'

    class Meta:
        model = Expense
        fields = ('amount', 'category', 'reason', 'spent_on', 'note')
        widgets = {
            'spent_on': forms.DateInput(attrs={'type': 'date'}),
        }


class BudgetForm(forms.ModelForm):
    month_remaining_budget = forms.DecimalField(
        required=False,
        min_value=0,
        label='Monthly budget',
        help_text='Enter your expected budget for the current month.',
    )
    daily_email_reminders = forms.BooleanField(
        required=False,
        label='Daily email reminders',
        help_text='Email me a daily reminder to log expenses.',
    )

    class Meta:
        model = UserProfile
        fields = ('month_remaining_budget', 'daily_email_reminders')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['month_remaining_budget'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'e.g. 1000000'}
        )
        self.fields['daily_email_reminders'].widget.attrs.update({'class': 'form-check-input'})

    def clean(self):
        cleaned = super().clean()
        remaining = cleaned.get('month_remaining_budget')
        if remaining is not None and remaining == 0:
            raise forms.ValidationError('Monthly budget must be greater than zero.')
        return cleaned

    def save(self, commit=True):
        profile = super().save(commit=False)
        remaining = self.cleaned_data.get('month_remaining_budget')
        if remaining is not None:
            profile.budget_start_date = timezone.localdate()
        else:
            profile.budget_start_date = None
        if commit:
            profile.save()
        return profile
