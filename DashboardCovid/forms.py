from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Executions


class ExecutionHistory(BSModalModelForm):
    class Meta:
        model = Executions
        fields = ['date_execution', 'state', 'country', 'end_date', 'start_date']
