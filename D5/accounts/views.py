from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import SignUpForm

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user
