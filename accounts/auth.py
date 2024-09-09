from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Get the token from the cookie
        token = request.COOKIES.get('access_token')

        if not token:
            return None
        
        try:
            # Validate and decode the token
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            
            if user is None:
                raise AuthenticationFailed('No user associated with this token.')
            
            # Attach the user to the request object
            request.user = user
            
            return (user, validated_token)
        except AuthenticationFailed:
            raise AuthenticationFailed('Invalid token')
