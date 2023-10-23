from django import template
from django.contrib.auth import get_user_model
import re
register = template.Library()
User = get_user_model()

@register.filter(name='conv_fkey2user')
def convert_from_foreignkey_to_usermodel(boundfield):
    matched = re.search('(?<=value=")(\d+)', str(boundfield))
    user = User.objects.get(pk=int(matched.group(0)))

    return user