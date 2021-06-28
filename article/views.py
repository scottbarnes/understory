from django.shortcuts import render
from django.http import HttpResponseServerError
# from django.http import HttpResponse


def error_500_test_view(request):
    """ Return an "Internal Server Error" 500 response code. """
    # return HttpResponse(status=500)
    return HttpResponseServerError()
