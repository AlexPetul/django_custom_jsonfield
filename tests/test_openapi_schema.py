from typing import Any
from unittest.mock import Mock

import pytest

from django_custom_jsonfield.rest_framework.openapi import CustomJSONFieldSerializerExtension
from django_custom_jsonfield.rest_framework.serializers import CustomJSONField


@pytest.mark.parametrize(
    "schema",
    [
        {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
            "additionalProperties": True,
        },
        {
            "type": "object",
            "properties": {"name": {"type": "string"}},
        },
        {
            "items": {"type": "integer"},
            "type": "array",
            "maxLength": 1,
            "minLength": 1,
        },
        {
            "items": {"type": "integer"},
            "type": "array",
        },
        {
            "type": "number",
        },
        {
            "type": "string",
        },
        {
            "type": "integer",
        },
        {
            "type": "boolean",
        },
    ],
)
def test_map_serializer_field_ok(schema: dict):
    json_field = CustomJSONField(schema=schema)
    extension = CustomJSONFieldSerializerExtension(json_field)
    data = extension.map_serializer_field(Mock(), "response")
    assert data == schema


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
        {
            "type": "test",
        },
    ],
)
def test_map_serializer_field_invalid_schema(schema: dict):
    json_field = CustomJSONField(schema=schema)
    extension = CustomJSONFieldSerializerExtension(json_field)
    data = extension.map_serializer_field(Mock(), "response")
    assert data == {"type": "string"}
