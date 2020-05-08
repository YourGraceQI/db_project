import json
import re
from django.db import transaction
from django.shortcuts import render
from insurancesys.models import Customer, Policy, Invoice, Home, Vehicle, Payment, Driver
from django.http import HttpResponse, JsonResponse
from .validators import *
from django.db.models import F
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from random import randint


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@is_authenticated
@validate_param(method='GET', filedsAndValidator={
    "c_id": [numeric_validator, get_length_validator(10)],
})
@validate_param(method='POST', filedsAndValidator={
    "c_id": [numeric_validator, get_length_validator(10)],
    "c_state": [get_length_validator(2), uppercase_validator],
    "c_zipcode": [numeric_validator, get_length_validator(5)],
    "c_gender": [get_choice_validator(Customer.GENDER)],
    "c_maritalstatus": [get_choice_validator(Customer.MARITAL_STATUS)],
    "c_customertype": [get_choice_validator(Customer.CUSTOMER_TYPE)],
})
@validate_param(method='PUT', filedsAndValidator={
    "c_id": [numeric_validator, get_length_validator(10)],
    "c_state": [get_length_validator(2), uppercase_validator],
    "c_zipcode": [numeric_validator, get_length_validator(5)],
    "c_gender": [get_choice_validator(Customer.GENDER)],
    "c_maritalstatus": [get_choice_validator(Customer.MARITAL_STATUS)],
    "c_customertype": [get_choice_validator(Customer.CUSTOMER_TYPE)],
})
@get_current_customer
def customer(request, current_customer):
    if request.body:
        json_data = json.loads(request.body)
    if request.method == 'GET':
        return response_data(0, '', [model_to_dict(current_customer)])
        # id = request.GET.get('c_id')
        # first_name = request.GET.get('c_firstname')
        # last_name = request.GET.get('c_lastname')
        # # use policy_id to query customer_id
        # policy_id = request.GET.get('policy_id')
        # if not id:
        #     if not first_name or not last_name:
        #         return response_data(1, 'Insufficient GET', [])
        #     else:
        #         customer = Customer.objects.filter(
        #             c_firstname=first_name, c_lastname=last_name)
        #         customer_data = list(customer.values())
        #         return response_data(0, '', customer_data)
        # else:
        #     customer = Customer.objects.filter(c_id=id)
        #     customer_data = list(customer.values())
        #     policy_data = list(Policy.objects.filter(c_id__c_id=id).values())
        #     if customer_data[0]:
        #         customer_data[0]['policys'] = policy_data
        #     return response_data(0, '', customer_data)

    if request.method == 'POST':
        c_id = json_data.get('c_id')
        c_firstname = json_data.get('c_firstname')
        c_lastname = json_data.get('c_lastname')
        c_birthdate = json_data.get('c_birthdate')
        c_street = json_data.get('c_street')
        c_city = json_data.get('c_city')
        c_state = json_data.get('c_state')
        c_zipcode = json_data.get('c_zipcode')
        c_gender = json_data.get('c_gender')
        c_maritalstatus = json_data.get('c_maritalstatus')
        c_customertype = json_data.get('c_customertype')
        if not c_id or not c_firstname or not c_lastname or not c_birthdate or not c_street or not c_city or not c_state or not c_zipcode or not c_gender or not c_maritalstatus or not c_customertype:
            return response_data(1, 'Insufficient POST', [])
        else:
            with transaction.atomic():
                Customer.objects.create(**json_data)
            return response_data(0, 'POST Success', [])

    if request.method == 'PUT':
        try:
            customer = Customer.objects.select_for_update().filter(c_id=current_customer.c_id)
        except:
            return response_data(1, 'No Matched Id', [])

        fields = [field.name for field in Customer._meta.get_fields()
                  if field.name != 'c_id']

        with transaction.atomic():
            for field in fields:
                if json_data.get(field):
                    setattr(customer[0], field, json_data.get(field))
            customer[0].save()
            return response_data(0, 'PUT Success', [])

    return response_data(1, 'Wrong Method', [])

# {
#     "startdate":
#     "enddate":
#     "policy_type":
#     "auto": {
#         "vin":
#         "model_year":
#         "vehiclestatus":
#         "driver": {
#             "driver_licence":
#             "d_firstname":
#             "d_lastname":
#             "d_birthdate":
#         }
#     }
#     "home": {
#         "home_id":
#         "purchase_date":
#         "purchase_value":
#         "homearea":
#         "hometype":
#         "auto_fire_notification":
#         "home_security_system":
#         "swimming_pool":
#         "basement":
#     }
# }
@is_authenticated
@validate_param(method='GET', filedsAndValidator={
    "policy_id": [numeric_validator, get_length_validator(12)],
    "c_id": [numeric_validator, get_length_validator(10)],
})
@validate_param(method='POST', filedsAndValidator={
    "policy_id": [numeric_validator, get_length_validator(12)],
    "policy_status": [get_choice_validator(Policy.POLICY_STATUS)],
    "policy_type": [get_choice_validator(Policy.POLICY_TYPE)],
    "c_id": [numeric_validator, get_length_validator(10)],
    "auto__vin": [numeric_validator, get_length_validator(12)],
    "home__home_id": [numeric_validator, get_length_validator(14)],
    "auto__driver__driver_licence": [numeric_validator, get_length_validator(15)],
    "auto__vehiclestatus": [get_choice_validator(Vehicle.VEHICLE_STATUS)],
    "home__hometype": [get_choice_validator(Home.HOME_TYPE)],
    "home__swimming_pool": [get_choice_validator(Home.SWIMMING_POOL)],
})
# @validate_param(method='PUT', filedsAndValidator={
#     "policy_id": [numeric_validator, get_length_validator(12)],
#     "policy_status": [get_choice_validator(Policy.POLICY_STATUS)],
#     "policy_type": [get_choice_validator(Policy.POLICY_TYPE)],
#     "c_id": [numeric_validator, get_length_validator(10)],
# })
@get_current_customer
def policy(request, current_customer):
    if request.body:
        json_data = json.loads(request.body)
    if request.method == 'GET':
        id = request.GET.get('policy_id')
        # c_id = request.GET.get('c_id')
        if not id:
            policy = Policy.objects.filter(c_id__c_id=current_customer.c_id)
            policy_data = list(policy.values())
            return response_data(0, 'GET Success', policy_data)
        else:
            try:
                policy = Policy.objects.get(
                    policy_id=id, c_id__c_id=current_customer.c_id)
            except:
                return response_data(1, 'Policy not exist.', [])
            policy_data = model_to_dict(policy)
            return response_data(0, 'GET Success', [policy_data])

    if request.method == 'POST':
        startdate = json_data.get('startdate')
        enddate = json_data.get('enddate')
        policy_type = json_data.get('policy_type')
        home = json_data.get('home')
        auto = json_data.get('auto')
        if not startdate or not enddate or not policy_type:
            return response_data('1', 'Insufficent POST', [])
        if policy_type == Policy.AUTO_POLICY:
            if not auto.get('vin') or not auto.get('model_year') or not auto.get('vehiclestatus'):
                return response_data(1, 'Insufficent POST', [])
            if not auto.get('driver').get('driver_licence') or not auto.get('driver').get('d_firstname') or not auto.get('driver').get('d_lastname') or not auto.get('driver').get('d_birthdate'):
                return response_data(1, 'Insufficent POST', [])
        if policy_type == Policy.HOME_POLICY:
            if not home.get('home_id') or not home.get('purchase_date') or not home.get('purchase_value') or not home.get('homearea') or not home.get('hometype') or not home.get('swimming_pool'):
                return response_data(1, 'Insufficent POST', [])
        new_policy_id = str(random_with_N_digits(12))
        while len(Policy.objects.filter(policy_id=new_policy_id)) > 0:
            new_policy_id = str(random_with_N_digits(12))
        try:
            with transaction.atomic():
                new_policy = Policy.objects.create(
                    policy_id=new_policy_id,
                    startdate=startdate,
                    enddate=enddate,
                    policy_type=policy_type,
                    c_id=current_customer,
                )
                # new_invoice_id = str(random_with_N_digits(15))
                # while len(Invoice.objects.filter(invoice_id=new_invoice_id)) > 0:
                #     new_invoice_id = str(random_with_N_digits(15))
                # new_invoice = Invoice.objects.create(
                #     invoice_id = new_invoice_id
                # )
                if policy_type == Policy.HOME_POLICY:
                    new_home = Home.objects.create(
                        home_id=home.get('home_id'),
                        purchase_date=home.get('purchase_date'),
                        purchase_value=round(home.get('purchase_value'), 2),
                        homearea=round(home.get('homearea'), 2),
                        hometype=home.get('hometype'),
                        auto_fire_notification=home.get('auto_fire_notification'),
                        home_security_system=home.get('home_security_system'),
                        swimming_pool=home.get('swimming_pool'),
                        basement=home.get('basement'),
                    )
                    new_home.policys.add(new_policy)
                if policy_type == Policy.AUTO_POLICY:
                    new_vehicle = Vehicle.objects.create(
                        vin=auto.get('vin'),
                        model_year=auto.get('model_year'),
                        vehiclestatus=auto.get('vehiclestatus'),
                    )
                    new_vehicle.policys.add(new_policy)
                    Driver.objects.create(
                        driver_licence=auto.get('driver').get('driver_licence'),
                        d_firstname=auto.get('driver').get('d_firstname'),
                        d_lastname=auto.get('driver').get('d_lastname'),
                        d_birthdate=auto.get('driver').get('d_birthdate'),
                        vin=new_vehicle,
                    )
            return response_data(0, 'POST Success', [])
        except:
            return response_data(1, 'Internal Error.', [])

    # if request.method =='PUT':
    #     id = json_data.get('policy_id')
    #     policy = Policy.objects.filter(policy_id=id)[0]
    #     if not policy:
    #         return response_data(1, 'No Matched Id', [])
    #     else:
    #         fields = [field.name for field in Policy._meta.get_fields()]
    #         for field in fields:
    #             if json_data.get(field):
    #                 if field == 'c_id':
    #                     customer = Customer.objects.get(c_id=json_data.get('c_id'))
    #                     setattr(policy, 'c_id', customer)
    #                 else:
    #                     setattr(policy, field, json_data.get(field))

    #         policy.save()
    #         return response_data(0, '', 'PUT Success')

    # if request.method == 'DELETE':
    #     id = json_data.get('policy_id')
    #     policy = Policy.objects.get(policy_id=id)
    #     invoice = Invoice.objects.get(policy_id__policy_id=id)
    #     home = Home.objects.get(policy_id__policy_id=id)
    #     vehicle = Vehicle.objects.get(policy_id__policy_id=id)
    #     if not policy:
    #         return response_data(1, 'No Matched Id', [])
    #     elif not invoice and not home and not vehicle:
    #         policy.delete()
    #         return response_data(0, '', [])

    return response_data(1, 'Wrong Method', [])


@validate_param(method='GET', filedsAndValidator={
    "invoice_id": [numeric_validator, get_length_validator(15)],
    "policy_id": [numeric_validator, get_length_validator(12)],
})
@validate_param(method='POST', filedsAndValidator={
    "invoice_id": [numeric_validator, get_length_validator(15)],
    "policy_id": [numeric_validator, get_length_validator(12)],
})
@validate_param(method='PUT', filedsAndValidator={
    "invoice_id": [numeric_validator, get_length_validator(15)],
    "policy_id": [numeric_validator, get_length_validator(12)],
})
def invoice(request):
    if request.body:
        json_data = json.loads(request.body)
    if request.method == 'GET':
        id = request.GET.get('invoice_id')
        policy_id = request.GET.get('policy_id')
        if not id:
            if not policy_id:
                return response_data(1, 'Insufficient GET', [])
            else:
                invoice = Invoice.objects.filter(
                    policy_id__policy_id=policy_id)
                invoice_data = list(invoice.values())
                return response_data(0, 'GET Success', invoice_data)
        else:
            invoice = Invoice.objects.filter(invoice_id=id)
            invoice_data = list(invoice.values())
            return response_data(0, 'GET Success', invoice_data)

    # if request.method == 'POST':
    #     invoice_id = json_data.get('invoice_id')
    #     invoice_amount = round(json_data.get('invoice_amount'), 2)
    #     payment_due = json_data.get('payment_due')
    #     installment = json_data.get('installment')
    #     policy_id = json_data.get('policy_id')
    #     policy = Policy.objects.get(policy_id=policy_id)
    #     if not policy:
    #         return response_data('1', 'Insert Parent Key First', [])
    #     elif not invoice_id or not invoice_amount or not payment_due or not installment or not policy_id:
    #         return response_data('1', 'Insufficent POST', [])
    #     else:
    #         json_data['policy_id'] = policy
    #         Invoice.objects.create(**json_data)
    #         return response_data(0, 'POST Success', [])

    # if request.method == 'PUT':
    #     id = json_data.get('invoice_id')
    #     invoice = Invoice.objects.filter(invoice_id=id)[0]
    #     if not invoice:
    #         return response_data(1, 'No Matched Id', [])
    #     else:
    #         fields = [field.name for field in Invoice._meta.get_fields()]
    #         for field in fields:
    #             if json_data.get(field):
    #                 if field == 'policy_id':
    #                     policy = Policy.objects.get(policy_id=json_data.get('policy_id'))
    #                     setattr(invoice, 'policy_id', policy)
    #                 else:
    #                     setattr(invoice, field, json_data.get(field))

    #         invoice.save()
    #         return response_data(0, '', 'PUT Success')

    # if request.method == 'DELETE':
    #     id = json_data.get('invoice_id')
    #     invoice = Invoice.objects.get(invoice_id=id)
    #     payment = Payment.objects.get(invoice_id__invoice_id=id)
    #     if not invoice:
    #         return response_data(1, 'No Matched Id', [])
    #     elif not payment:
    #         invoice.delete()
    #         return response_data(0, '', [])

    return response_data(1, 'Wrong Method', [])


@validate_param(method='GET', filedsAndValidator={
    "pay_id": [numeric_validator, get_length_validator(15)],
    "invoice_id": [numeric_validator, get_length_validator(15)],
})
# @validate_param(method='POST', filedsAndValidator={
#     "pay_id": [numeric_validator, get_length_validator(15)],
#     "payment_method": [get_choice_validator(Payment.METHOD)],
#     "invoice_id": [numeric_validator, get_length_validator(15)],
# })
# @validate_param(method='PUT', filedsAndValidator={
#     "pay_id": [numeric_validator, get_length_validator(15)],
#     "payment_method": [get_choice_validator(Payment.METHOD)],
#     "invoice_id": [numeric_validator, get_length_validator(15)],
# })
def payment(request):
    if request.body:
        json_data = json.loads(request.body)
    if request.method == 'GET':
        id = request.GET.get('pay_id')
        invoice_id = request.GET.get('invoice_id')
        if not id:
            if not invoice_id:
                return response_data(1, 'Insufficient GET', [])
            else:
                payment = Payment.objects.filter(
                    invoice_id__invoice_id=invoice_id)
                payment_data = list(payment.values())
                return response_data(0, 'GET Success', payment_data)
        else:
            payment = Payment.objects.filter(pay_id=id)
            payment_data = list(payment.values())
            return response_data(0, 'GET Success', payment_data)

    if request.method == 'POST':
        new_pay_id = str(random_with_N_digits(15))
        while len(Payment.objects.filter(pay_id=new_pay_id)) > 0:
            new_pay_id = str(random_with_N_digits(15))
        payment_method = json_data.get('payment_method')
        pay_amount = round(json_data.get('pay_amount'), 2)
        invoice_id = json_data.get('invoice_id')
        current_invoice = Invoice.objects.get(invoice_id=invoice_id)
        if not current_invoice:
            return response_data('1', 'Insert Parent Key First', [])
        elif not payment_method or not pay_amount or not invoice_id:
            return response_data('1', 'Insufficent POST', [])
        else:
            allpayment = Payment.objects.filter(invoice_id__invoice_id=invoice_id)
            sum = pay_amount
            for payment in allpayment:
                sum = sum + payment.pay_amount
            if sum >= current_invoice.invoice_amount:
                current_invoice.invoice_cleared = True
                current_invoice.save()
            json_data['invoice_id'] = invoice
            try:
                with transaction.atomic():
                    Payment.objects.create(
                        pay_id = new_pay_id,
                        payment_method = payment_method,
                        pay_amount = pay_amount,
                        invoice_id = current_invoice,
                    )
                return response_data(0, 'POST Success', [])
            except:
                return response_data(1, 'Internal Error', [])

    # if request.method == 'PUT':
    #     id = json_data.get('pay_id')
    #     payment = Payment.objects.filter(pay_id=id)[0]
    #     if not payment:
    #         return response_data(1, 'No Matched Id', [])
    #     else:
    #         fields = [field.name for field in Invoice._meta.get_fields()]
    #         for field in fields:
    #             if json_data.get(field):
    #                 if field == 'pay_id':
    #                     invoice = Invoice.objects.get(invoice_id=json_data.get('pay_id'))
    #                     setattr(payment, 'invoice_id', invoice)
    #                 else:
    #                     setattr(payment, field, json_data.get(field))

    #         payment.save()
    #         return response_data(0, '', 'PUT Success')

    # if request.method == 'DELETE':
    #     id = json_data.get('pay_id')
    #     payment = Invoice.objects.get(pay_id=id)
    #     if not invoice:
    #         return response_data(1, 'No Matched Id', [])
    #     elif not payment:
    #         invoice.delete()
    #         return response_data(0, '', [])

    return response_data(1, 'Wrong Method', [])


@validate_param(method='GET', filedsAndValidator={
    "vin": [numeric_validator, get_length_validator(12)],
    "policy_id": [numeric_validator, get_length_validator(12)],
})
def vehicle(request):
    if request.body:
        json_data = json.loads(request.body)
    if request.method == 'GET':
        id = request.GET.get('vin')
        policy_id = request.GET.get('policy_id')
        if not id:
            if not policy_id:
                return response_data(1, 'Insufficient GET', [])
            else:
                vehicle = Vehicle.objects.filter(policys__policy_id=policy_id)
                vehicle_data = list(vehicle.values('vin', 'model_year', 'vehiclestatus', policy_id=F(
                    'policys__policy_id'), policy_status=F('policys__policy_status'), c_id=F('policys__c_id__c_id')))
                return response_data(0, 'GET Success', vehicle_data)
        else:
            vehicle = Vehicle.objects.filter(vin=id)
            vehicle_data = list(vehicle.values('vin', 'model_year', 'vehiclestatus', policy_id=F(
                'policys__policy_id'), policy_status=F('policys__policy_status'), c_id=F('policys__c_id__c_id')))
            return response_data(0, 'GET Success', vehicle_data)

    return response_data(1, 'Wrong Method', [])


@validate_param(method='GET', filedsAndValidator={
    "vin": [numeric_validator, get_length_validator(12)],
    "driver_licence": [numeric_validator, get_length_validator(15)],
})
def driver(request):
    if request.body:
        json_data = json.loads(request.body)
    if request.method == 'GET':
        id = request.GET.get('driver_licence')
        vin = request.GET.get('vin')
        if not id:
            if not vin:
                return response_data(1, 'Insufficient GET', [])
            else:
                driver = Driver.objects.filter(vin__vin=vin)
                driver_data = list(driver.values('driver_licence', firstname=F('d_firstname'), lastname=F(
                    'd_lastname'), birthdate=F('d_birthdate'), vehicle_vin=F('vin__vin')))
                return response_data(0, 'GET Success', driver_data)
        else:
            driver = Driver.objects.filter(driver_licence=id)
            driver_data = list(driver.values('driver_licence', firstname=F('d_firstname'), lastname=F(
                'd_lastname'), birthdate=F('d_birthdate'), vehicle_vin=F('vin__vin')))
            return response_data(0, 'GET Success', driver_data)

    return response_data(1, 'Wrong Method', [])


@validate_param(method='GET', filedsAndValidator={
    "home_id": [numeric_validator, get_length_validator(14)],
    "policy_id": [numeric_validator, get_length_validator(12)],
})
def home(request):
    if request.body:
        json_data = json.loads(request.body)
    if request.method == 'GET':
        id = request.GET.get('home_id')
        policy_id = request.GET.get('policy_id')
        if not id:
            if not policy_id:
                return response_data(1, 'Insufficient GET', [])
            else:
                home = Home.objects.filter(policys__policy_id=policy_id)
                home_data = list(home.values('home_id', 'purchase_date', 'purchase_value', 'homearea', 'hometype',
                                             'auto_fire_notification', 'home_security_system', 'swimming_pool', 'basement', policy=F('policys__c_id__c_id')))
                return response_data(0, 'GET Success', home_data)
        else:
            home = Home.objects.filter(home_id=id)
            home_data = list(home.values('home_id', 'purchase_date', 'purchase_value', 'homearea', 'hometype',
                                         'auto_fire_notification', 'home_security_system', 'swimming_pool', 'basement', policy=F('policys__c_id__c_id')))
            return response_data(0, 'GET Success', home_data)

    return response_data(1, 'Wrong Method', [])


def signin(request):
    json_data = json.loads(request.body)
    username = json_data.get('username')
    password = json_data.get('password')
    print(username, password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return response_data(0, 'Login Success', model_to_dict(user))
    else:
        return response_data(1, 'Wrong Usename or Password', [])

@is_authenticated
def signout(request):
    logout(request)
    return response_data(0, 'Logout success', [])

@validate_param(method='POST', filedsAndValidator={
    # "c_id": [numeric_validator, get_length_validator(10)],
    "c_state": [get_length_validator(2), uppercase_validator],
    "c_zipcode": [numeric_validator, get_length_validator(5)],
    "c_gender": [get_choice_validator(Customer.GENDER)],
    "c_maritalstatus": [get_choice_validator(Customer.MARITAL_STATUS)],
    "c_customertype": [get_choice_validator(Customer.CUSTOMER_TYPE)],
})
def signup(request):
    if request.method != 'POST':
        return response_data(1, 'Wrong Method', [])
    json_data = json.loads(request.body)
    username = json_data.get('username')
    password = json_data.get('password')
    email = json_data.get('email')
    c_id = json_data.get('customerid')
    first_name = json_data.get('c_firstname')
    last_name = json_data.get('c_lastname')
    birthdate = json_data.get('c_birthdate')
    if c_id is not None:
        try:
            customer_queryset = Customer.objects.select_for_update().filter(c_id=c_id)
        except:
            return response_data(1, 'Customer not exist', [])
        customer = customer_queryset[0]
        customer_dict = model_to_dict(customer)
        # try:
        #     customer = Customer.objects.get(c_id=c_id)
        #     customer_dict = model_to_dict(customer)
        # except:
        #     return response_data(1, 'Customer not exist', [])
        if customer.user:
            return response_data(1, 'Customer already registered', [])
        if first_name == customer_dict.get('c_firstname') and last_name == customer_dict.get('c_lastname'):
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username, email, password)
                    user.customer = customer
                    user.save()
                    customer.user = user
                    customer.save()
                return response_data(0, 'Sign Up Success', username)
            except:
                return response_data(1, 'Internal Error', username)
        else:
            return response_data(1, 'Incorrect Customer Information', [])
    else:
        c_id = str(random_with_N_digits(10))  
        while len(Customer.objects.filter(c_id=c_id)) > 0:
            c_id = str(random_with_N_digits(10))
        c_firstname = json_data.get('c_firstname')
        c_lastname = json_data.get('c_lastname')
        c_birthdate = json_data.get('c_birthdate')
        c_street = json_data.get('c_street')
        c_city = json_data.get('c_city')
        c_state = json_data.get('c_state')
        c_zipcode = json_data.get('c_zipcode')
        c_gender = json_data.get('c_gender')
        c_maritalstatus = json_data.get('c_maritalstatus')
        c_customertype = json_data.get('c_customertype')

        if not c_id or not c_firstname or not c_lastname or not c_street or not c_city or not c_state or not c_zipcode or not c_gender or not c_maritalstatus or not c_customertype:
            return response_data(1, 'Insufficient SignUp', [])
        else:
            customer = Customer(
                c_id=c_id,
                c_firstname=c_firstname,
                c_lastname=c_lastname,
                c_street=c_street,
                c_city=c_city,
                c_state=c_state,
                c_zipcode=c_zipcode,
                c_gender=c_gender,
                c_maritalstatus=c_maritalstatus,
                c_customertype=c_customertype,
                c_birthdate=c_birthdate,
            )
            with transaction.atomic():
                customer.save()
                user = User.objects.create_user(username, email, password)
                user.customer = customer
                user.save()
                customer.user = user
                customer.save()
            return response_data(0, 'Sign Up Success', username)
            try:
                with transaction.atomic():
                    customer.save()
                    user = User.objects.create_user(username, email, password)
                    user.customer = customer
                    user.save()
                    customer.user = user
                    customer.save()
                return response_data(0, 'Sign Up Success', username)
            except:
                return response_data(1, 'Internal Error', username)

def check_username_is_existing(request):
    if request.method != 'POST':
        return response_data(1, 'Wrong method.', [])
    json_data = json.loads(request.body)
    if not json_data.get('username'):
        return response_data(1, 'Insufficient Post.', [])
    try:
        User.objects.get(username=json_data.get('username'))
        return response_data(1, 'Username already exists.', [])
    except:
        return response_data(0, 'Username is valid', [])

    # "pay_id": "",
    # "payment_date": "",
    # "payment_method": "",
    # "pay_amount": "",
    # "invoice_id": "",


# {
    # "c_id": "6666666668",
    # "c_firstname": "vvvv",
    # "c_lastname": "qi",
    # "c_street": "ttt",
    # "c_city": "rrr",
    # "c_state": "NY",
    # "c_zipcode": "11205",
    # "c_gender": "F",
    # "c_maritalstatus": "S",
    # "c_customertype": "A"
# }


# {
#     "policy_id": "222222222222224",
#     "startdate": "2018-01-01",
#     "enddate": "2020-01-01",
#     "premium_amount": 500,
#     "policy_status": "C",
#     "policy_type": "H",
#     "c_id": "6666666668"
# }

# {
#     "invoice_id": ""
#     "invoice_amount": ""
#     "payment_due": ""
#     "installment": ""
#     "policy_id": ""
#     "policy": ""
# }
