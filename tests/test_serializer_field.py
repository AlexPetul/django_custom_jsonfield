import pytest
from rest_framework import exceptions, serializers

from django_custom_jsonfield.rest_framework.serializers import CustomJSONField


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
            exceptions.ErrorDetail(
                string="Value does not match the JSON schema.",
                code="invalid_data",
            ),
        ],
    }
    assert serializer.errors == expected_errors


@pytest.mark.parametrize(
    "schema",
    [
        {"minItems": "1"},
        {"properties": 1},
        {"pattern": "*invalid.regex"},
    ],
)
def test_map_serializer_field_invalid_schema(schema: dict):
    """Test serializer raises an exception if JSON schema is invalid."""

    with pytest.raises(exceptions.ValidationError) as e:
        CustomJSONField(schema=schema)

    assert isinstance(e.value, exceptions.ValidationError)
    assert e.value.detail[0] == "Invalid JSON schema."
    assert e.value.detail[0].code == "invalid_schema"
