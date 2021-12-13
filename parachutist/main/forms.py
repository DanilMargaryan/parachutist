from django import forms
from main import models


class RangeDate(forms.Form):
    start_date = forms.DateField(label='Заезд', required=True,
                                 widget=forms.DateInput(attrs={'class': 'booking-section__calendar-input',
                                                               'type': 'date'}))
    end_date = forms.DateField(label='Выезд', required=True,
                               widget=forms.DateInput(attrs={'class': 'booking-section__calendar-input',
                                                             'type': 'date'}))


class OrderRoom(forms.Form):
    error_css_class = 'is-invalid'

    start_date = forms.DateField(label='Заезд', widget=forms.DateInput(attrs={'readonly': True, 'class': 'form-control'}))
    end_date = forms.DateField(label='Выезд', widget=forms.DateInput(attrs={'readonly': True, 'class': 'form-control'}))
    name = forms.CharField(label='Имя', max_length=255, widget=forms.DateInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', max_length=255, widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label='Номер телефона', widget=forms.TextInput(attrs={'type': 'tel', 'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self):
        for field in self.errors:
            self[field].field.widget.attrs['class'] += ' ' + self.error_css_class
