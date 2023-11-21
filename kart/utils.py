from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Graphql__JWT need username in Token
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add username in Token
        token['username'] = user.username
        return token
