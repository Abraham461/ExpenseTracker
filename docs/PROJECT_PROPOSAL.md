# SubTrack - Daily Expense Tracker

## Executive Summary
SubTrack helps users build daily spending discipline by tracking expenses, optionally setting monthly income, and receiving proactive alerts when spending runs ahead of plan.

## Problem Statement
Many users know their income but lack a clear daily budget. Without daily feedback, small expenses accumulate and lead to overspending. Manual tracking is also easy to skip.

## Proposed Solution
A Django-based web system that provides:
- Daily expense logging with category and reason fields for clearer insights.
- Automatic daily budget calculation when monthly income is set.
- Smart warnings with budget progress indicators.
- Daily reminder notifications to keep logs up to date.
- Visual analytics for spending patterns and budget health.
- A streak system that rewards consistent daily logging.
- A daily summary view: "What did I spend on today?"

## Technical Architecture
Layer | Technology
--- | ---
Backend | Python (Django MVT Architecture)
Database | SQLite (Development), PostgreSQL (Production)
Frontend | HTML, CSS, Bootstrap 5
Data Visualization | Chart.js
ORM | Django ORM
Authentication | Django Built-in Auth System

## Core Modules
1. **Authentication**: Sign up, login, logout.
2. **Expense Management**: CRUD for daily expenses.
3. **Category System**: Classify expenses (Food, Transport, Shopping, Bills, Entertainment, Other).
4. **Reason Capture**: Log why each expense occurred.
5. **Income Settings**: Optional monthly income input.
6. **Budget Engine**: Daily budget calculation and remaining budget display.
7. **Dashboard and Analytics**: Daily limit, month-to-date totals, charts.
8. **Streak System**: Track consecutive days with at least one expense logged.
9. **Notification Engine**: Daily reminders and overspend alerts.

## Core Concept Improvements
- **Automatic Daily Budget Calculation**: If monthly income is provided, daily limit = monthly income / days in month. The dashboard shows remaining daily budget (example: "You have $12.40 left for today.").
- **Category System**: Expenses are categorized in addition to a free-text reason. This enables better analytics and faster entry.
- **Smart Warnings**: Progress indicators show budget health. Green indicates within budget. Yellow indicates approaching limit. Red indicates overspending. Example message: "You have used 85% of today's budget."

## UI Improvements
- **Minimal Click Flow**: Quick Add Expense button on the dashboard for sub-3-second entry.
- **Dashboard Layout**: Clear daily summary and immediate action.

```text
Daily Budget: $20
Spent Today: $12
Remaining: $8

[ Add Expense ]

Today's Expenses
- Coffee ($3)
- Taxi ($6)
- Lunch ($3)

Monthly Overview Chart
```

- **Quick Add Form**:

```text
Amount: ______
Category: [Food v]
Reason: Coffee with friends
Date: Auto Today
[ Save ]
```

## Analytics Enhancements
- **Spending by Category**: Pie chart showing category breakdown.
- **Weekly Spending Trend**: Line chart by day of week.
- **Monthly Budget Progress**: Progress bar indicating budget used (example: "Budget Used: 68%").

## Streak System
Tracks consecutive days where the user logs at least one expense. This encourages daily engagement and habit formation.

## Smart Reminders
- **Daily Reminder** (8 PM): "You haven't logged today's expenses yet."
- **Overspending Warning**: "You exceeded today's budget by $4."

## Small UX Features
- **Auto Suggestions**: When typing a reason, suggest previous entries (example: "coffee").
- **Quick Repeat Expense**: One-click repeat for frequent expenses.
- **Dark Mode**: Optional theme for better accessibility at night.
- **Export Data**: Download as CSV or Excel for reporting or assignments.

## Implementation Details by Feature

## 1. Expense Categories
Where to implement:
- Module: Expense Management
- Layer: Database + Backend + Frontend

What to do:
- Add a Category table/model and link it to Expense instead of relying only on the reason field.

Example Django models:
```python
class Category(models.Model):
    name = models.CharField(max_length=50)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    reason = models.CharField(max_length=255)
    date = models.DateField()
```

UI location:
- Expense form fields: Amount, Category (dropdown), Reason, Date.

Why:
- Enables analytics by category.
- Improves user input speed.

## 2. Automatic Daily Budget Calculation
Where to implement:
- Module: Income Settings + Dashboard
- Layer: Backend logic

What to do:
- Calculate daily budget automatically based on monthly income.

Backend logic:
```python
from calendar import monthrange
from datetime import date

days = monthrange(date.today().year, date.today().month)[1]
daily_budget = user_income / days
```

Display location:
```text
Daily Budget: $20
Spent Today: $12
Remaining: $8
```

## 3. Overspending Alert System
Where to implement:
- Module: Notification Engine
- Layer: Backend + Dashboard

What to do:
- Compare today's spending with the calculated daily limit.

Backend check:
```python
if today_spending > daily_budget:
    trigger alert
```

UI output:
```text
You exceeded today's budget by $4
```

## 4. Analytics Charts
Where to implement:
- Module: Dashboard and Analytics
- Layer: Frontend visualization

Use: Chart.js.

Chart 1: Spending by Category
- Data source: category totals.
- Chart type: Pie chart.

Chart 2: Weekly Spending Trend
- Data source: expenses grouped by date.
- Chart type: Line chart.

## 5. Dashboard Layout Improvement
Where to implement:
- Module: Dashboard Template
- Layer: Frontend (Django Templates + Bootstrap)

Layout structure:
Top Section
-----------
Daily Budget
Spent Today
Remaining Budget

Middle Section
--------------
Add Expense Button

Bottom Section
--------------
Expense List
Charts

Example Bootstrap structure:
- Row 1: Budget cards
- Row 2: Add expense button
- Row 3: Charts
- Row 4: Expense table

## 6. Daily Reminder Notification
Where to implement:
- Module: Notification Engine
- Layer: Backend task scheduler

What to do:
- If no expense logged today, remind the user.

Logic:
```python
if no expense for today:
    send reminder
```

Example reminder:
You haven't logged today's expenses yet.

## 7. Quick Expense Entry
Where to implement:
- Module: Expense Management
- Layer: Frontend UX

What to do:
- Add a fast entry form using a Bootstrap modal instead of a new page.

Example interface:
```text
Amount: ______
Category: [v]
Reason: ______
[Add Expense]
```

## 8. Database Optimization
Where to implement:
- Module: Database design

What to do:
- Add indexes for faster queries.

Example:
```python
date = models.DateField(db_index=True)
```

Helps with:
- Daily spending calculations.
- Analytics queries.

## 9. Export Expense Data
Where to implement:
- Module: Analytics or Reporting
- Layer: Backend

What to do:
- Allow users to export data.

Export formats:
- CSV
- Excel

Example endpoint:
```text
/export-expenses/
```

Django response:
```python
HttpResponse(content_type="text/csv")
```

## 10. Security Improvements
Where to implement:
- Module: Authentication

What to do:
- Use Django built-in authentication system.

Key protections:
- Password hashing
- Session management
- CSRF protection

## 11. Improved Non-Functional Requirements
Performance:
Dashboard loads in under 2 seconds.

Security:
Use Django authentication and CSRF protection.

Usability:
Responsive UI using Bootstrap.

Scalability:
System compatible with PostgreSQL for production deployment.

## 12. System Flow (Implementation Perspective)
User Login
  ->
Dashboard
  ->
Add Expense
  ->
Expense saved to database
  ->
Dashboard updates totals
  ->
Notification engine checks spending

## System Flow
User Login
  ->
Dashboard
  ->
Add Expense
  ->
Store in Database
  ->
Update Analytics
  ->
Budget Alert Engine

## Future Enhancements
- Mobile application integration
- Bank transaction import
- AI spending recommendations
- Multi-currency support
- Shared household budgets

## Standout Feature: "What Did I Spend On Today?"
Daily summary view that explains spending in simple terms.
Example:
You spent $18 today:
Food: $10
Transport: $5
Coffee: $3

## Non-Functional Requirements
- Performance: dashboard loads within ~2 seconds on standard datasets.
- Security: password hashing and built-in auth from Django.
- Usability: responsive UI with quick entry flow.
- Scalability: PostgreSQL-ready deployment path.
