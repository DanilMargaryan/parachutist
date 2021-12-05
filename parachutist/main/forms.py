from django import forms


class RangeDate(forms.Form):
    start_date = forms.DateField(label='Заезд', required=False,
                                 widget=forms.TextInput(attrs={'class': 'booking-section__calendar-input',
                                                               'type': 'date'}))
    end_date = forms.DateField(label='Выезд', required=False,
                               widget=forms.TextInput(attrs={'class': 'booking-section__calendar-input',
                                                             'type': 'date'}))
