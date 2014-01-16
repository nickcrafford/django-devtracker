from django import forms

class UserForm(forms.Form):
    username        = forms.CharField(max_length=50)
    email           = forms.EmailField()
    password        = forms.CharField(widget=forms.PasswordInput)
    password_2      = forms.CharField(widget=forms.PasswordInput)

    def clean_password_2(self):
        password_2 = self.cleaned_data['password_2']
        try:
            password = self.cleaned_data['password']
        except:
            password = None
        if password == None or password != password_2:
            raise forms.ValidationError("Passwords do not match")
        return password

class ProfileForm(forms.Form):
    billing_name         = forms.CharField()
    billing_address      = forms.CharField()
    billing_city         = forms.CharField()
    billing_state        = forms.CharField()
    billing_postal       = forms.CharField()
    weekly_revenue_goal  = forms.DecimalField(required=False)
    monthly_revenue_goal = forms.DecimalField(required=False)
    yearly_revenue_goal  = forms.DecimalField(required=False)
    tax_bracket          = forms.IntegerField(required=False)