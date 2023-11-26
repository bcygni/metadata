import fastjsonschema
import json
from django.db.models import JSONField
from pathlib import Path
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


class JsonValidationCompiler:

    def __init__(self, schema: dict):
        self.schema = schema
        self.validate = fastjsonschema.compile(schema)

    def __call__(self, data):
        return self.validate(data)


class JSONSchemaField(JSONField):

    def __init__(self, *args, schema: dict | str = None, **kwargs):
        if isinstance(schema, str):
            schema: dict = self._load_schema_from_file(schema)
        self._validate_schema = JsonValidationCompiler(schema)
        super().__init__(*args, **kwargs)

    @classmethod
    def _load_schema_from_file(cls, filename: str):
        path = Path(__file__).parent / filename
        with open(path) as file:
            return json.load(file)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        try:
            self._validate_schema(value)
        except fastjsonschema.exceptions.JsonSchemaValueException as e:
            raise ValidationError(message=e.message)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value and not self.null:
            self._validate_schema(value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['schema'] = self._validate_schema.schema
        return name, path, args, kwargs
