from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/new/', views.expense_create, name='expense_create'),
    path('expenses/import/', views.import_expenses, name='import_expenses'),
    path('expenses/import/template/', views.export_expense_template, name='export_expense_template'),
    path('expenses/export/<str:export_format>/', views.export_expenses, name='export_expenses'),
    path('expenses/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('income/', views.income_settings, name='income_settings'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/new/', views.category_create, name='category_create'),
    path('analytics/', views.analytics, name='analytics'),
    path('insights/', views.insights, name='insights'),
    path('reminders/run/', views.run_reminders, name='run_reminders'),
]
