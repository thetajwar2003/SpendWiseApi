import json


class AuthController:
    def __init__(self, cognito, user_model):
        self.cognito = cognito
        self.user_model = user_model

    def register_user(self, email, password, first_name, last_name):
        try:
            response = self.cognito.sign_up(
                ClientId=self.cognito.meta.client.meta.service_model.service_id,
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'name', 'Value': f"{first_name} {last_name}"},
                ]
            )
            user_id = response['UserSub']
            self.user_model.create_user(user_id, email, first_name, last_name)
            return {"message": "User registered successfully", "user_id": user_id}, 201
        except self.cognito.exceptions.UsernameExistsException:
            return {"error": "User already exists"}, 400

    def login_user(self, email, password):
        try:
            response = self.cognito.initiate_auth(
                ClientId=self.cognito.meta.client.meta.service_model.service_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            return {
                "message": "Login successful",
                "access_token": response['AuthenticationResult']['AccessToken'],
                "refresh_token": response['AuthenticationResult']['RefreshToken']
            }, 200
        except self.cognito.exceptions.NotAuthorizedException:
            return {"error": "Invalid credentials"}, 401
