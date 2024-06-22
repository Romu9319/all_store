from django import forms

class DateInput(forms.DateInput):
    input_type="date"

class ClientForm(forms.Form):

    CHOICE_GENDER = (
        ("M", "Male"),
        ("F", "Female")
    )

    name = forms.CharField(label="Name", max_length=50, required=True,  widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label="Last name", max_length=50, required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    address = forms.CharField(label="Address", max_length=50,widget=forms.Textarea(attrs={'class':'form-control', 'rows':2}))
    phone = forms.CharField(label="Phone", max_length=20, widget=forms.TextInput(attrs={'class':'form-control'}))
    gender = forms.ChoiceField(label="Gender", choices=CHOICE_GENDER, widget=forms.Select(attrs={'class':'form-control'}))
    birthdate = forms.DateField(label="Birthdate", input_formats=['%Y-%m-%d'], widget=DateInput(attrs={'class':'form-control'}))