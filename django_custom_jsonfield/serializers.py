from rest_framework import serializers


class CustomJSONField(serializers.JSONField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        # if jsonschema.validate(data):
        #     pass

        return data
