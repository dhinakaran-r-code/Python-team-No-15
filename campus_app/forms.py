from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, StudentProfile, Department, UserRole, Booking, Resource

class StudentRegistrationForm(UserCreationForm):
    department = forms.ChoiceField(choices=Department.choices, required=True)
    year = forms.ChoiceField(
        choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], 
        required=True
    )
    is_representative = forms.BooleanField(required=False, label="Are you a Class Representative?")
    email = forms.EmailField(required=True) # Ensure unique email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = UserRole.STUDENT
        user.email = self.cleaned_data['email'] # Ensure email is saved
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                department=self.cleaned_data['department'],
                year=self.cleaned_data['year'],
                is_representative=self.cleaned_data['is_representative']
            )
        return user

class LoginForm(AuthenticationForm):
    # Custom styling can be added here or in widget attributes
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['resource', 'booking_date', 'start_time', 'end_time']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'resource': forms.Select(attrs={'class': 'form-select'}),
        }

class RejectionForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=True, label="Reason for Rejection")

class AdminBookingForm(forms.Form):
    resource = forms.ModelChoiceField(queryset=Resource.objects.all(), widget=forms.Select(attrs={'class': 'form-select'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), initial='09:00')
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), initial='17:00')

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("End time must be after start time.")
        
        return cleaned_data
