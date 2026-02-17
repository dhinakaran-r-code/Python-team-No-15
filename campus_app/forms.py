from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, StudentProfile, StaffProfile, Resource, Booking, Department

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-input'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), widget=forms.Select(attrs={'class': 'form-input'}))
    year = forms.ChoiceField(choices=StudentProfile.YEAR_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input'})

class StaffCreationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    password = forms.CharField(widget=forms.PasswordInput())
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
    
    def clean_department(self):
        department = self.cleaned_data['department']
        if StaffProfile.objects.filter(department=department).exists():
            raise ValidationError('This department already has a staff member')
        return department
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.role = 'STAFF'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            StaffProfile.objects.create(user=user, department=self.cleaned_data['department'])
        return user

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['name', 'type', 'capacity', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'type': forms.Select(attrs={'class': 'form-input'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['resource', 'booking_date', 'time_slot']
        widgets = {
            'resource': forms.Select(attrs={'class': 'form-input'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'time_slot': forms.Select(attrs={'class': 'form-input'}, choices=[
                ('09:00-10:00', '09:00 - 10:00'),
                ('10:00-11:00', '10:00 - 11:00'),
                ('11:00-12:00', '11:00 - 12:00'),
                ('12:00-13:00', '12:00 - 13:00'),
                ('14:00-15:00', '14:00 - 15:00'),
                ('15:00-16:00', '15:00 - 16:00'),
                ('16:00-17:00', '16:00 - 17:00'),
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['resource'].queryset = Resource.objects.filter(status='AVAILABLE')
    
    def clean(self):
        cleaned_data = super().clean()
        resource = cleaned_data.get('resource')
        booking_date = cleaned_data.get('booking_date')
        time_slot = cleaned_data.get('time_slot')
        
        if resource and booking_date and time_slot:
            existing = Booking.objects.filter(
                resource=resource,
                booking_date=booking_date,
                time_slot=time_slot
            ).exclude(status='REJECTED')
            if existing.exists():
                raise ValidationError('This resource is already booked for the selected time slot')
        
        return cleaned_data

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'code': forms.TextInput(attrs={'class': 'form-input'}),
        }
