from drf_spectacular.drainage import warn
from drf_spectacular.openapi import (
    OpenApiSerializerFieldExtension,
    OpenApiTypes,
    build_array_type,
    build_basic_type,
    build_object_type,
)


class CustomJSONFieldSerializerExtension(OpenApiSerializerFieldExtension):
    target_class = "django_custom_jsonfield.rest_framework.serializers.CustomJSONField"

    def map_serializer_field(self, auto_schema, direction):
        schema = self.target.schema

        try:
            if schema["type"] == "object":
                kwargs = {}
                if "additionalProperties" in schema:
                    kwargs["additionalProperties"] = schema["additionalProperties"]

                return build_object_type(
                    schema["properties"],
                    required=schema.get("required"),
                    description=schema.get("description"),
                    **kwargs,
                )
            elif schema["type"] == "array":
                return build_array_type(
                    schema["items"],
                    min_length=schema.get("minLength"),
                    max_length=schema.get("maxLength"),
                )
            else:
                basic_type_mapping = {
                    "string": OpenApiTypes.STR,
                    "number": OpenApiTypes.NUMBER,
                    "integer": OpenApiTypes.INT,
                    "boolean": OpenApiTypes.BOOL,
                    "null": OpenApiTypes.NONE,
                }

                return build_basic_type(basic_type_mapping[schema["type"]])
        except:  # noqa: E722
            warn(f"Encountered an issue resolving field {schema}, defaulting to string.")
            return build_basic_type(OpenApiTypes.STR)
