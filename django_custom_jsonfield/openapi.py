from drf_spectacular.openapi import (
    OpenApiSerializerFieldExtension,
    build_array_type,
    build_object_type,
    follow_field_source,
)


class CustomJSONFieldSerializerExtension(OpenApiSerializerFieldExtension):
    target_class = "django_custom_jsonfield.serializers.CustomJSONField"

    def map_serializer_field(self, auto_schema, direction):
        model = self.target.parent.Meta.model
        model_field = follow_field_source(model, self.target.source.split("."))
        schema = model_field.schema

        if schema["type"] == "object":
            return build_object_type(schema["properties"])
        elif schema["type"] == "array":
            return build_array_type(schema["items"])
