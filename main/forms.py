from django import forms 
from .models import AstroUser 
from django.contrib.auth import password_validation 
from django.core.exceptions import ValidationError
from .apps import user_registered
from .models import SuperRubric 
from .models import SubRubric 
from django.contrib.auth.decorators import login_required


#класс для ввода данных пользователя 
class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    class Meta:
        model = AstroUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')


#форма для занесения сведений о новом пользователe
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password_one = forms.CharField(label='Пароль', 
        widget = forms.PasswordInput, 
        help_text = password_validation.password_validators_help_text_html())
    password_two = forms.CharField(label='Пароль(повторно)',
        widget = forms.PasswordInput,
        help_text = 'Введите тот же пароль еще раз для проверки')

    def clean_password_one(self):
        password_one = self.cleaned_data['password_one']
        if password_one:
            password_validation.validate_password(password_one)
        return password_one 

    def clean(self):
        super().clean()
        password_one = self.cleaned_data['password_one']
        password_two = self.cleaned_data['password_two']
        if password_one and password_two and password_one != password_two:
            errors = {'password_two': ValidationError(
                'Введенные вами пароли не совпадают', code = 'password_micmatch')
            }
            raise ValidationError(errors)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password_one'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user)
        return user 
    class Meta:
        model = AstroUser
        fields = ('username', 'email', 'password_one', 'password_two', 'first_name', 'last_name',
                'send_messages')


#создаем поле надрубрики
#@login_required
class SubRubricForm(forms.ModelForm):
    super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(), 
                                            empty_label=None,
                                            label='Надрубрика',
                                            required=True)
    
    class Meta:
        model = SubRubric
        fields = '__all__'


#форма поиска на сайте
#@login_required
class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')

