# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class HostsStore(models.Model):
    host = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.id) + " " + self.host

class UserAgentsStore(models.Model):
    user_agent = models.CharField(max_length=800)

    def __str__(self):
        return str(self.id) + " " + self.user_agent[:20]

class RewritesStore(models.Model):
    host = models.ForeignKey(HostsStore)
    user_agent = models.ForeignKey(UserAgentsStore)
    rewrite_condition = models.CharField(max_length=800)
    rewrite_location = models.CharField(max_length=800)
    
    def __str__(self):
        return str(self.host) + "_" + str(self.user_agent) + " " + self.rewrite_condition 

    
