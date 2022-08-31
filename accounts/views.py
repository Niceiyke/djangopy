from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from.forms import RegistrationForm


# Create your views here.
def RegistrationView(request):
    form =RegistrationForm()
    if request.method =='POST':
        print(request.POST)
        form =RegistrationForm(request.POST)
         
        if form.is_valid():
            user = form.save(commit=False)
            # Todo implement email activation
            user.email= user.email.strip().lower()
            user.is_active =True
            user.save()
            return redirect('/')



    context={
        'form':form
        }


    return render(request,'accounts/register.html',context)



