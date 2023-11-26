from django.contrib import admin
from state_machine.models.state_machine import State, StateMachine, Trigger
from django.urls import resolve


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    ...


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    ...


class StateAdminInline(admin.TabularInline):
    model = State
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        resolved = resolve(request.path_info)
        if resolved.captured_kwargs:
            state_machine_id = resolved.captured_kwargs['object_id']
            qs.filter(state_machine_id=state_machine_id)
        return qs


class TriggerAdminInline(admin.TabularInline):
    model = Trigger
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        for fk in ["destination_state", "source_states"]:
            field = formset.form.base_fields[fk]
            field.widget.can_add_related = False
            field.widget.can_change_related = False
            field.widget.can_delete_related = False
        return formset

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        resolved = resolve(request.path_info)
        if resolved.captured_kwargs:
            state_machine_id = resolved.captured_kwargs['object_id']
            qs = qs.filter(state_machine_id=state_machine_id)
        return qs



@admin.register(StateMachine)
class StateMachineAdmin(admin.ModelAdmin):

    def add_view(self, request, **kwargs):
        self.inlines = (StateAdminInline,)
        return super().add_view(request)

    inlines = (StateAdminInline, TriggerAdminInline,)
