from django.shortcuts import redirect,render
from django.db.models import Sum,Min,Avg
from django.views.generic import View, ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Data_operator, FailureMode, FunctionFailure,InsightData,Deviation,Equipment,Category, Line, Product_type, Team_leader, Time_period
from .forms import DataForm,DeviationForm,FiltterForm


class InsightDataListView(LoginRequiredMixin,ListView):
    login_url = '/accounts/login'
    model = InsightData
    template_name = "insight/list-data.html"
    context_object_name= 'datas'

    def get_context_data(self, **kwargs):
        product_type= Product_type.objects.all()
        team_leader =Team_leader.objects.all()
        operators =Data_operator.objects.all()
        lines =Line.objects.all()
        time_period =Time_period.objects.all()


        datas=super().get_context_data(**kwargs)
        datas['products']=product_type
        datas['leaders']=team_leader
        datas['operators']=operators
        datas['lines']=lines
        datas['times']=time_period


        return datas
    def get_queryset(self):
        qs=super().get_queryset()

        start_date=self.request.GET.get('start-date')
        end_date=self.request.GET.get('end-date')
        line= self.request.GET.get('line')
        product =self.request.GET.get('product-type')
        team_lead = self.request.GET.get('team-leader')
        data_operator = self.request.GET.get('operator')
        time =self.request.GET.get('time-period')

        if line !='' and line is not None:
             qs= qs.filter(line__id=line) 
        if product !='' and  product is not None:
             qs= qs.filter(product_type__id=product) 
        if team_lead !='' and  team_lead is not None:
             qs= qs.filter(team_leader__id=team_lead)    
        if data_operator !='' and  data_operator is not None:
             qs= qs.filter(data_operator__id=data_operator)  
        if time !='' and  time is not None:
             qs= qs.filter(time_period__id=time)            
        if start_date !='' and start_date is not None:
            qs =qs.filter(production_date__gte= start_date)
        if end_date !='' and end_date is not None:
            qs =qs.filter(production_date__lte= end_date)

        return qs
      

class InsightDataCreateView(LoginRequiredMixin,CreateView):
    login_url='/accounts/login'
    model: InsightData
    form_class =DataForm
    template_name = 'insight/create.html'
    success_url = "/insight"

    def get_initial(self):
        qs=InsightData.objects.all().values_list('new_counter_reading').last()
        qs=qs[len(qs)-1]
        print(qs)
        data=super().get_initial()
        data['last_counter_reading']=qs
        return data

    def form_valid(self, form):
        data= super().form_valid(form)
        self.object =form.save(commit=False)
        self.object.bottle_produced =self.object.new_counter_reading - self.object.last_counter_reading
        print('bottleproduced',self.object.bottle_produced)

        self.object.line_output = (int(self.object.bottle_produced)/int(self.object.line_speed.name))*100
        print('lineoutput', self.object.line_output)

        self.object.deviation_duration =60-((int(self.object.bottle_produced)/int(self.object.line_speed.name))*60)
        if(self.object.deviation_duration<=0):
            self.object.deviation_duration=0
        print('deviation', self.object.deviation_duration)

        expected_carton_unit=(int(self.object.line_speed.name)/int(self.object.product_type.bottles_per_carton))
        print('expected carton',expected_carton_unit)
        self.object.opi =((float(self.object.bottle_produced)/float(self.object.product_type.bottles_per_carton))/(float(expected_carton_unit)))*100
        print( 'opi',self.object.opi)
        self.object.save()

        if (self.object.deviation_duration>0):
            return redirect(f'create-deviation/{self.object.id}')
      
        return data
        

class InsightDataUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/accounts/login'
    model = InsightData
    form_class = DataForm
    template_name = 'insight/create.html'
    success_url = "/insight"

    
class InsightDataDeleteView(LoginRequiredMixin,DeleteView):
    login_url='/accounts/login'
    model =InsightData
    template_name ='insight/delete.html'
    success_url = '/insight'
@login_required(login_url='/accounts/login')
def DeviationListView(request):
    qs= Deviation.objects.all()
    categories= Category.objects.all()
    equipments =Equipment.objects.all()
    failure_modes =FailureMode.objects.all()
    lines =Line.objects.all()
    function_failures =FunctionFailure.objects.all()
    start_date=request.GET.get('start-date')
    end_date=request.GET.get('end-date')
    category =request.GET.get('category')
    equipment =request.GET.get('equipment')
    duration =request.GET.get('duration')
    frequency =request.GET.get ('frequency')
    function_fiailure =request.GET.get('function-failure')
    failure_mode =request.GET.get ('failure-mode')
    line= request.GET.get('line')

    if line !='' and line is not None:
        qs= qs.filter(insight__line__id=line)    
    if category !='' and category is not None:
        qs= qs.filter(category__id=category)
    if equipment !='' and equipment is not None:
        qs= qs.filter(equipment__id=equipment)

    if start_date !='' and start_date is not None:
        qs =qs.filter(insight__production_date__gte= start_date)
    if end_date !='' and end_date is not None:
        qs =qs.filter(insight__production_date__lte= end_date)
    if duration !='' and duration is not None: 
        qs =qs.filter(duration__gte= duration)

    if frequency!='' and frequency is not None: 
        qs =qs.filter(frequency__gte= frequency)

    if function_fiailure !='' and function_fiailure is not None:
        qs= qs.filter(function_failure__id=function_fiailure)
    if failure_mode !='' and failure_mode is not None:
        qs= qs.filter(failure_mode__id=failure_mode)


    total_duration=qs.aggregate(duration_sum=Sum('duration'))
    bd_duration=qs.filter(category__id=1).aggregate(bdduration_sum=Sum('duration'))
    ms_duration=qs.filter(category__id=2).aggregate(msduration_sum=Sum('duration'))

    num_breakdown=(qs.filter(category__id=1).count())
    try:
     mtbf=round(bd_duration['bdduration_sum']/num_breakdown,0)
    except:
        mtbf=0

 
    context ={
        'deviations':qs,
        'lines':lines,
        'categories':categories,
        'equipments':equipments,
        'functions':function_failures,
        'failures':failure_modes,
        'duration':total_duration['duration_sum'],
        'bdduration':bd_duration['bdduration_sum'],
        'msduration':ms_duration['msduration_sum'],
        'mtbf':mtbf,


       
    }

    return render (request,"insight/list-deviation.html",context)

@login_required(login_url='/accounts/login')
def DeviationDeploymentView(request):
    equipments =Equipment.objects.all()
    function_failures =FunctionFailure.objects.all()
    failure_modes =FailureMode.objects.all()
    lines =Line.objects.all()


    line= request.GET.get('line')
    function_failures =FunctionFailure.objects.all()
    start_date=request.GET.get('start-date')
    end_date=request.GET.get('end-date')

    if line !='' and line is not None:
        equipments= equipments.filter(deviation__insight__line__id=line)
    
    if start_date !='' and start_date is not None:
        equipments =equipments.filter(deviation__insight__production_date__gte= start_date)

    if end_date !='' and start_date is not None:
        equipments =equipments.filter(deviation__insight__production_date__lte= end_date)
        

    bddeployments=equipments.filter(deviation__category=1).annotate(duration=Sum('deviation__duration',distinct=True),frequency=Sum('deviation__frequency',distinct=True))
    msdeployments=equipments.filter(deviation__category=2).annotate(duration=Sum('deviation__duration',distinct=True),frequency=Sum('deviation__frequency',distinct=True))

    
    for deployment in bddeployments:
        print('bd',deployment,deployment.duration,deployment.frequency)

    for deployment in msdeployments:
        print('ms',deployment,deployment.duration,deployment.frequency)
    
    context={
        'lines':lines,
        'msdeployments':msdeployments,
        'bddeployments':bddeployments

    }

    return render(request,'insight/deployment-dashboard.html',context)
      
# Todo Refactor code 
@login_required(login_url='/accounts/login')
def DeviationCreateView(request,pk):
    form=DeviationForm()    
    if request.method =="POST":
        form=DeviationForm(request.POST)
        if form.is_valid():
           category=form.cleaned_data['category']
           equipment=form.cleaned_data['equipment']
           frequency=form.cleaned_data['frequency']
           duration=form.cleaned_data['duration']
           function_failure=form.cleaned_data['function_failure']
           failure_mode=form.cleaned_data['failure_mode']
           failure_mode_description=form.cleaned_data['failure_mode_description']
       
        insight_obj=InsightData.objects.get(id=pk)
        deviation=Deviation(insight=insight_obj,
            category=category,
            equipment=equipment,
            frequency=frequency,
            duration=duration,
            function_failure=function_failure,
            failure_mode=failure_mode,
            failure_mode_description=failure_mode_description
        )
        deviation.save(force_insert=True)
    total_duration=InsightData.objects.get(id=pk)   
    total_duration=total_duration.deviation_duration 
    print('gfd',total_duration)
    b=Deviation.objects.all()
    d=0
    for i in b:
        if i.insight.id==pk:
         d+=i.duration
    duration=d     
    if (total_duration-duration )>0:
        duration=total_duration-duration
        context={'form':form,'duration':duration}
        return render(request,'insight/create-deviation.html',context)
    else:
        return redirect('/insight')

class DeviationUpdateView(LoginRequiredMixin,UpdateView):
    login_url='/accounts/login'
    model = Deviation
    form_class =DeviationForm
    template_name = 'insight/create-deviation.html'
    success_url = "/insight/deviation"

class DeviationDeleteView(LoginRequiredMixin,DeleteView):
    login_url='/accounts/login'
    model =InsightData
    template_name ='insight/delete-deviation.html'
    success_url = '/insight/deviation'
@login_required(login_url='/accounts/login')
def FilterForm(request):
    filterform=FiltterForm()
    context = {'filterform':filterform}
    return render(request,'insight/filter.html',context)

@login_required(login_url='/accounts/login')
def DashboardView(request):
    line1_data =[]
    line1_label =[]
    line2_data =[]
    line2_label =[]
    line3_data =[]
    line3_label =[]
    line4_data =[]
    line4_label =[]
    line5_data =[]
    line5_label =[]
    line6_data =[]
    line6_label =[]


    line1 =InsightData.objects.filter(line=1)
    for i in line1:
        line1_data.append(i.opi) 
        line1_label.append(i.time_period) 
    
    line2 =InsightData.objects.filter(line=2)
    for i in line2:
        line2_data.append(i.opi) 
        line2_label.append(i.time_period) 

    line3 =InsightData.objects.filter(line=3)
    for i in line3:
        line3_data.append(i.opi) 
        line3_label.append(i.time_period) 

    line4 =InsightData.objects.filter(line=4)
    for i in line4:
        line4_data.append(i.opi) 
        line4_label.append(i.time_period) 

    line5 =InsightData.objects.filter(line=5)
    for i in line5:
        line5_data.append(i.opi) 
        line5_label.append(i.time_period) 

    line6 =InsightData.objects.filter(line=6)
    for i in line6:
        line6_data.append(i.opi) 
        line6_label.append(i.time_period) 
    
    line1_opi =0
    for i in line1_data:
        a =0
        a+=i
    line1_opi=round(a/12,1)


    context={
        'line_opi1': line1_opi,
        'line1_data':line1_data,
        'line1_label': line1_label,
        'line2_data': line2_data,
        'line2_label': line2_label,
        'line3_data':line3_data,
        'line3_label': line3_label,
        'line4_data': line4_data,
        'line4_label': line4_label,
        'line5_data':line5_data,
        'line5_label': line5_label,
        'line6_data': line6_data,
        'line6_label': line6_label,
    }
    return render(request,'insight/dashboard.html',context)