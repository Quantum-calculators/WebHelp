from django import forms

class LinkForm(forms.Form):
    link = forms.CharField(
        widget=forms.DateInput(
            attrs={
                "type": " ",
                "class": "vstav",
                "placeholder": " Вставьте ссылку на сайт",
            }
        )
    )
