from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove default help texts for cleaner UI
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        role = self.cleaned_data.get('role')

        if role == 'organiser' and not password.startswith('admin'):
            raise forms.ValidationError("Organiser password must start with 'admin'")
        return password

    from django import forms
from .models import Disaster

class DisasterForm(forms.ModelForm):
    class Meta:
        model = Disaster
        fields = [
            'title', 'description', 'location', 'urgency_level', 'image',
            'bank_account_name', 'bank_account_number', 'ifsc_code', 'upi_id'
        ]


from .models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'message']


from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'})
        }
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your feedback...'})
        }

from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

        from django import forms
from .models import Donation
import re

class ManualDonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', 'transaction_id', 'proof_image', 'message']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter valid transaction ID'}),
            'proof_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Optional message'}),
        }

    def clean_transaction_id(self):
        txn_id = self.cleaned_data.get('transaction_id')
        if not re.match(r'^[A-Za-z0-9\-]{8,}$', txn_id):
            raise forms.ValidationError("Transaction ID must be at least 8 characters and alphanumeric.")
        return txn_id

