from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    """Форма для обновления профиля пользователя."""
    
    class Meta:
        model = User
        fields = ('first_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ваше имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email',
                'required': True
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Этот email уже используется другим пользователем.')
        return email


class DeleteAccountForm(forms.Form):
    """Форма для подтверждения удаления аккаунта."""
    confirm = forms.BooleanField(
        required=True,
        label='Я подтверждаю удаление своего аккаунта',
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Введите ваш пароль для подтверждения'
        }),
        label='Пароль для подтверждения',
        required=True
    )
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Неверный пароль.')
        return password