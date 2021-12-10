from django import forms


class RangeDate(forms.Form):
    start_date = forms.DateField(label='Заезд', required=True,
                                 widget=forms.DateInput(attrs={'class': 'booking-section__calendar-input',
                                                               'type': 'date'}))
    end_date = forms.DateField(label='Выезд', required=True,
                               widget=forms.DateInput(attrs={'class': 'booking-section__calendar-input',
                                                             'type': 'date'}))


class OrderRoom(forms.Form):
    start_date = forms.DateField(label='Заезд', widget=forms.DateInput(attrs={'readonly': True}))
    end_date = forms.DateField(label='Выезд', widget=forms.DateInput(attrs={'readonly': True}))
    name = forms.CharField(label='Имя', max_length=255)
    last_name = forms.CharField(label='Фамилия', max_length=255)
    phone = forms.IntegerField(label='Номер телефона', widget=forms.TextInput(attrs={'type': 'tel'}))
    email = forms.EmailField(label='Email')
