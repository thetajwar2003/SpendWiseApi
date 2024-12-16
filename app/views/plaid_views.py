from flask import Blueprint, request, jsonify, current_app
from ..controllers.plaid_controller import PlaidController
from ..models.user_model import UserModel
from functools import wraps
from datetime import datetime, timedelta, date
from collections import defaultdict

# Define Blueprint correctly
plaid_bp = Blueprint('plaid_bp', __name__)


def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({'error': 'Authorization Bearer token is required'}), 401

        # Extract the Access Token (Bearer token)
        access_token = auth_header.split(" ")[1]
        # Attach to request object for downstream use
        request.access_token = access_token
        return func(*args, **kwargs)

    return decorated


@plaid_bp.route('/create_link_token', methods=['POST'])
def create_link_token():
    # Access the Plaid client from the current app context
    plaid_client = current_app.plaid_client
    plaid_controller = PlaidController(plaid_client)

    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        link_token = plaid_controller.create_link_token(user_id)
        return jsonify({'link_token': link_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@plaid_bp.route('/exchange_public_token', methods=['POST'])
def exchange_public_token():
    # Access the Plaid client and user model from the current app context
    plaid_client = current_app.plaid_client
    user_model = UserModel(current_app.dynamodb)  # Initialize the user model
    plaid_controller = PlaidController(plaid_client)

    data = request.json
    public_token = data.get('public_token')
    user_id = data.get('user_id')

    if not public_token or not user_id:
        return jsonify({'error': 'Public token and user_id are required'}), 400

    try:
        # Exchange public token for access token and item_id
        access_token, item_id = plaid_controller.exchange_public_token(
            public_token)

        # Update the user in DynamoDB with the new access_token and item_id
        user_model.update_item(
            user_id, access_token=access_token, item_id=item_id)

        return jsonify({
            "message": "Bank account linked successfully",
            "item_id": item_id,
            "access_token": access_token  # Optional to return for security
        }), 200

    except Exception as e:
        return jsonify({'error': f"Error linking bank account: {str(e)}"}), 500


@plaid_bp.route('/get_user_bank_info', methods=['POST'])
@requires_auth  # Validate the Bearer token
def get_user_bank_info():
    """
    Fetch the user's bank account information from Plaid using their access token.
    """
    plaid_client = current_app.plaid_client
    user_model = UserModel(current_app.dynamodb)  # Initialize the user model
    plaid_controller = PlaidController(plaid_client)

    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        # Retrieve user from DynamoDB
        user = user_model.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = user.get('access_token')
        if not access_token:
            return jsonify({'error': 'No linked bank account for this user'}), 400

        # Fetch bank accounts using Plaid
        accounts = plaid_controller.get_accounts(access_token)

        return jsonify({
            "message": "User bank information retrieved successfully",
            "accounts": accounts
        }), 200

    except Exception as e:
        return jsonify({'error': f"Error fetching bank info: {str(e)}"}), 500


@plaid_bp.route('/transactions/summary', methods=['POST'])
@requires_auth
def get_transactions_summary():
    """
    Fetch the user's transactions and compute income/expenses summary.
    Allows optional start_date and end_date parameters.
    """
    plaid_client = current_app.plaid_client
    user_model = UserModel(current_app.dynamodb)
    plaid_controller = PlaidController(plaid_client)

    data = request.json
    user_id = data.get('user_id')
    start_date = data.get('start_date')  # Optional
    end_date = data.get('end_date')  # Optional

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        # Retrieve user from DynamoDB
        user = user_model.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = user.get('access_token')
        if not access_token:
            return jsonify({'error': 'No linked bank account for this user'}), 400

        # Convert start_date and end_date to datetime.date
        start_date = datetime.strptime(
            start_date, "%Y-%m-%d").date() if start_date else None
        end_date = datetime.strptime(
            end_date, "%Y-%m-%d").date() if end_date else None

        # Get transactions summary
        summary = plaid_controller.get_transactions_summary(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )

        return jsonify({
            "message": "Transactions summary fetched successfully",
            "income": round(summary["income"], 2),
            "expenses": round(summary["expenses"], 2),
            "income_details": summary["income_details"],
            "expense_details": summary["expense_details"]
        }), 200

    except Exception as e:
        return jsonify({'error': f"Error fetching transactions summary: {str(e)}"}), 500


@plaid_bp.route('/transactions/monthly-summary', methods=['POST'])
@requires_auth
def get_monthly_summary():
    """
    Endpoint to get income and expense summary for each month.
    """
    plaid_client = current_app.plaid_client
    plaid_controller = PlaidController(plaid_client)
    user_model = UserModel(current_app.dynamodb)

    # Get request data
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        # Retrieve user from DynamoDB
        user = user_model.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = user.get('access_token')
        if not access_token:
            return jsonify({'error': 'No linked bank account for this user'}), 400

        # Fetch transactions from Plaid
        transactions = plaid_controller.get_transactions(access_token)

        # Process transactions: group by month
        monthly_summary = defaultdict(lambda: {'income': 0, 'expenses': 0})

        for txn in transactions:
            try:
                # Safely handle txn['date']
                txn_date = txn.get('date')
                if not txn_date:
                    continue  # Skip if no date

                # Check if txn_date is already a datetime.date object
                if isinstance(txn_date, datetime):
                    txn_date = txn_date.date()  # Extract date if datetime
                elif isinstance(txn_date, str):
                    txn_date = datetime.strptime(txn_date, "%Y-%m-%d").date()

                # Extract month abbreviation
                month = txn_date.strftime("%b")

                # Categorize amount into income or expenses
                amount = txn.get('amount', 0)
                if amount < 0:  # Negative amount = income
                    monthly_summary[month]['income'] += abs(amount)
                else:  # Positive amount = expense
                    monthly_summary[month]['expenses'] += amount
            except Exception as txn_error:
                print(f"Skipping malformed transaction: {txn_error}")
                continue

        # Convert summary to a list of dictionaries (sorted by month order)
        month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                       'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        result = [
            {
                "month": month,
                "income": round(monthly_summary[month]['income'], 2),
                "expenses": round(monthly_summary[month]['expenses'], 2)
            }
            for month in month_order if month in monthly_summary
        ]

        return jsonify({
            "message": "Monthly income and expense summary fetched successfully",
            "monthly_summary": result
        }), 200

    except Exception as e:
        return jsonify({'error': f"Error fetching monthly summary: {str(e)}"}), 500


@plaid_bp.route('/transactions/expense-categories', methods=['POST'])
@requires_auth
def get_expense_categories():
    """
    Endpoint to get expense categories breakdown for the previous month.
    """
    plaid_client = current_app.plaid_client
    plaid_controller = PlaidController(plaid_client)
    user_model = UserModel(current_app.dynamodb)

    # Get request data
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        # Retrieve user from DynamoDB
        user = user_model.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = user.get('access_token')
        if not access_token:
            return jsonify({'error': 'No linked bank account for this user'}), 400

        # Fetch expense categories
        result = plaid_controller.get_previous_month_expenses(access_token)

        return jsonify({
            "message": "Expense categories fetched successfully",
            "categories": result["categories"],
            "total_categories": result["total_categories"],
            "total_expenses": result["total_expenses"]
        }), 200

    except Exception as e:
        return jsonify({'error': f"Error fetching expense categories: {str(e)}"}), 500


@plaid_bp.route('/get_account_details', methods=['POST'])
@requires_auth
def get_account_details():
    """
    Fetch details of a specific account and its transactions, highlighting recurring ones.
    """
    plaid_client = current_app.plaid_client
    user_model = UserModel(current_app.dynamodb)
    plaid_controller = PlaidController(plaid_client)

    # Get request data
    data = request.json
    user_id = data.get('user_id')
    account_id = data.get('account_id')

    if not user_id or not account_id:
        return jsonify({'error': 'User ID and Account ID are required'}), 400

    try:
        # Retrieve user from DynamoDB
        user = user_model.get_user(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        access_token = user.get('access_token')
        if not access_token:
            return jsonify({'error': 'No linked bank account for this user'}), 400

        # Fetch account details
        account_details = plaid_controller.get_account_details(
            access_token, account_id)

        # Fetch transactions and identify recurring ones
        transactions_data = plaid_controller.get_transactions_for_account(
            access_token, account_id)

        return jsonify({
            "message": "Account details and transactions fetched successfully",
            "account_details": account_details,
            "transactions": transactions_data["transactions"],
            "recurring_transactions": transactions_data["recurring_transactions"]
        }), 200

    except Exception as e:
        return jsonify({'error': f"Error fetching account details: {str(e)}"}), 500


@plaid_bp.route("/liabilities", methods=["POST"])
@requires_auth
def get_liabilities():
    """
    Fetch liabilities data for the user's accounts.
    Includes credit cards, mortgage, and student loans.
    """
    plaid_client = current_app.plaid_client
    user_model = UserModel(current_app.dynamodb)
    plaid_controller = PlaidController(plaid_client)

    # Retrieve request body data
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        # Fetch user from database
        user = user_model.get_user(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        access_token = user.get("access_token")
        if not access_token:
            return jsonify({"error": "No linked bank account for this user"}), 400

        # Fetch liabilities from Plaid
        liabilities = plaid_controller.get_liabilities(access_token)

        return jsonify({
            "message": "Liabilities fetched successfully",
            "liabilities": liabilities
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error fetching liabilities: {str(e)}"}), 500
