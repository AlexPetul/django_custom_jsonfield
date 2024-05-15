import pytest
from django.core import checks
from django.db import models

from django_custom_jsonfield.fields import CustomJSONField


@pytest.mark.parametrize(
    "schema",
    [
        {"minItems": "1"},
        {"properties": 1},
        {"pattern": "*invalid.regex"},
    ],
)
def test_model_check_invalid_schema(schema: dict):
    class FakeModel(models.Model):
        json_field = CustomJSONField(schema=schema)

        class Meta:
            app_label = "test_app"

    instance = FakeModel()
    errors = instance.check()
    expected_errors = [
        checks.Error(
            "Provided JSON schema for field 'json_field' is invalid.",
            obj=CustomJSONField,
            id="fields.J0001",
        )
    ]

    assert errors == expected_errors
