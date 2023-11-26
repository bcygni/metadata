from state_machine.models.state_machine import StateMachine, State, Trigger
from django.db import models


class WorkItem(models.Model):
    system_code = models.ForeignKey(StateMachine, State="code", on_delete=models.CASCADE)
    current_status_code = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    current_status_date = models.DateTimeField(auto_now_add=True)
    last_trigger = models.ForeignKey(Trigger, on_delete=models.DO_NOTHING)
    priority = models.IntegerField(default=0)


class WorkEvent(models.Model):

    work_item = models.ForeignKey(WorkItem, on_delete=models.CASCADE)
    previous_status = models.TextField(max_length=30)
    next_status = models.TextField(max_length=30)
