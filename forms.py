#from django.forms import ModelForm
from django import forms
from .models import Plan
import operator
from django.forms import widgets
import re


class UserForm(forms.Form):

    STATUS_USER = (
        ('+', 'действующий'),
        ('-', 'не активный')
    )

    ERRORS_CH_F = {'required': 'поле нужно заполнить'}
    ERRORS_E_F = {'required': 'поле нужно заполнить',
                  'invalid': 'формат x@x.xx'}

    f_name = forms.CharField(label='Имя', max_length=50, error_messages=ERRORS_CH_F)
    l_name = forms.CharField(label='Фамилия', max_length=50, error_messages=ERRORS_CH_F)
    adress = forms.CharField(label='Адресс', max_length=100, error_messages=ERRORS_CH_F)
    email = forms.EmailField(max_length=50, error_messages=ERRORS_E_F)
    tel = forms.CharField(label='Телефон', max_length=100, error_messages=ERRORS_CH_F)
    name_plan = forms.ChoiceField(label='тарифный план', required=False, choices=Plan.objects.values_list('name','name'), initial='не выбран')
    status = forms.ChoiceField(label='статус абонента', choices=STATUS_USER, required=True, initial='-')
    descript = forms.CharField(label='Примечание', max_length=500, required=False)

# initial='-' в поле выводиться значение при отсутствии переданых значений
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['name_plan'] = forms.ChoiceField(label='тарифный план', required=False, choices=Plan.objects.values_list('name','name'), initial='не выбран')

    def clean_f_name(self):
        data = self.cleaned_data['f_name']
        chk = re.match('^[\D]+$', data)
        if chk is None:
            raise forms.ValidationError("цифры не допустимы")
       # Always return the cleaned data, whether you have changed it or
       # not.
        return data

    def clean_l_name(self):
        data = self.cleaned_data['l_name']
        chk = re.match('^[\D]+$', data)
        if chk is None:
            raise forms.ValidationError("цифры не допустимы")
       # Always return the cleaned data, whether you have changed it or
       # not.
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        chk = re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',data)
        if chk is None:
            raise forms.EmailValidator("некорректный e-mail", code='invalid')
       # Always return the cleaned data, whether you have changed it or
       # not.
        return data

    def clean_tel(self):
        data = self.cleaned_data['tel']
        chk = re.match('(^\(\d{3}\)\d{7}$|^\d{7}$)',data)
        if chk is None:
            raise forms.ValidationError("формат (123)1234567 или 4301234")
       # Always return the cleaned data, whether you have changed it or
       # not.
        return data

class PlanForm(forms.Form):

    STATUS_PLAN = (
        ('+', 'действует'),
        ('-', 'архивный')
    )
    ERRORS_CH_F = {'required': 'поле нужно заполнить'}
    ERRORS_D_F = {'required': 'поле нужно заполнить',
                  'invalid': 'формат 00.00.0000'}

    FORMAT_INPUT = [ # установка валидных форматов при вводе даты в поле на форме input_formats=FORMAT_INPUT
        '%d.%m.%Y',
        '%d.%m.%y',
        '%m/%d/%Y',       # '10/25/2006'
        '%m/%d/%y'       # '10/25/06'
    ]

    name = forms.CharField(label = 'Тарифный план', max_length=100, error_messages=ERRORS_CH_F)
    price = forms.CharField(label = 'грн/день (0.00)', max_length=8, error_messages=ERRORS_CH_F)
    relise_date = forms.DateField(label='действует с', input_formats=FORMAT_INPUT, widget=forms.DateInput(format="%d.%m.%Y"), error_messages=ERRORS_D_F)
    expired_date = forms.DateField(label='снят с', required=False, input_formats=FORMAT_INPUT, widget=forms.DateInput(format="%d.%m.%Y"), initial='01.01.1900', error_messages=ERRORS_D_F)
    status = forms.ChoiceField(label='статус тарифного плана', choices=STATUS_PLAN)

    def clean_price(self):
        data = self.cleaned_data['price']
        chk = re.match('^\d{1,5}[,\.]\d{2}$',data)
        if chk is None:
            raise forms.ValidationError("формат: 0.00 или 0")
       # Always return the cleaned data, whether you have changed it or
       # not.
        return data



# widget=forms.DateInput(format="%d.%m.%Y") формат отображения даты в поле на форме после принятия datetime типа 