# django_custom_jsonfield

![Test](https://github.com/alexpetul/django_custom_jsonfield/actions/workflows/test.yml/badge.svg)
[![Coverage](https://codecov.io/github/AlexPetul/django_custom_jsonfield/graph/badge.svg?token=V33XNC6SZ7)](https://codecov.io/github/AlexPetul/django_custom_jsonfield)

An extended JSON field for Django and Django REST framework with validation support using [jsonschema](https://json-schema.org/learn/getting-started-step-by-step).

## Usage

Install the package:

```text
pip install django_custom_jsonfield
```

Import `CustomJSONField` and define your `schema`, for example:

```python
from django.db import models
from django_custom_jsonfield import CustomJSONField


class Location(models.Model):
    coordinates = CustomJSONField(
        schema={
            "type": "object",
            "properties": {
                "x": {"type": "number"}, 
                "y": {"type": "number"},
            },
            "required": ["x", "y"],
        },
    )

Location(coordinates={"x": 45, "y": 45})  # ok
Location(coordinates={"x": 45, "z": 45})  # ValidationError

```

## DRF Serializer
Just like you use `CustomJSONField` in your models, you can use them in serializers:

```python
from rest_framework import serializers
from django_custom_jsonfield.rest_framework.serializers import CustomJSONField

class LocationSerializer(serializers.Serializer):
    coordinates = CustomJSONField(schema={...})

```

This package automatically comes with openapi extension for `drf-spectacular`.