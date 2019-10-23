from django.shortcuts import render, redirect
from .models import Company, User, Transfer
from django.http import HttpResponseNotFound
from django.http import JsonResponse

from rest_framework import viewsets
from .serializers import CompanySerializer, UserSerializer, TransferSerializer

from faker import Faker
from datetime import datetime
import dateutil.relativedelta

from random import randint
from .models import Transfer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('name')
    serializer_class = UserSerializer

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer



def index(request):
    return render(request, 'index.html')


# Calculating of needed last 6 months
import pandas as pd
cur_time = datetime.now()
start_time_for_months = cur_time - dateutil.relativedelta.relativedelta(months=6)
dict_months = {}            # numbers and names of months

for i in pd.date_range(start=start_time_for_months, end=cur_time, freq='MS'):
    dict_months[int(i.strftime("%m"))] = i.strftime("%B")


def show_abusers(request):
    return render(request, 'abusers.html', {'dict_months':dict_months})


from django.db import connection

def show_report(request, month):

    try:
        month_name = dict_months[int(month)]

        cursor = connection.cursor()
        result = cursor.execute('''SELECT vpn_app_company.name, vpn_app_company.quota, sum(transferred) AS transferred FROM vpn_app_transfer
        INNER JOIN vpn_app_user on vpn_app_transfer.user_id = vpn_app_user.id
            INNER JOIN vpn_app_company ON vpn_app_user.company_id = vpn_app_company.id AND user_id in (SELECT user_id WHERE MONTH(datetime)={})
                GROUP BY company_id ORDER BY transferred DESC ;'''.format(month))

        items = []                      # Creating the report data
        for row in cursor.fetchall():
            a = round(row[2] / 1099511627776, 2)
            if a > row[1]:
                items.append({'name': row[0], 'quota': row[1], 'transferred': a})

        connection.close()
        return JsonResponse({'items': items, 'month_name':month_name})
    except:
        return redirect('show_abusers')


fake = Faker()

# Generation of transfers data
def generate_data(request):
    try:
        Transfer.objects.all().delete()
        for month_delta in range(6, 1, -1):

            for user in User.objects.all():
                amount_transf = randint(2, 100)
                for each_transf in range(1,amount_transf):
                    initial_start_time = cur_time - dateutil.relativedelta.relativedelta(months=month_delta-1)

                    end_time = cur_time - dateutil.relativedelta.relativedelta(months=month_delta-2)
                    if end_time == cur_time:
                        start_time = cur_time.replace(day=1,hour=0,minute=0,microsecond=0)
                    else:
                        start_time = initial_start_time.replace(day=1, hour=0, minute=0, microsecond=0)
                    random_date_time = fake.date_time_between(start_date=start_time, end_date=end_time)
                    random_transferred = randint(100,1099511627776)
                    Transfer.objects.create(user_id=user.id,datetime=random_date_time,resource='http://xxxx.xxx/xx.xx',transferred=random_transferred)
        generation_result_success = 'Data is generated!'

        return JsonResponse({'generation_result':generation_result_success})
    except:
        generation_result_failure = "Data isn't generated!"
        return JsonResponse({'generation_result': generation_result_failure})



# -------------------------------------------------------------------------------------------
# ------------------------------------- Old options -----------------------------------------
# -------------------------------------------------------------------------------------------


def companies_list(request):
    companies = Company.objects.all()
    return render(request, 'companies.html',{'companies':companies})

def users_list(request):
    users = User.objects.all()
    return render(request, 'users.html',{'users':users})

def add_company(request):
    if request.method == 'POST':
        company = Company()
        company.name =request.POST.get('company_name')
        company.quota =request.POST.get('company_quota')
        company.save()
        return redirect('companies_list')
    else:
        return render(request, 'edit_company.html')

def add_user(request):
    companies = Company.objects.all()
    if request.method == 'POST':
        user = User()
        user.name =request.POST.get('user_name')
        user.email =request.POST.get('user_email')
        user.company_id =request.POST.get('companies_dropdown','')
        user.save()
        return redirect('users_list')
    else:
        return render(request, 'edit_user.html',{'companies':companies})

def edit_company(request, pk):
    try:
        company = Company.objects.get(id=pk)
        if request.method == 'POST':
            company.name =request.POST.get('company_name')
            company.quota =request.POST.get('company_quota')
            company.save()
            return redirect('companies_list')
        else:
            return render(request,'edit_company.html',{'company':company})
    except Company.DoesNotExist:
        return HttpResponseNotFound("<h2>Company not found</h2>")

def edit_user(request, pk):
    companies = Company.objects.all()
    try:
        user = User.objects.get(id=pk)
        if request.method == 'POST':
            user.name =request.POST.get('user_name')
            user.email =request.POST.get('user_email')
            user.company_id =request.POST.get('companies_dropdown','')
            user.save()
            return redirect('users_list')
        else:
            return render(request,'edit_user.html',{'user':user, 'companies':companies})
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>Company not found</h2>")

def delete_company(request, pk):
    try:
        company = Company.objects.get(id=pk)
        company.delete()
        return redirect('companies_list')
    except Company.DoesNotExist:
        return HttpResponseNotFound("<h2>Company not found</h2>")

def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.delete()
        return redirect('users_list')
    except User.DoesNotExist:
        return HttpResponseNotFound("<h2>User not found</h2>")


def abusers(request):
    transfers = Transfer.objects.all()

    return render(request, 'abusers1.html', {'transfers':transfers, 'dict_months':dict_months})



def create_report(request):

    try:
        month = request.POST.get('month_dropdown')
        month_name = dict_months[int(month)]
        cursor = connection.cursor()
        result = cursor.execute('''SELECT vpn_app_company.name, vpn_app_company.quota, sum(transferred) AS transferred FROM vpn_app_transfer
        INNER JOIN vpn_app_user on vpn_app_transfer.user_id = vpn_app_user.id
            INNER JOIN vpn_app_company ON vpn_app_user.company_id = vpn_app_company.id AND user_id in (SELECT user_id WHERE MONTH(datetime)={})
                GROUP BY company_id ORDER BY transferred DESC ;'''.format(month))
        items = []
        for row in cursor.fetchall():
            a = round(row[2] / 1099511627776, 2)
            if a > row[1]:
                items.append({'name': row[0], 'quota': row[1], 'transferred': a})

        connection.close()
        return render(request, 'report.html', {'items': items, 'month':month_name})
    except:
        # return render(request, 'abusers1.html', {'warning': "Please, select month."})
        return redirect('abusers')
