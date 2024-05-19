# django_custom_jsonfield

![Test](https://github.com/alexpetul/django_custom_jsonfield/actions/workflows/test.yml/badge.svg)
[![Coverage](https://codecov.io/github/AlexPetul/django_custom_jsonfield/graph/badge.svg?token=V33XNC6SZ7)](https://codecov.io/github/AlexPetul/django_custom_jsonfield)

An extended JSON field for Django and Django REST framework with validation support using [jsonschema](https://json-schema.org/learn/getting-started-step-by-step).

## Usage

### Installation

To install the package, run:

```text
pip install django_custom_jsonfield
```

### Defining a model field

Import CustomJSONField and define your schema. Here’s an example of how to use it in a model:

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

### DRF Serializers
You can also use `CustomJSONField` in Django REST Framework serializers:

```python
from rest_framework import serializers
from django_custom_jsonfield.rest_framework.serializers import CustomJSONField

class LocationSerializer(serializers.Serializer):
    coordinates = CustomJSONField(schema={...})

```

### OpenAPI Integration
This package includes extension for `drf-spectacular`, allowing your API documentation 
to correctly display the expected JSON schema.

## Migrating existing data
The `CustomJSONField` does not impose constraints on existing data. 
Therefore, you can change a field from default `JSONField` to `CustomJSONField` even if 
some rows violate the schema. However, it is recommended to follow these steps to 
sure a smooth transition:

1. **Create a new field**: add a new field of type `CustomJSONField` to your model.
2. **Data migration**: Perform a data migration to copy the values from the old field to the new field, ensuring the data conforms to the schema.
3. **Replace the old field**: Remove the old field and rename the new field to match the old field's name.

Following these steps will ensure that your data complies with the new schema.