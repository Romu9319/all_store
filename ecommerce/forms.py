from django import forms

class DateInput(forms.DateInput):
    input_type="date"

class ClientForm(forms.Form):

    CHOICE_GENDER = (
        ("M", "Male"),
        ("F", "Female")
    )

    name = forms.CharField(label="Name", max_length=50, required=True)
    last_name = forms.CharField(label="Last name", max_length=50, required=True)
    email = forms.EmailField(label="Email", required=True)
    address = forms.CharField(label="Address", max_length=50,widget=forms.Textarea)
    phone = forms.CharField(label="Phone", max_length=20)
    gender = forms.ChoiceField(label="Gender", choices=CHOICE_GENDER)
    birthdate = forms.DateField(label="Birthdate", input_formats=['%Y-%m-%d'], widget=DateInput())