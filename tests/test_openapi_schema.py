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
