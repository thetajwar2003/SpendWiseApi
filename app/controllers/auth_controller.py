from botocore.exceptions import ClientError
from ..utils.calculate_secret_hash import calculate_secret_hash
from botocore.exceptions import ClientError as DynamoDBClientError


class AuthController:
    def __init__(self, cognito, user_model, config):
        self.cognito = cognito
        self.user_model = user_model
        self.user_pool_id = config['COGNITO_USER_POOL_ID']
        self.app_client_id = config['COGNITO_APP_CLIENT_ID']
        self.app_client_secret = config['COGNITO_APP_CLIENT_SECRET']

    from botocore.exceptions import ClientError as DynamoDBClientError

    def register_user(self, email, password, first_name, last_name):
        try:
            # Calculate the SECRET_HASH
            secret_hash = calculate_secret_hash(
                self.app_client_id, self.app_client_secret, email)

            # Register the user with Cognito
            response = self.cognito.sign_up(
                ClientId=self.app_client_id,
                SecretHash=secret_hash,  # Include SECRET_HASH
                Username=email,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'given_name', 'Value': first_name},
                    {'Name': 'family_name', 'Value': last_name},
                ]
            )

            # Extract the Cognito-generated user ID
            print("Cognito sign_up response:", response)
            user_id = response.get('UserSub')

            # Ensure user_id exists
            if not user_id:
                raise ValueError("UserSub not found in Cognito response")

            # Store user data in DynamoDB
            print(
                f"Creating user in DynamoDB: {user_id}, {email}, {first_name}, {last_name}")
            self.user_model.create_user(user_id, email, first_name, last_name)

            return {"message": "User registered successfully", "user_id": user_id}, 201

        except self.cognito.exceptions.UsernameExistsException:
            return {"error": "User already exists"}, 400
        except DynamoDBClientError as e:
            print("DynamoDB error:", e)
            return {"error": f"Error storing user in DynamoDB: {str(e)}"}, 500
        except ClientError as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500
        except ValueError as ve:
            return {"error": f"Unexpected error: {str(ve)}"}, 500

    def login_user(self, email, password):
        """
        Log in a user using AWS Cognito and return tokens.
        """
        try:
            # Check if the App Client has a client secret
            auth_parameters = {
                'USERNAME': email,
                'PASSWORD': password
            }

            # Only add SecretHash if App Client has a client secret
            if self.app_client_secret:
                secret_hash = calculate_secret_hash(
                    self.app_client_id, self.app_client_secret, email)
                auth_parameters['SECRET_HASH'] = secret_hash

            # Authenticate the user with Cognito
            response = self.cognito.initiate_auth(
                ClientId=self.app_client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters=auth_parameters
            )

            # Return tokens and a success message
            auth_result = response['AuthenticationResult']
            return {
                "message": "Login successful",
                "access_token": auth_result['AccessToken'],
                "refresh_token": auth_result['RefreshToken'],
                "id_token": auth_result['IdToken'],
            }, 200

        except self.cognito.exceptions.NotAuthorizedException:
            return {"error": "Invalid credentials"}, 401
        except self.cognito.exceptions.UserNotFoundException:
            return {"error": "User not found"}, 404
        except ClientError as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500
