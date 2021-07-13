from rest_framework.decorators import api_view


@api_view(['GET', 'SET'])
def mailing_lists(request):

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
