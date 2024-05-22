from typing import Any

import pytest
from django import VERSION as DJANGO_VERSION
from django.core import checks
from django.core.exceptions import ValidationError
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
def test_json_schema_invalid(schema: dict):
    """Test Django returns errors if JSON schema is invalid."""

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


def test_json_schema_ok():
    class FakeModel(models.Model):
        json_field = CustomJSONField(
            schema={
                "type": "array",
                "minLength": 1,
                "maxLength": 1,
                "items": {"type": "integer"},
            },
        )

        class Meta:
            app_label = "test_app"

    instance = FakeModel()
    assert instance.check() == []


@pytest.mark.parametrize(
    "schema",
    [10, 10.00, list(), tuple(), set(), "", b"", True, None],
)
def test_schema_type_invalid(schema: Any):
    """Test Django raises exception if JSON schema is not typed correctly."""

    with pytest.raises(ValueError) as e:
        CustomJSONField(schema=schema)

    assert e.value.args[0] == "The schema parameter must be a dictionary."


@pytest.mark.parametrize(
    "value,schema",
    [
        (
            {"name": "John"},
            {
                "type": "object",
                "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
                "required": ["name", "age"],
            },
        ),
        (
            "invalid_string",
            {
                "const": "custom_string",
            },
        ),
    ],
)
def test_validate_value_against_schema(value: Any, schema: Any):
    """Test Django raises exception if value doesn't match JSON schema."""

    class FakeModel(models.Model):
        json_field = CustomJSONField(schema=schema)

        class Meta:
            app_label = "test_app"

    instance = FakeModel()
    instance.json_field = value

    with pytest.raises(ValidationError) as e:
        instance.clean_fields()

    assert isinstance(e.value.args[0]["json_field"][0], ValidationError)
    assert e.value.args[0]["json_field"][0].args[0] == "Value does not match the JSON schema."
    assert e.value.args[0]["json_field"][0].args[1] == "invalid_data"
    assert e.value.args[0]["json_field"][0].args[2] == {"value": value}


def test_deconstruct():
    json_field = CustomJSONField(schema={})
    _, _, _, kwargs = json_field.deconstruct()
    assert "schema" in kwargs


@pytest.mark.skipif(DJANGO_VERSION < (4, 1), reason="non_db_attrs is only available in Django 4.1+")
def test_non_db_attrs():
    json_field = CustomJSONField(schema={})
    assert "schema" in json_field.non_db_attrs
