from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from uuid import uuid4
from state_machine.models.queryset import StateMachineManager


User = get_user_model()


code_validator = RegexValidator('^[a-zA-Z0-9_-]+$', message="No special characters allowed except for '-' and '_'")


class StateMachine(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    code = models.CharField("State Machine Code", max_length=30, unique=True, validators=[code_validator])
    description = models.CharField(blank=True, default="", max_length=60)
    objects = StateMachineManager()

    class Meta:
        db_table = "state_machine_definition"

    def __str__(self):
        return f"{self.code} ({str(self.pk)})"


class State(models.Model):
    state_machine = models.ForeignKey(StateMachine, on_delete=models.CASCADE, related_name="states")
    code = models.CharField("State Code", max_length=30, validators=[code_validator])
    category_code = models.CharField(blank=True, default="", max_length=30, validators=[code_validator])

    class Meta:
        db_table = "state_definition"
        unique_together = ('state_machine', 'code')

    def __str__(self):
        return f"{self.code}"


class Trigger(models.Model):

    TRANSITION = "TRANSITION"
    REVERSE_TRANSITION = "REVERSE"

    TRANSITION_CHOICES = (
        (TRANSITION, "Transition"),
        (REVERSE_TRANSITION, "Reverse Transition")
    )

    state_machine = models.ForeignKey(StateMachine, on_delete=models.CASCADE, related_name="triggers", null=True)
    code = models.CharField(max_length=30, validators=[code_validator])
    trigger_type = models.CharField(max_length=30, choices=TRANSITION_CHOICES, default=TRANSITION)
    destination_state = models.ForeignKey(State, related_name="sources", on_delete=models.CASCADE)
    source_states = models.ManyToManyField(State, related_name="triggers")

    class Meta:
        db_table = "trigger_definition"
        unique_together = ("state_machine", "code")

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __str__(self):
        return f"{self.code}"


class Project(models.Model):
    name = models.CharField(max_length=60, unique=True)
    code = models.CharField(max_length=30, unique=True, validators=[code_validator])
    users = models.ManyToManyField(User)
    state_machine = models.ForeignKey(StateMachine, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


