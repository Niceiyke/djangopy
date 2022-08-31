from datetime import date
from django.forms import ModelForm
from django import forms
from .models import FailureMode, InsightData,Deviation,Equipment



class DataForm(ModelForm):
    class Meta:
        model = InsightData
        fields =['area','line','line_speed','line_manager',
        'shift_type','team_leader','data_operator','production_team',
        'product_type','time_period','last_counter_reading', 'new_counter_reading','bbt_no','deviation_data'
        ]




class DeviationForm(ModelForm):
    class Meta:
        model=Deviation
        fields =['category','equipment','frequency','duration',
        'function_failure','failure_mode','failure_mode_description']

   

class EquipmentForm(ModelForm):
    class Meta:
        model=Equipment
        fields ='__all__'


class FiltterForm(forms.Form):
    category =forms.ChoiceField(widget=forms.Select,required=False)
    equipment =forms.ChoiceField(widget=forms.Select,required=False)
    FailureMode =forms.CharField(max_length=100,required=False)
    functionFailure =forms.CharField(max_length=100,required=False)
    startDate =forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),required=False)
    endDate =forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}),required=False)

