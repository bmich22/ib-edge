from django.http import HttpResponseNotFound


def handler404(request, exception):
    return HttpResponseNotFound("This is a plain 404 page.")