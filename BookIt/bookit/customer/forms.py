import datetime
from django import forms
from django.forms import widgets, fields
from common.models import CType



class RegisterForm(forms.Form):
    login_type_choices = (
        (0, 'Resource Provider'),
        (1, 'Resource User')
    )

    login_type = forms.ChoiceField(
        disabled=True,
        label='Login Role',
        widget=forms.Select(attrs={'class': 'form-select', }),
        choices=login_type_choices,
        initial=login_type_choices[0],
    )
    username = forms.CharField(
        disabled=True,
        label='username',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username',
        })
    )
    password1 = forms.CharField(
        disabled=True,
        label='password',
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        )
    )
    password2 = forms.CharField(
        disabled=True,
        label='password-confirm',
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password-confirm',
            }
        )
    )
    phone = forms.CharField(
        disabled=True,
        label='phone',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'phone',
        })
    )
    email = forms.EmailField(
        disabled=True,
        label='email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email-address',
            }
        )
    )
    vcode = forms.CharField(
        label='vcode',
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'vcode',
            }
        )
    )


class PreRegisterForm(forms.Form):
    login_type_choices = (
        (0, 'Resource Provider'),
        (1, 'Resource User')
    )

    login_type = forms.ChoiceField(
        label='Login Role',
        widget=forms.Select(attrs={'class': 'form-select', }),
        choices=login_type_choices,
        initial=login_type_choices[0],
    )
    username = forms.CharField(
        label='username',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username',
        })
    )
    password1 = forms.CharField(
        label='password',
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        )
    )
    password2 = forms.CharField(
        label='password-confirm',
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password-confirm',
            }
        )
    )
    phone = forms.CharField(
        label='phone',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'phone',
        })
    )
    email = forms.EmailField(

        label='email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email-address',
            }
        )
    )


class LoginForm(forms.Form):
    login_type_choices = (
        (0, 'Resource Provider'),
        (1, 'Resource User')
    )

    login_type = forms.ChoiceField(
        label='Login Role',
        widget=forms.Select(attrs={'class': 'form-select', }),
        choices=login_type_choices,
        initial=login_type_choices[1],
    )

    email = forms.EmailField(

        label='email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email-address',
            }
        )
    )
    password = forms.CharField(
        label='password',
        max_length=20,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        )
    )


class IsLogin(forms.Form):
    role_type = forms.CharField(
        label='role_type',
        max_length=2,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'role_type',
            }
        )
    )

    role_id = forms.CharField(
        label='role_id',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'role_id',
            }
        )
    )

    role_name = forms.CharField(
        label='role_name',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'role_name',
            }
        )
    )


# class PasswordFrom(forms.Form):
#     email = forms.EmailField(
#         label='email',
#         max_length=200,
#         widget=forms.EmailInput(
#             attrs={
#                 'class':'form-control',
#                 'placeholder':'email'
#             }
#         )
#     )
#

class newcourtform(forms.Form):
    timechoice = (
        (-1, 'Close'), (-2, '24-hour Open'),
        (0, '12:00 midnight'), (1, '1:00 am'), (2, '2:00 am'), (3, '3:00 am'), (4, '4:00 am'), (5, '5:00 am'),
        (6, '6:00 am'), (7, '7:00 am'), (8, '8:00 am'), (9, '9:00 am'), (10, '10:00 am'), (11, '11:00 am'),
        (12, '12:00 noon'),
        (13, '1:00 pm'), (14, '2:00 pm'), (15, '3:00 pm'), (16, '4:00 pm'), (17, '5:00 pm'), (18, '6:00 pm'),
        (19, '7:00 pm'), (20, '8:00 pm'), (21, '9:00 pm'), (22, '10:00 pm'), (23, '11:00pm'),
        (24, '12:00 midnight(next day)')
    )

    court_type = fields.ChoiceField(
        required='required',
        label='Court Type',
        widget=widgets.Select(attrs={
            'class': 'form-select',
            'placeholder': "Choice Your Venue's Type Here.",
        }),

        choices=[]

    )
    courtname = forms.CharField(
        required='required',
        label='Court Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Type Your Venue Name Here.',
        })
    )

    courtaddress = forms.CharField(
        required='required',
        label='CourtAddress',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Type Venue Address Here.'
            }
        ),
    )
    courtcapacity = forms.IntegerField(
        required='required',
        label='Court Capacity',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': "Type Your Venue's Capacity Here."
            }
        )
    )
    monb = forms.ChoiceField(
        label="Monday Start Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    mone = forms.ChoiceField(
        label='Monday End Time:',
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),

    )
    tueb = forms.ChoiceField(
        label="Tuesday Start Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    tuee = forms.ChoiceField(
        label="Tuesday End Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    wedb = forms.ChoiceField(
        label="Wednesday Start Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    wede = forms.ChoiceField(
        label="Wednesday End Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    thub = forms.ChoiceField(
        label="Thursday Start Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    thue = forms.ChoiceField(
        label="Thursday End Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    frib = forms.ChoiceField(
        label="Friday Start Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    frie = forms.ChoiceField(
        label="Friday End Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    satb = forms.ChoiceField(
        label="Saturday Start Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    sate = forms.ChoiceField(
        label="Saturday End Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    sunb = forms.ChoiceField(
        label="Sunday Start Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )
    sune = forms.ChoiceField(
        label="Sunday End Time:",
        choices=timechoice,
        widget=forms.Select(attrs={
            'class': 'form-select',

        }),

    )

    courtintro = forms.CharField(
        label='Court Intro',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Court Info',
                'style': "height: 200px;word-break:break-all"
            })
    )

    def __init__(self, *args, **kwargs):
        super(newcourtform, self).__init__(*args, **kwargs)

        self.fields['court_type'].choices = CType.objects.values_list('id', 'TypeName')


class SearchFrom(forms.Form):
    begin = forms.DateTimeField(
        label="Time Begin:",
        widget=forms.DateTimeInput(
            attrs={
                'class': 'date form-control',
                'type': 'datetime-local',
                'max': str(datetime.date.today())[:10],
                'min': str(datetime.date.today())[:10],
            }
        ),
        required=False
    )
    end = forms.DateTimeField(
        label="Time End:",
        widget=forms.DateTimeInput(
            attrs={
                'class': 'date form-control',
                'type': 'datetime-local',
                'max': str(datetime.date.today())[:10],
                'min': str(datetime.date.today())[:10],
            }
        ),
        required=False

    )
    keyword = forms.CharField(
        label="Keyword",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Keyword Here!'
            }
        ),
        required=False
    )
