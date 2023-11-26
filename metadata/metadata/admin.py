from prettyjson import PrettyJSONWidget
from django.db.models import JSONField
from django import forms
from django.contrib import admin
from metadata.models import TaskMetadataSchema, TriggerMetadataSchema

# Register your models here.


TASK_METADATA_HTML = """
<p>If tasks in the workflow will be using one of the below indexed text metadata fields, provide a valid JSON
dict with the following properties: "name", "default", and, "is_required". </p>
<p>
    <strong>name</strong>: The name of the data that will be stored in this metadata field. (Required)<br>
    <strong>description</strong>: Some text describing what this data is/where it's used, etc.<br>
    <strong>default_value</strong>: The default value of this data if not provided at creation.<br>
    <strong>is_required</strong>: Set to true, if this data should always exist in the task metadata.
</p>
<h4>Example:</h4>
<pre style="background-color: rgb(235,235,235); padding: 5px;">
{
  "name": "handoff-method",
  "description": "some description",
  "default_value": "foo",
  "is_required": true
}
</pre>
"""

# class CommentForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for f in self.fields:
#             f.widget.attrs.update({
#                 'autocomplete': 'off',
#                 'spellcheck': 'false'
#             })


@admin.register(TaskMetadataSchema)
class TaskMetadataSchemaAdmin(admin.ModelAdmin):
    fieldsets = (
        ("State Machine", {"fields": ("state_machine",)}),
        ("Indexed Text Fields", {
            "fields": ("text_field_1_config", "text_field_2_config"),
            "description": TASK_METADATA_HTML}),
        ("Indexed Number Fields", {"fields": ("num_field_1_config", "num_field_2_config")}),
        ("Indexed DateTime Fields", {"fields": ("datetime_field_1_config", "datetime_field_2_config")}),
        ("Extra Fields", {"fields": ("additional_metadata_config",)})
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget(attrs={"spellcheck": "false", "cols": 100})}
    }


@admin.register(TriggerMetadataSchema)
class TriggerMetadataSchemaAdmin(admin.ModelAdmin):
    ...
