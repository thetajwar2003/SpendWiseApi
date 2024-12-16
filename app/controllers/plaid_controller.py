from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from datetime import datetime, timedelta, date
from collections import defaultdict


class PlaidController:
    def __init__(self, plaid_client):
        self.plaid_client = plaid_client

    def create_link_token(self, user_id):
        request = LinkTokenCreateRequest(
            user={
                "client_user_id": user_id,
            },
            client_name="SpendWise",
            products=[Products("transactions")],
            country_codes=[CountryCode('US')],  # Fixed: Using CountryCode enum
            language="en",
            redirect_uri="http://localhost:3000/login",
        )
        response = self.plaid_client.link_token_create(request)
        return response.to_dict()["link_token"]

    def exchange_public_token(self, public_token):
        # Updated Public Token Exchange logic
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.plaid_client.item_public_token_exchange(request)
        access_token = response.to_dict()["access_token"]
        item_id = response.to_dict()["item_id"]
        return access_token, item_id

    def get_accounts(self, access_token):
        """
        Retrieve accounts and balances associated with the given access token.
        """
        try:
            # Use the access token to fetch accounts
            request = AccountsGetRequest(access_token=access_token)
            response = self.plaid_client.accounts_get(request)
            accounts = response.to_dict()["accounts"]
            return accounts
        except Exception as e:
            raise Exception(f"Error fetching accounts: {str(e)}")

    def get_transactions_summary(self, access_token, start_date=None, end_date=None):
        """
        Fetch and summarize transactions into income and expenses.
        Allows optional start_date and end_date.
        """
        try:
            # Set default date range (last 30 days) if not provided
            end_date = end_date or datetime.now().date()
            start_date = start_date or (end_date - timedelta(days=30))

            # Request transactions from Plaid
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date,
                options=TransactionsGetRequestOptions(count=500, offset=0)
            )
            response = self.plaid_client.transactions_get(request)
            transactions = response.to_dict()["transactions"]

            # Summarize income and expenses
            summary = {
                "income": 0,
                "expenses": 0,
                "income_details": [],
                "expense_details": []
            }

            for txn in transactions:
                amount = txn["amount"]
                category = txn.get("category", ["Uncategorized"])[0]
                date = txn["date"]

                # Income: Negative amount
                if amount < 0:
                    summary["income"] += abs(amount)
                    summary["income_details"].append({
                        "date": date,
                        "amount": abs(amount),
                        "category": category,
                        "name": txn["name"]
                    })
                # Expenses: Positive amount
                else:
                    summary["expenses"] += amount
                    summary["expense_details"].append({
                        "date": date,
                        "amount": amount,
                        "category": category,
                        "name": txn["name"]
                    })

            return summary
        except Exception as e:
            raise Exception(f"Error fetching transactions: {str(e)}")

    def get_transactions(self, access_token):
        """
        Fetch all transactions for the current year.
        """
        try:
            end_date = datetime.now().date()
            start_date = datetime(end_date.year, 1, 1).date()

            # Plaid Transactions API request requires date objects
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,  # Pass as date
                end_date=end_date,      # Pass as date
                options=TransactionsGetRequestOptions(count=500, offset=0)
            )
            response = self.plaid_client.transactions_get(request)
            transactions = response.to_dict()["transactions"]

            return transactions
        except Exception as e:
            raise Exception(f"Error fetching transactions: {str(e)}")

    def get_monthly_summary(self, access_token):
        """
        Get income and expense summary grouped by month for the current year.
        """
        try:
            # Fetch all transactions for the current year
            transactions = self.get_transactions(access_token)

            # Dictionary to store monthly income and expenses
            monthly_summary = defaultdict(
                lambda: {"income": 0.0, "expenses": 0.0})

            # Process transactions
            for txn in transactions:
                # Safely extract and parse the date
                tx_date_str = txn.get("date")
                if not tx_date_str:
                    continue  # Skip transactions without a date

                try:
                    tx_date = datetime.strptime(tx_date_str, "%Y-%m-%d").date()
                except ValueError:
                    continue  # Skip transactions with invalid date formats

                # Extract month name (e.g., "January", "February")
                month = tx_date.strftime("%B")

                # Extract the transaction amount
                amount = txn.get("amount", 0.0)
                if amount < 0:
                    # Income is negative
                    monthly_summary[month]["income"] += abs(amount)
                else:
                    # Expense is positive
                    monthly_summary[month]["expenses"] += amount

            # Prepare the result sorted by month order
            month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                           'July', 'August', 'September', 'October', 'November', 'December']

            result = [
                {
                    "month": month,
                    "income": round(monthly_summary[month]["income"], 2),
                    "expenses": round(monthly_summary[month]["expenses"], 2)
                }
                for month in month_order if month in monthly_summary
            ]

            return result
        except Exception as e:
            raise Exception(f"Error fetching monthly summary: {str(e)}")
