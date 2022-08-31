from django.db import models
from core import choices

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100,)


    def __str__(self):
     return self.name

class Shift_type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100,choices=choices.equipment_choices)
   


    def __str__(self):
        return self.name

class FunctionFailure(models.Model):
    equipment =models.ForeignKey(Equipment,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.equipment}:{self.name}'

class FailureMode(models.Model):
    equipment =models.ForeignKey(Equipment,on_delete=models.CASCADE)
    function_failure =models.ForeignKey(FunctionFailure,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.equipment}:{self.name}'





class Line(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Line_manager(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Data_operator(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Team_leader(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Production_team(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product_type(models.Model):

    name = models.CharField(max_length=50)
    bottle_size =models.CharField(max_length=50)
    bottles_per_carton =models.PositiveIntegerField()


    def __str__(self):
        return f'{self.name}: {self.bottle_size}'

class Time_period(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Line_speed(models.Model):

    name = models.PositiveIntegerField(default=30000,null=True,blank=True)

    def __str__(self):
        return str(self.name)



class InsightData(models.Model):
    area =models.ForeignKey(Area,on_delete=models.CASCADE)
    line =models.ForeignKey(Line,on_delete=models.CASCADE)
    line_speed =models.ForeignKey(Line_speed,on_delete=models.CASCADE)
    shift_type =models.ForeignKey(Shift_type,on_delete=models.CASCADE)
    line_manager =models.ForeignKey(Line_manager,default='Oyom',on_delete=models.SET_DEFAULT)
    team_leader =models.ForeignKey(Team_leader,on_delete=models.SET_DEFAULT,default='Oyom')
    data_operator = models.ForeignKey(Data_operator,on_delete=models.SET_DEFAULT,default='Oyom')
    production_team =models.ForeignKey(Production_team,on_delete=models.CASCADE)
    product_type =models.ForeignKey(Product_type,on_delete=models.SET_DEFAULT,default='no-name')
    time_period =models.ForeignKey(Time_period,on_delete=models.CASCADE)
    last_counter_reading =models.PositiveIntegerField(default=0)
    new_counter_reading =models.PositiveIntegerField()
    production_date =models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)
    bbt_no =models.CharField(max_length=6)
    bottle_produced =models.PositiveIntegerField(null=True,blank=True)
    deviation_duration =models.PositiveIntegerField(null=True,blank=True)
    line_output =models.PositiveIntegerField(null=True,blank=True)
    opi =models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    deviation_data=models.ManyToManyField('Deviation',blank=True)
   

    def save(self, *args, **kwargs):
        

        self.bottle_produced =self.new_counter_reading - self.last_counter_reading
        print('bottleproduced',self.bottle_produced)
        self.line_output = (int(self.bottle_produced)/int(self.line_speed.name))*100
        print('lineoutput', self.line_output)
        self.deviation_duration =60-((int(self.bottle_produced)/int(self.line_speed.name))*60)
        if(self.deviation_duration<=0):
            self.deviation_duration=0
        print('deviation', self.deviation_duration)
        expected_carton_unit=(int(self.line_speed.name)/int(self.product_type.bottles_per_carton))
        print('expected carton',expected_carton_unit)
        self.opi =((float(self.bottle_produced)/float(self.product_type.bottles_per_carton))/(float(expected_carton_unit)))*100
        print( 'opi',self.opi)
        super(InsightData,self).save(*args,**kwargs)

    
    def __str__(self):
        return f'{self.production_date}: {self.time_period}'

  


class Deviation(models.Model):
    insight=models.ForeignKey(InsightData,on_delete=models.CASCADE)
    category= models.ForeignKey(Category, blank=True, null=True,on_delete=models.CASCADE)
    equipment= models.ForeignKey( Equipment, blank=True, null=True, on_delete=models.CASCADE)
    frequency= models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    function_failure =models.ForeignKey(FunctionFailure,on_delete=models.CASCADE)
    failure_mode =models.ForeignKey(FailureMode,on_delete=models.CASCADE)
    failure_mode_description =models.CharField(max_length=100)
    status =models.CharField(max_length=50,choices=choices.status)

    def __str__(self):
        return self.failure_mode_description 























