from django.db import models
from metadata.fields import JSONSchemaField
from django.contrib.auth.models import AbstractUser


str_field_schema = "schemas/string_schema.json"
int_field_schema = "schemas/int_schema.json"
decimal_field_schema = "schemas/decimal_schema.json"
datetime_field_schema = "schemas/datetime_schema.json"


class TaskMetadataSchema(models.Model):

    state_machine = models.OneToOneField("state_machine.StateMachine", on_delete=models.CASCADE, to_field="code")
    text_field_1_config = JSONSchemaField(null=True, blank=True, schema=str_field_schema)
    text_field_2_config = JSONSchemaField(null=True, blank=True, schema=str_field_schema)
    int_field_1_config = JSONSchemaField(null=True, blank=True, schema=int_field_schema)
    int_field_2_config = JSONSchemaField(null=True, blank=True, schema=int_field_schema)
    num_field_1_config = JSONSchemaField(null=True, blank=True, schema=decimal_field_schema)
    num_field_2_config = JSONSchemaField(null=True, blank=True, schema=decimal_field_schema)
    datetime_field_1_config = JSONSchemaField(null=True, blank=True, schema=datetime_field_schema)
    datetime_field_2_config = JSONSchemaField(null=True, blank=True, schema=datetime_field_schema)
    additional_metadata_config = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = "task_metadata"


class TriggerMetadataSchema(TaskMetadataSchema):

    class Meta:
        db_table = "event_metadata"
