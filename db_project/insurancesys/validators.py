import re, json
from .utils import response_data

def numeric_validator(value):
    match = re.match(r'^[0-9]+$', value)
    return True if match else False

def uppercase_validator(value):
    match = re.match(r'^[A-Z]+$',value)
    return True if match else False 

def get_length_validator(length):
    def length_validator(value):
        return len(value) == length
    return length_validator

def get_choice_validator(choices):
    choice_list = [choice_item[0] for choice_item in choices]
    def choice_validator(value):
        return value in choice_list
    return choice_validator

def apply_validator(data, filedsAndValidator):
    for filed_name in filedsAndValidator:
        if '__' in filed_name:
            key_array = filed_name.split('__')
            field_value = data.get(key_array[0])
            if field_value:
                for key in key_array[1:]:
                    field_value = field_value[key]
            
        else:
            field_value = data.get(filed_name)
        validators = filedsAndValidator.get(filed_name)
        for validator in validators:
            if field_value is None or field_value == '':
                pass
            elif not validator(field_value):
                return False
    return True

def validate_param(method, filedsAndValidator):
    def decorator(func):
        def validated_func(request, **kwargs):
            if not request.method == method:
                return func(request)
            if request.method == 'GET':
                query_param = request.GET
                if not apply_validator(query_param, filedsAndValidator):
                    return response_data(1, 'Invalid Param', [])
            if request.method != 'GET' and request.body:
                json_data = json.loads(request.body)
                print(json_data)

                if not apply_validator(json_data, filedsAndValidator):
                    return response_data(1, 'Invalid Param', [])
            return func(request)
        return validated_func
    return decorator

def is_authenticated(func):
    def authenticated_func(request):
        if request.user and request.user.is_authenticated:
            return func(request)
        else:
            return response_data(1, 'User not authenticated', [])
    return authenticated_func

def get_current_customer(func):
    def authenticated_func(request):
        if request.user and request.user.is_authenticated:
            customer = request.user.customer
            return func(request, customer)
        else:
            return response_data(1, 'User not authenticated', [])
    return authenticated_func
