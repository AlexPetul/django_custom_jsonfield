import jsonschema
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class CustomJSONField(serializers.JSONField):
    default_error_messages = {
        "invalid_data": _("Value does not match the JSON schema."),
    }

    def __init__(self, schema: dict, **kwargs):
        self.schema = schema
        super().__init__(**kwargs)
        self.validators.append(self._validate_data)

    def _validate_data(self, value):
        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.exceptions.ValidationError:
            raise serializers.ValidationError(
                self.default_error_messages["invalid_data"],
                code="invalid_data",
            )
