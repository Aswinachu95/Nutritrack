"# Nutritrack

A Django-based nutrition tracking application that helps users monitor their daily food intake, track calories and macronutrients, and manage personalized diet plans.

## Features

- **User Authentication**: Secure user registration and login with JWT support
- **Food Database**: Comprehensive food library with nutritional information (calories, protein, carbs, fat, fiber)
- **Meal Logging**: Track meals by type (breakfast, lunch, dinner, snack) with portion sizes
- **User Profiles**: Store personal health data including:
  - Age, gender, height, and weight
  - Activity level tracking
  - Weight management goals (lose, maintain, or gain)
  - Automatic BMR (Basal Metabolic Rate) calculation
  - TDEE (Total Daily Energy Expenditure) calculation based on activity level
- **Diet Plans**: Create and manage personalized diet plans with target calorie goals
- **Daily Summary**: View daily nutritional intake and progress toward goals
- **RESTful API**: Full API endpoints for programmatic access with filtering and search capabilities
- **Admin Interface**: Django admin panel for managing foods, users, and meal logs

## Tech Stack

- **Backend**: Django 5.2+
- **Database**: SQLite (development)
- **API**: Django REST Framework with drf-spectacular for API documentation
- **Authentication**: Django built-in auth + djangorestframework-simplejwt
- **Additional Tools**:
  - django-filter: Advanced filtering on API endpoints
  - django-import-export: Import/export data functionality
  - PyYAML, jsonschema: Data validation and serialization

## Project Structure

```
nutritrack/
├── core/                     # Main Django app
│   ├── models.py            # Database models (Food, MealLog, DietPlan, UserProfile)
│   ├── views.py             # View controllers
│   ├── serializers.py       # DRF serializers for API
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL routing
│   ├── admin.py             # Django admin configuration
│   └── management/
│       └── commands/
│           ├── load_foods_csv.py    # Load food data from CSV
│           └── seed_foods.py        # Seed initial food data
├── nutritrack/              # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Project-level URL routing
│   └── wsgi.py              # WSGI application
├── templates/               # HTML templates for frontend
│   └── core/
│       ├── base.html
│       ├── home.html
│       ├── login.html
│       ├── register.html
│       ├── profile.html
│       ├── daily_summary.html
│       ├── meal_logs.html
│       ├── foods_list.html
│       ├── food_detail.html
│       └── plans.html
├── static/                  # Static files (CSS, JS)
│   └── css/
│       └── styles.css
├── data/                    # Data files
│   └── food_demo.csv
└── requirements.txt         # Python dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aswinachu95/Nutritrack.git
   cd nutritrack
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load food data** (optional)
   ```bash
   python manage.py seed_foods
   # or load from CSV:
   python manage.py load_foods_csv data/food_demo.csv
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## Database Models

### Food
- Stores food items with nutritional information
- Fields: name, category, region, is_vegetarian, calories, protein, carbs, fat, fiber

### UserProfile
- Extends Django's User model with health/fitness data
- Calculates BMR and TDEE based on user attributes
- Tracks weight goals and activity levels

### MealLog
- Records meals eaten by users
- Fields: user, food, servings, meal_type, eaten_at
- Automatically calculates total calories based on food and serving size

### DietPlan
- User-created diet plans with target calorie goals
- Tracks plan creation date and ownership

## Usage

1. **Register/Login**: Create an account or log in to the application
2. **Update Profile**: Set your personal health information in your profile
3. **Browse Foods**: View available foods in the database
4. **Log Meals**: Record meals throughout the day
5. **View Summary**: Check your daily nutritional intake on the dashboard
6. **Create Plans**: Set up diet plans with calorie targets

## Admin Panel

Access the Django admin at `/admin/` with your superuser credentials to:
- Manage users and profiles
- Add/edit/delete foods
- View and moderate meal logs
- Manage diet plans

## API Endpoints

The application provides RESTful API endpoints for all major features. API documentation is available at `/api/schema/swagger/` when running the development server.

## License

This project is open source and available under the MIT License." 
