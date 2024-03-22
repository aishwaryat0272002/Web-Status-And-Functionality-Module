from django.db import models
from django.utils import timezone

class DomainAnalysis(models.Model):
    domain = models.CharField(max_length=255)
    public_ip = models.CharField(max_length=15)
    http_status = models.PositiveIntegerField(null=True, blank=True)
    https_status = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now) 

     
    def __str__(self):
        return self.domain

class Results(models.Model):
    domain = models.CharField(max_length=100)
    Public_ip = models.CharField(max_length=100)
    status_code_if_redirected = models.CharField(max_length=100,null=True,blank=True)
    http_status = models.CharField(max_length=100)
    https_redirect_url = models.CharField(max_length=100,null=True,blank=True)
    https_status = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now) 
    
    
    # http_final_url = models.CharField(max_length=100)
    # http_public_ip = models.CharField(max_length=100)
   
    
    # https_final_url = models.CharField(max_length=100)
    # https_public_ip = models.CharField(max_length=100)
    # remarks = models.CharField(max_length=100)
        


