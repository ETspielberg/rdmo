from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import AdditionalField, AdditionalFieldValue


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': _('First name')})
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': _('Last name')})

        self.additional_fields = AdditionalField.objects.all()
        self.additional_values = self.instance.additional_values.all()

        # add fields and init values for the Profile model
        for additional_field in self.additional_fields:

            if additional_field.type == 'text':
                field = forms.CharField(widget=forms.TextInput(attrs={'placeholder': additional_field.text}))
            elif additional_field.type == 'textarea':
                field = forms.CharField(widget=forms.Textarea(attrs={'placeholder': additional_field.text}))
            else:
                raise Exception('Unknown additional_field type.')

            field.label = additional_field.text
            field.help = additional_field.help
            field.required = additional_field.required

            self.fields[additional_field.key] = field

        for additional_field_value in self.additional_values:
            self.fields[additional_field.key].initial = additional_field_value.value

    def save(self, *args, **kwargs):
        super(ProfileForm, self).save(*args, **kwargs)
        self._save_additional_values()

    def _save_additional_values(self, user=None):
        if user is None:
            user = self.instance

        for additional_field in self.additional_fields:
            try:
                additional_value = user.additional_values.get(field=additional_field)
            except AdditionalFieldValue.DoesNotExist:
                additional_value = AdditionalFieldValue(user=user, field=additional_field)

            additional_value.value = self.cleaned_data[additional_field.key]
            additional_value.save()


class SignupForm(ProfileForm):

    def signup(self, request, user):
        self._save_additional_values(user)
