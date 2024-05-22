from typing import Any
from unittest.mock import Mock, patch

import pytest

from django_custom_jsonfield.rest_framework.openapi import CustomJSONFieldSerializerExtension
from django_custom_jsonfield.rest_framework.serializers import CustomJSONField


@pytest.mark.parametrize(
    "schema,expected",
    [
        (
            {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": True,
            },
            {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": True,
            },
        ),
        (
            {
                "type": "object",
                "properties": {"name": {"type": "string"}},
            },
            {
                "type": "object",
                "properties": {"name": {"type": "string"}},
            },
        ),
        (
            {
                "items": {"type": "integer"},
                "type": "array",
                "maxLength": 1,
                "minLength": 1,
            },
            {
                "items": {"type": "integer"},
                "type": "array",
                "maxLength": 1,
                "minLength": 1,
            },
        ),
        (
            {
                "items": {"type": "integer"},
                "type": "array",
            },
            {
                "items": {"type": "integer"},
                "type": "array",
            },
        ),
        # basic types
        ({"type": "number"}, {"type": "number"}),
        ({"type": "string"}, {"type": "string"}),
        ({"type": "integer"}, {"type": "integer"}),
        ({"type": "boolean"}, {"type": "boolean"}),
    ],
)
def test_map_serializer_field_ok(schema: Any, expected: Any):
    """Test correct mapping of JSON schema to OpenAPI schema."""

    json_field = CustomJSONField(schema=schema)
    extension = CustomJSONFieldSerializerExtension(json_field)
    data = extension.map_serializer_field(Mock(), "response")
    assert data == expected


@pytest.mark.parametrize(
    "schema,expected",
    [
        ({"const": 10}, {"enum": [10]}),  # integer
        ({"const": 10.00}, {"enum": [10.00]}),  # float
        ({"const": 10.00}, {"enum": [10.00]}),  # bytes
        ({"const": "string"}, {"enum": ["string"]}),  # string
        ({"const": True}, {"enum": [True]}),  # bool
        ({"const": None}, None),  # none
        ({"const": {"k": "v", "k2": 10}}, {"enum": [{"k": "v", "k2": 10}]}),  # dict
        ({"const": [10, 20]}, {"enum": [[10, 20]]}),  # list
    ],
)
def test_map_serializer_field_const(schema: dict, expected: Any):
    """Test basic types declared as const in JSON schema."""

    json_field = CustomJSONField(schema=schema)
    extension = CustomJSONFieldSerializerExtension(json_field)
    data = extension.map_serializer_field(Mock(), "response")
    assert data == expected


@pytest.mark.parametrize(
    "schema",
    [
        {"type": "unknown_type"},
    ],
)
@patch(
    "django_custom_jsonfield.rest_framework.serializers.jsonschema.validators.validator_for",
    new=Mock(),
)
def test_map_serializer_field_fallback(schema: Any):
    """Test fallback to string."""

    json_field = CustomJSONField(schema=schema)
    extension = CustomJSONFieldSerializerExtension(json_field)
    data = extension.map_serializer_field(Mock(), "response")
    assert data == {"type": "string"}
