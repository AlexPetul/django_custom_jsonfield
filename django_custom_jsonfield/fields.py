import jsonschema
from django.core import checks, exceptions
from django.db import models
from django.utils.translation import gettext_lazy as _
from jsonschema import validators


class CustomJSONField(models.JSONField):
    default_error_messages = {
        "invalid_data": _("Value does not match the JSON schema."),
    }

    def __init__(self, schema: dict, **kwargs):
        if not isinstance(schema, dict):
            raise ValueError("The schema parameter must be a dictionary.")
        self.schema = schema
        super().__init__(**kwargs)

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ("schema",)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_jsonschema(),
        ]

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        try:
            jsonschema.validate(value, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.ValidationError(
                self.error_messages["invalid_data"],
                code="invalid_data",
                params={"value": value},
            ) from e

    def _check_jsonschema(self):
        """Check that the JSON schema is valid."""
        validator = validators.validator_for(self.schema)
        try:
            validator.check_schema(self.schema)
        except jsonschema.exceptions.SchemaError:
            return [
                checks.Error(
                    f"Provided JSON schema for field '{self.name}' is invalid.",
                    obj=self.__class__,
                    id="fields.J0001",
                )
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["schema"] = self.schema
        return name, path, args, kwargs
