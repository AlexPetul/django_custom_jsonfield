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

    def build_object_schema(self, schema: dict):
        kwargs = {}
        if "additionalProperties" in schema:
            kwargs["additionalProperties"] = schema["additionalProperties"]

        return build_object_type(
            schema["properties"],
            required=schema.get("required"),
            description=schema.get("description"),
            **kwargs,
        )

    def build_array_schema(self, schema: dict):
        return build_array_type(
            schema["items"],
            min_length=schema.get("minLength"),
            max_length=schema.get("maxLength"),
        )

    def build_basic_schema(self, schema: dict):
        basic_type_mapping = {
            "string": OpenApiTypes.STR,
            "number": OpenApiTypes.NUMBER,
            "integer": OpenApiTypes.INT,
            "boolean": OpenApiTypes.BOOL,
            "null": OpenApiTypes.NONE,
        }

        schema_type = schema["type"]
        if schema_type not in basic_type_mapping:
            raise KeyError(f"Unknown schema type: {schema_type}")

        return build_basic_type(basic_type_mapping[schema_type])

    def map_serializer_field(self, auto_schema, direction):
        schema = self.target.schema

        if "const" in schema:
            if schema["const"] is None:
                return None

            return {"enum": [schema["const"]]}

        try:
            if schema["type"] == "object":
                return self.build_object_schema(schema)
            elif schema["type"] == "array":
                return self.build_array_schema(schema)
            else:
                return self.build_basic_schema(schema)
        except Exception:
            warn(f"Encountered an issue resolving field {self.target}, defaulting to string.")
            return build_basic_type(OpenApiTypes.STR)
