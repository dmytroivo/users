from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render, redirect, render_to_response
from .forms import UserForm, PlanForm
from .models import User, Plan
from datetime import datetime
import re


def index_html(request):
    context={}
    usr=User.objects.all()
    context['usr']=usr
    
    for usrth in usr:
        context['usrth']=usrth
        break
#    if request.method == 'POST':
#        pass
#        return render(request, 'index_html')
    return render(request, 'index.html',context)

def user_html(request):

    context={}
    user_form=UserForm()
    context['user_form']=user_form
    user=User.objects.all()
    context['user']=user

    if request.method == 'POST':
        user_form=UserForm(request.POST)
        context['user_form']=user_form
        if user_form.is_valid():
            u=User(
                f_name = request.POST.get('f_name'),
                l_name = request.POST.get('l_name'),
                adress = request.POST.get('adress'),
                email = request.POST.get('email'),
                tel = request.POST.get('tel'),
                name_plan = Plan.objects.get(name=request.POST.get('name_plan')),
                status = request.POST.get('status'),
                descript = request.POST.get('descript')
            )
            u.save()
            return redirect('user')

    return render(request,'user.html',context)

def edituser_html(request):
        
        context={}
        if request.method == 'GET' and 'id_item' in request.GET:
            item = User.objects.get(id=request.GET.get('id_item'))
            if item.name_plan is None:
                item.name_plan=Plan.objects.get(name='не выбран')
            context['item']=item
            user_form=UserForm(
                {
                  'f_name':item.f_name,
                  'l_name':item.l_name,
                  'adress':item.adress,
                  'email':item.email,
                  'tel':item.tel,
                  'name_plan':item.name_plan.name,
                  'status':item.status,
                  'descript':item.descript
                }
            )
            context['user_form']=user_form
            context['id_item']=request.GET.get('id_item')
            return render(request,'edituser.html', context)
        
        elif request.method != 'POST': 
            return redirect('user')

        if request.method == 'POST':
            user_form=UserForm(request.POST)
            context['user_form']=user_form
            item = User.objects.get(id=request.POST.get('id_item'))
            context['item']=item
            context['id_item']=request.POST.get('id_item')

            if  user_form.is_valid():

                User.objects.filter(id=request.POST.get('id_item')).update(
                    f_name=request.POST.get('f_name'),
                    l_name=request.POST.get('l_name'),
                    adress=request.POST.get('adress'),
                    email=request.POST.get('email'),
                    tel=request.POST.get('tel'),
                    name_plan=Plan.objects.get(name=request.POST.get('name_plan')),
                    status =request.POST.get('status'),
                    descript =request.POST.get('descript'),
                )
                return redirect('user')
        return render(request,'edituser.html', context)

def plan_html(request):
    context={}
    plan_form=PlanForm()
    context['plan_form']=plan_form
    pln=Plan.objects.all()
    context['pln']=pln

    if request.method == 'POST':
        plan_form=PlanForm(request.POST)
        context['plan_form']=plan_form

        if plan_form.is_valid():
            add_item_plan = Plan(
                name=request.POST.get('name'), 
                price=request.POST.get('price'), 
                relise_date=_str_to_datetime(request.POST.get('relise_date')),
                expired_date=_str_to_datetime(request.POST.get('expired_date')),
                status=request.POST.get('status')
            )
            add_item_plan.save()
            return redirect('plan')

    return render(request,'plan.html', context)


def editplan_html(request):
        
        context={}
        if request.method == 'GET' and 'id_item' in request.GET:
            item = Plan.objects.get(id=request.GET.get('id_item'))
#            if item.name_plan=='':
#               item.name_plan=Plan.objects.get(name='не выбран')
            context['item']=item
            plan_form=PlanForm(
                {'name':item.name,
                 'price':item.price,
                 'relise_date':item.relise_date,
                 'expired_date':item.expired_date,
                 'status':item.status,
                }
            )
            context['plan_form']=plan_form
            context['id_item']=request.GET.get('id_item')
            return render(request,'editplan.html', context)
        elif request.method != 'POST': 
            return redirect('plan')

        if request.method == 'POST':
            plan_form=PlanForm(request.POST)
            context['plan_form']=plan_form
            item = Plan.objects.get(id=request.POST.get('id_item'))
            context['item']=item
            context['id_item']=request.POST.get('id_item')

            if  plan_form.is_valid():

                Plan.objects.filter(id=request.POST.get('id_item')).update(
                    name=request.POST.get('name'), 
                    price=request.POST.get('price').replace(',','.'), 
                    relise_date=_str_to_datetime(request.POST.get('relise_date')),
                    expired_date=_str_to_datetime(request.POST.get('expired_date')),
                    status=request.POST.get('status')
                )
                return redirect('plan')
        return render(request,'editplan.html', context)

def delete_by_id(request):
    if (request.method == 'POST'):
        if Plan.objects.get(id=request.POST.get("delete_by_id")).name != 'не выбран':
            Plan.objects.filter(id=request.POST.get("delete_by_id")).delete()
    
    return redirect('plan')

def delete_user_by_id(request):
    if (request.method == 'POST'):
        User.objects.filter(id=request.POST.get("delete_user_by_id")).delete()
    
    return redirect('user')

def _str_to_datetime(srting_data):
    try:
        result_mat=re.match('^(\d{2})[\./](\d{2})[\./](\d{4})$', srting_data)
        if result_mat is not None:
            return datetime.strptime(
                            srting_data[0:2]+
                            srting_data[3:5]+
                            srting_data[6:], "%d%m%Y").date()
        else: result_mat=re.match('^(\d{2})[\./](\d{2})[\./](\d{2})$', srting_data)
        
        if result_mat is not None:
            return datetime.strptime(
                            srting_data[0:2]+
                            srting_data[3:5]+
                            srting_data[6:], "%d%m%y").date()
    except ValueError:
        pass
    return None


#def _amount_to_decim(price):
#    try:
#        result_mat=re.match('^(\d{0,5}),(\d{0,2})$', srting_data)
#        if result_mat is not None:
#            return price.replase(',','.')
#    except ValueError:
#        pass
#    return None
