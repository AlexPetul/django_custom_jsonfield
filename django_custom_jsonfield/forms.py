from django.forms.fields import JSONField


class CustomJSONField(JSONField):
    default_error_messages = {
        "invalid_schema",
    }
