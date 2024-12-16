from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.liabilities_get_request import LiabilitiesGetRequest
from plaid.exceptions import ApiException
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
            products=[Products("transactions"), Products("liabilities")],
            country_codes=[CountryCode('US')],
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

    def get_previous_month_expenses(self, access_token):
        """
        Fetch expenses for the previous month and categorize them.
        """
        try:
            # Calculate previous month's start and end dates
            today = date.today()
            first_day_current_month = today.replace(day=1)
            last_day_previous_month = first_day_current_month - \
                timedelta(days=1)
            first_day_previous_month = last_day_previous_month.replace(day=1)

            # start_date and end_date as date objects
            start_date = first_day_previous_month
            end_date = last_day_previous_month

            # Fetch transactions from Plaid
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date,
                options=TransactionsGetRequestOptions(count=500, offset=0)
            )
            response = self.plaid_client.transactions_get(request)
            transactions = response.to_dict()["transactions"]

            # Group expenses by category
            category_expenses = defaultdict(float)
            total_expenses = 0.0

            for txn in transactions:
                amount = txn["amount"]
                category = txn.get("category", ["Uncategorized"])[0]

                # Only process expenses (positive amounts)
                if amount > 0:
                    category_expenses[category] += amount
                    total_expenses += amount

            # Format results
            formatted_categories = [
                {"category": cat, "amount": round(amount, 2)}
                for cat, amount in category_expenses.items()
            ]

            return {
                "categories": formatted_categories,
                "total_categories": len(category_expenses),
                "total_expenses": round(total_expenses, 2)
            }

        except Exception as e:
            raise Exception(
                f"Error fetching previous month expenses: {str(e)}")

    def get_account_details(self, access_token, account_id):
        """
        Fetch account details for a specific account.
        """
        try:
            # Use the AccountsGetRequest to fetch account details
            request = AccountsGetRequest(access_token=access_token)
            response = self.plaid_client.accounts_get(request)
            accounts = response.to_dict().get("accounts", [])

            # Filter to get the specific account by account_id
            for account in accounts:
                if account["account_id"] == account_id:
                    return account  # Return the matched account details

            # If no account matches, raise an exception
            raise Exception("Account not found for the given account_id")

        except Exception as e:
            raise Exception(f"Error fetching account details: {str(e)}")

    def get_transactions_for_account(self, access_token, account_id, days=90):
        """
        Fetch transactions for a specific account and identify recurring transactions.
        """
        try:
            # Set the start and end dates for the transactions
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)

            # Pass `start_date` and `end_date` as `datetime.date` objects
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,  # Pass as `date` object
                end_date=end_date,      # Pass as `date` object
                options=TransactionsGetRequestOptions(
                    account_ids=[account_id], count=500, offset=0)
            )
            response = self.plaid_client.transactions_get(request)
            transactions = response.to_dict().get("transactions", [])

            # Process transactions to identify recurring ones
            recurring_transactions = self.identify_recurring_transactions(
                transactions)

            return {
                "transactions": transactions,
                "recurring_transactions": recurring_transactions
            }
        except Exception as e:
            raise Exception(f"Error fetching transactions: {str(e)}")

    def identify_recurring_transactions(self, transactions):
        """
        Identify recurring transactions based on transaction name and frequency.
        """
        transaction_counts = defaultdict(list)

        # Group transactions by name and store transaction amounts and dates
        for txn in transactions:
            transaction_counts[txn['name']].append({
                "amount": txn['amount'],
                "date": txn['date']
            })

        # Identify recurring transactions (e.g., more than 3 occurrences)
        recurring = []
        for name, txn_list in transaction_counts.items():
            if len(txn_list) >= 3:  # Arbitrary threshold for recurring
                recurring.append({
                    "name": name,
                    "occurrences": len(txn_list),
                    "transactions": txn_list
                })

        return recurring

    def get_liabilities(self, access_token):
        """
        Fetch and return the entire liabilities response for the given access token.
        """
        try:
            request = LiabilitiesGetRequest(access_token=access_token)
            response = self.plaid_client.liabilities_get(request)

            # Convert response to a dictionary
            liabilities = response.to_dict()

            # Sanitize the liabilities fields
            if "liabilities" in liabilities:
                for liability_type in ["mortgage", "student", "credit"]:
                    if liability_type in liabilities["liabilities"]:
                        for item in liabilities["liabilities"][liability_type]:
                            # Replace None with empty strings or default values
                            if item.get("account_number") is None:
                                item["account_number"] = ""

                            # Example: Handle additional fields if needed
                            if "interest_rate" in item and item["interest_rate"].get("percentage") is None:
                                item["interest_rate"]["percentage"] = 0.0

            return liabilities

        except ApiException as e:
            raise Exception(f"Error fetching liabilities: {str(e)}")
