from django.shortcuts import render
import json
from insurancesys.models import Customer
# Create your views here.

from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# c_id
# c_firstname
# c_lastname
# c_street
# c_city
# c_state
# c_zipcode
# c_gender
# c_maritalstatus
# c_customertype


def customer(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        c_id = json_data.get('c_id')
        c_firstname = json_data.get('c_firstname')
        c_lastname = json_data.get('c_lastname')
        c_street = json_data.get('c_street')
        c_city = json_data.get('c_city')
        c_state = json_data.get('c_state')
        c_zipcode = json_data.get('c_zipcode')
        c_gender = json_data.get('c_gender')
        c_maritalstatus = json_data.get('c_maritalstatus')
        c_customertype = json_data.get('c_customertype')
        if not c_id or not c_firstname or not c_lastname or not c_street or not c_city or not c_state or not c_zipcode or not c_gender or not c_maritalstatus or not c_customertype:
            return JsonResponse({
                'error_code': 1
            })
        Customer.objects.create(c_id=c_id, c_firstname=c_firstname, c_lastname=c_lastname, c_street=c_street, c_city=c_city,
                                c_state=c_state, c_zipcode=c_zipcode, c_gender=c_gender, c_maritalstatus=c_maritalstatus, c_customertype=c_customertype)
        # print(request.GET['is_auto_customer'])

        # json_data['name'] = 'grace'

        return JsonResponse({
            'error_code': 0
        })

