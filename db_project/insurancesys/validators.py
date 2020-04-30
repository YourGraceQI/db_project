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
    for filedName in filedsAndValidator:
        fieldValue = data.get(filedName)
        validators = filedsAndValidator.get(filedName)
        for validator in validators:
            if fieldValue is None:
                pass
            elif not validator(fieldValue):
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
                if not apply_validator(json_data, filedsAndValidator):
                    return response_data(1, 'Invalid Param', [])
            return func(request)
        return validated_func
    return decorator

