   from django.contrib import admin
from .models import DomainAnalysis
from .models import Results


admin.site.register(Results)
admin.site.register(DomainAnalysis)

# Register your models here.
