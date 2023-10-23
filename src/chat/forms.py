from django import forms
from django.utils.translation import gettext_lazy
from . import models

User = models.User

class SearchForm(forms.Form):
    keywords = forms.CharField(
        label=gettext_lazy('keywords (split space)'),
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': gettext_lazy('Enter the room name.'),
            'class': 'form-control',
        }),
    )

    def get_keywords(self):
        init_keywords = ''
        keywords = init_keywords

        if self.is_valid():
            keywords = self.cleaned_data.get('keywords', init_keywords)

        return keywords

class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = ('name', 'description', 'participants')
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': gettext_lazy('Enter the room name.'),
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'cols': 10,
                'style': 'resize: none',
                'placeholder': gettext_lazy('Enter the description.'),
                'class': 'form-control',
            }),
            'participants': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.filter(is_staff=False)

class _ConfigForm(forms.ModelForm):
    class Meta:
        model = models.Config
        fields = ('owner', 'order', 'offset')
        labels = {
            'order': gettext_lazy('Ordering'),
            'offset': gettext_lazy('Offset'),
        }
        widgets = {
            'owner': forms.HiddenInput(),
            'order': forms.NumberInput(attrs={
                'placeholder': gettext_lazy('Enter the ordering'),
                'class': 'form-control',
                'min': '1',
                'step': '1',
            }),
            'offset': forms.NumberInput(attrs={
                'placeholder': gettext_lazy('Enter the offset'),
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'step': '1',
            }),
        }

class _BaseConfigFormSet(forms.BaseModelFormSet):
    def clean(self):
        super().clean()

        # if errors exist, this process is interruptedinterrupted
        if any(self.errors):
            return

        orders = [form.cleaned_data.get('order') for form in self.forms if form not in self.deleted_forms]
        uniq = set(orders)

        if len(orders) != len(uniq):
            raise forms.ValidationError(gettext_lazy("Set the participant's order to uniquely determine the move number."))

ConfigFormSet = forms.modelformset_factory(model=models.Config, form=_ConfigForm, formset=_BaseConfigFormSet, extra=0, max_num=0)
