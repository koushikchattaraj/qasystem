from django.contrib.auth.backends import ModelBackend, UserModel
from .models import User
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        print(email,"//////")
        print(password,"-------")
        usermodel = get_user_model()
        print(usermodel)
        try:
            user = usermodel.objects.get(Q(email__iexact=email)| Q(username__iexact=email) )
            if user:
                if user.check_password(password):
                    return user
        except usermodel.DoesNotExist:
            print("User Dose Not Exits")
       