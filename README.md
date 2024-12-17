# SpendWise Backend - Flask Application

SpendWise is a **Personal Finance Management App** designed to help users manage their finances effortlessly. This repository contains the backend implementation for SpendWise, built with Flask and integrated with AWS services to provide a secure and scalable solution. It follows the **MVC architecture** for clear separation of concerns and maintainability.

---

## Features

### Authentication

- User registration and login via **AWS Cognito**.
- JWT-based session handling for secure API access.

### Transactions

- Add, retrieve, update, and delete financial transactions.
- Integration with **Plaid API** for transaction synchronization.

### Budgeting

- Set, retrieve, update, and delete budgets for various spending categories.
- Monitor budgets for better financial planning.

### Subscription Management

- Add, retrieve, and delete recurring subscriptions.
- Track subscription costs and avoid unnecessary payments.

### Financial Insights

- View detailed financial insights (monthly, quarterly, annual).

### Scalability and Security

- Built using **AWS DynamoDB** for non-relational data storage.
- Deployed with **Heroku** for production scalability.
- Integrated with **Plaid** for banking data and secure transactions.

---

## Tech Stack

### Backend

- **Python** (Flask framework)
- **AWS DynamoDB**: Database for storing user data, transactions, budgets, and subscriptions.
- **AWS Cognito**: Authentication and user management.
- **Plaid API**: For secure financial data integration.

### Deployment

- **Heroku**: For scalable and managed deployment.

---

## Project Structure

```
spendwise-backend/
├── app/
│   ├── __init__.py                # Flask app factory
│   ├── models/                    # Data models (DynamoDB interactions)
│   │   ├── __init__.py
│   │   ├── user_model.py          # User data model
│   │   ├── transaction_model.py   # Transaction data model
│   │   ├── budget_model.py        # Budget data model
│   │   └── subscription_model.py  # Subscription data model
│   ├── controllers/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth_controller.py     # Handles authentication logic
│   │   ├── transaction_controller.py # Handles transaction logic
│   │   ├── budget_controller.py   # Handles budget logic
│   │   └── subscription_controller.py # Handles subscription logic
│   ├── views/                     # Routes for API endpoints
│   │   ├── __init__.py
│   │   ├── auth_views.py          # Authentication routes
│   │   ├── transaction_views.py   # Transaction routes
│   │   ├── budget_views.py        # Budget routes
│   │   └── subscription_views.py  # Subscription routes
│   ├── utils/                     # Utility modules for AWS and Plaid
│   │   ├── __init__.py
│   │   ├── aws_cognito.py         # AWS Cognito integration
│   │   ├── aws_dynamodb.py        # AWS DynamoDB integration
│   │   └── plaid_client.py        # Plaid API integration
│   └── config.py                  # Configuration file
├── requirements.txt               # Dependencies
├── run.py                         # Application entry point
└── README.md                      # This file
```

---

## Installation and Setup

### Prerequisites

1. Python 3.8 or later
2. AWS Account with credentials for **DynamoDB**, **Cognito**, and other services.
3. Plaid API credentials.
4. Heroku CLI installed.

---

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/spendwise-backend.git
   cd spendwise-backend
   ```

2. **Set up a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Create a `.env` file in the root directory and add the following:

   ```plaintext
   AWS_REGION=your-aws-region
   AWS_ACCESS_KEY_ID=your-access-key
   AWS_SECRET_ACCESS_KEY=your-secret-key
   COGNITO_USER_POOL_ID=your-cognito-user-pool-id
   COGNITO_APP_CLIENT_ID=your-cognito-app-client-id
   PLAID_CLIENT_ID=your-plaid-client-id
   PLAID_SECRET=your-plaid-secret
   PLAID_ENV=sandbox  # or 'development'/'production'
   ```

5. **Run the application locally:**

   ```bash
   python run.py
   ```

6. **Run Tests with Coverage:**

   ```bash
   pytest --cov=app --cov-report=term --cov-report=html
   ```

   This will generate an HTML coverage report in the `htmlcov` folder.

7. **Deploy to Heroku:**

   ```bash
   git push heroku master
   ```

---

## API Endpoints

### **Authentication**

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| POST   | `/auth/register` | Register a new user |
| POST   | `/auth/login`    | Login and get a JWT |

---

### **Plaid Integration**

| Method | Endpoint                                 | Description                             |
| ------ | ---------------------------------------- | --------------------------------------- |
| POST   | `/plaid/create_link_token`               | Create a Plaid Link token               |
| POST   | `/plaid/exchange_public_token`           | Exchange public token for access token  |
| POST   | `/plaid/get_user_bank_info`              | Retrieve user's linked bank information |
| POST   | `/plaid/transactions/summary`            | Get transactions income/expense summary |
| POST   | `/plaid/transactions/monthly-summary`    | Monthly income and expense summary      |
| POST   | `/plaid/transactions/expense-categories` | Breakdown of expenses by category       |
| POST   | `/plaid/get_account_details`             | Fetch details of a specific account     |
| POST   | `/plaid/liabilities`                     | Get user's liabilities data             |

---

## Coverage Badge

![Coverage](./coverage.svg)

---

## Deployment

1. Ensure Heroku CLI is installed and logged in:

   ```bash
   heroku login
   ```

2. Deploy the app:

   ```bash
   git push heroku master
   ```

3. Add environment variables to Heroku:

   ```bash
   heroku config:set AWS_REGION=your-region
   heroku config:set AWS_ACCESS_KEY_ID=your-access-key
   heroku config:set AWS_SECRET_ACCESS_KEY=your-secret-key
   heroku config:set PLAID_CLIENT_ID=your-client-id
   heroku config:set PLAID_SECRET=your-plaid-secret
   ```

---

### CI/CD Pipeline with GitHub Actions

A **GitHub Actions** workflow is configured for:

1. Running tests with coverage.
2. Deploying the app to Heroku.

**GitHub Workflow:**

```yaml
name: CI/CD for Flask App to Heroku

on:
  push:
    branches:
      - master

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Tests with Coverage
        run: |
          pytest --cov=app --cov-report=term --cov-report=html

      - name: Update Coverage in README
        uses: cicirello/jacoco-badge-generator@v2
        with:
          coverage-summary: coverage.xml
          readme-path: README.md

      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
          heroku_email: ${{ secrets.HEROKU_EMAIL }}
```
