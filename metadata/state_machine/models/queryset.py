from django.db import models
from django.db.models import Aggregate


class CommaSepFieldSet(models.CharField):

    def from_db_value(self, value, *args):
        value: str = super().to_python(value)
        if value:
            return set(value.split(","))
        return value


class GroupConcat(Aggregate):
    function = 'GROUP_CONCAT'
    template = '%(function)s(DISTINCT %(expressions)s)'

    def as_postgresql(self, compiler, connection):
        self.function = 'STRING_AGG'
        return super(GroupConcat, self).as_sql(compiler, connection)


class StateMachineManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().annotate(
            list_of_states=GroupConcat("states__triggers__code", output_field=CommaSepFieldSet()),
            list_of_triggers=GroupConcat("states__code", output_field=CommaSepFieldSet())
        )
        return qs


class TriggerManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related(
            "state_machine__code", "destination_state"
        ).prefetch_related("source_states").annotate(
            list_of_source_states=GroupConcat("source_states__code", output_field=CommaSepFieldSet()),
        )
        return qs


class StateManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related(
            "state_machine__code", "destination_state"
        ).annotate(
            list_of_states=GroupConcat("sources__code", output_field=CommaSepFieldSet()),
            list_of_triggers=GroupConcat("triggers__code", output_field=CommaSepFieldSet())
        )
        return qs