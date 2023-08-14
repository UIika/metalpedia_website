from .models import Year
from django.db.models import Min

def default_year(request):
    return {'default_year': Year.objects.values('number').aggregate(Min('number'))['number__min']}