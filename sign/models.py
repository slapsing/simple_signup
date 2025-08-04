from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django import forms
from django.views.generic import TemplateView


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='basic')
        basic_group.user_set.add(user)
        return user

    class IndexView(LoginRequiredMixin, TemplateView):
        template_name = 'protect/index.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
            return context
