import jsonschema
from django.utils.translation import gettext_lazy as _
from jsonschema import validators
from rest_framework import serializers


class CustomJSONField(serializers.JSONField):
    default_error_messages = {
        "invalid_data": _("Value does not match the JSON schema."),
        "invalid_schema": _("Invalid JSON schema."),
    }

    def __init__(self, schema: dict, **kwargs):
        self.schema = schema
        super().__init__(**kwargs)

        validator = validators.validator_for(self.schema)
        try:
            validator.check_schema(self.schema)
        except jsonschema.exceptions.SchemaError:
            self.fail("invalid_schema")

        self.validators.append(self._validate_data)

    def _validate_data(self, value):
        """Validate value against JSON schema."""
        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.exceptions.ValidationError:
            self.fail("invalid_data")
