import pytest
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail

from django_custom_jsonfield.serializers import CustomJSONField


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
    ],
)
def test_validate(value: dict, schema: dict):
    class FakeSerializer(serializers.Serializer):
        json_field = CustomJSONField(schema=schema)

    serializer = FakeSerializer(data={"json_field": value})
    serializer.is_valid()

    expected_errors = {
        "json_field": [
            ErrorDetail(
                string="Value does not match the JSON schema.",
                code="invalid_data",
            ),
        ],
    }
    assert serializer.errors == expected_errors
