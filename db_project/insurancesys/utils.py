from django.http import JsonResponse

def response_data(error_code,reason,data):
    return JsonResponse({
        'error_code': error_code,
        'error_reason': reason,
        'data': data,
    })