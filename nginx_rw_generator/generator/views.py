# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import HostsStore, UserAgentsStore, RewritesStore

# Create your views here.

@csrf_exempt
def addRule(request):

    host = request.POST.get("host")
    ua = request.POST.get("ua")
    condition = request.POST.get("condition")
    location = request.POST.get("location")

    if host and not HostsStore.objects.filter(host=host):        
        host_entry = HostsStore(host=host)        
        host_entry.save()

    host_id = HostsStore.objects.filter(host=host)[0]

    if ua and not UserAgentsStore.objects.filter(user_agent=ua):
        ua_entry = UserAgentsStore(user_agent=ua)
        ua_entry.save()
    ua_id = UserAgentsStore.objects.filter(user_agent=ua)[0]

    rw_entry = RewritesStore(host=host_id, user_agent=ua_id,
        rewrite_condition=condition, rewrite_location=location)
    rw_entry.save()

    return render(request, 'index.html',
        context={"data":" ".join([host,ua,condition,location,])})
    
def createConfig(request):
    
    hosts_set_conf = open("./hosts_set.conf", "wr")
    ua_set_conf = open("./ua_set.conf", "wr")
    rewrites_conf = open("./rewrites.conf", "wr")

    hosts = []
    user_agents = []
    rewrites = []

    for host in HostsStore.objects.all():
        hosts.append("if ($host = '%s')\n  {\n set $host_id '%d';\n  }\n" % (host.host, host.id))
    for ua in UserAgentsStore.objects.all():
        user_agents.append("if ($host = '%s')\n  {\n set $ua_id '%d';\n  }\n" % (ua.user_agent, ua.id))
    for rw in RewritesStore.objects.all():
        data = (rw.host.id, rw.user_agent.id, rw.rewrite_condition, rw.rewrite_location)
        rewrites.append("  set $rw_id '$host_id, $ua_id';\n   if ($rw_id = '2 %d, %d')\n  {\n rewrite %s %s permanent;\n  }\n" % data)

    for rule in hosts:
        hosts_set_conf.write(rule)
    hosts_set_conf.close()
    for rule in user_agents:
        ua_set_conf.write(rule)
    ua_set_conf.close()
    for rule in rewrites:
        rewrites_conf.write(rule)
    rewrites_conf.close()
        
    return render(request, "index.html", context={"data":"Succesfull"})  
    
        
    
