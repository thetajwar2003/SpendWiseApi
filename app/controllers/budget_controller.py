class BudgetController:
    def __init__(self, budget_model):
        self.budget_model = budget_model

    def create_budget(self, user_id, category, amount):
        self.budget_model.create_budget(user_id, category, amount)
        return {"message": "Budget created successfully"}, 201

    def get_budgets(self, user_id):
        budgets = self.budget_model.get_budgets(user_id)
        return {"budgets": budgets}, 200

    def update_budget(self, user_id, category, new_amount):
        self.budget_model.update_budget(user_id, category, new_amount)
        return {"message": "Budget updated successfully"}, 200

    def delete_budget(self, user_id, category):
        self.budget_model.delete_budget(user_id, category)
        return {"message": "Budget deleted successfully"}, 200
