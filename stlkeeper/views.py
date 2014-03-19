import os
import glob
from components.stl2json import StlSolid

from django.http import HttpResponse
from django.template import RequestContext, loader

def index(request) :
    
    stl_files = filter(lambda fn: fn.endswith('.stl'), os.listdir("/home/devil/Projects/part-modeller/data"))
        
    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'files': stl_files,
    })
    return HttpResponse(template.render(context))

def stl(request) :
    # returns json structure to show STL
    file_name = "/home/devil/Projects/part-modeller/data/%s" % request.GET['file']
    
    solid = StlSolid()
    solid.loadFromFile(file_name)
    
    return HttpResponse(solid)
