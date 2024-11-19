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
- Deployed with **AWS Elastic Beanstalk** for scalability and high availability.

---

## Tech Stack

### Backend

- **Python** (Flask framework)
- **AWS DynamoDB**: Database for storing user data, transactions, budgets, and subscriptions.
- **AWS Cognito**: Authentication and user management.
- **Plaid API**: For secure financial data integration.

### Deployment

- **AWS Elastic Beanstalk**: For scalable and managed deployment.
- **AWS Lambda & API Gateway** (Optional): For serverless execution.

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

5. **Run the application:**

   ```bash
   python run.py
   ```

6. **Test the application:**

   Use **Postman** or **cURL** to test the endpoints. The server will run on `http://127.0.0.1:5000`.

---

## API Endpoints

### **Authentication**

| Method | Endpoint         | Description         |
| ------ | ---------------- | ------------------- |
| POST   | `/auth/register` | Register a new user |
| POST   | `/auth/login`    | Login and get a JWT |

### **Transactions**

| Method | Endpoint        | Description                     |
| ------ | --------------- | ------------------------------- |
| POST   | `/transactions` | Add a new transaction           |
| GET    | `/transactions` | Get all transactions for a user |

### **Budgets**

| Method | Endpoint              | Description                |
| ------ | --------------------- | -------------------------- |
| POST   | `/budgets`            | Create a new budget        |
| GET    | `/budgets`            | Get all budgets for a user |
| PUT    | `/budgets/<category>` | Update a budget category   |
| DELETE | `/budgets/<category>` | Delete a budget category   |

### **Subscriptions**

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| POST   | `/subscriptions`      | Add a new subscription           |
| GET    | `/subscriptions`      | Get all subscriptions for a user |
| DELETE | `/subscriptions/<id>` | Delete a subscription            |

### **Plaid Integration**

| Method | Endpoint                   | Description                      |
| ------ | -------------------------- | -------------------------------- |
| POST   | `/plaid/create_link_token` | Create a Plaid Link token        |
| POST   | `/plaid/exchange_token`    | Exchange public token for access |
