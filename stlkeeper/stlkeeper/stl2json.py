import sys
import os
import re
import string

class StlSolid :
    def __init__(self) :
        self.facets = []
        
    def addFacet(self, f) :
        self.facets.append(f)
                
    def __str__(self) :
        s = []
        for f in self.facets :
            s.append(f.__str__())
        return '[%s]' % string.join(s, ',')
    
    def loadFromFile(self, file_name):
        self._loadFromAsciiStlFile(file_name)
        
    def _loadFromAsciiStlFile(self, file_name):
        float_val_pattern = '[+-]?\d+(?:\.\d+)?(?:[Ee][+-]\d+)?'   #1.84e+006  
  
        facet_begin_regex = re.compile('^\s*facet\s+normal\s+(%s)\s+(%s)\s+(%s)\s*$' % (float_val_pattern, float_val_pattern, float_val_pattern) );  
        facet_end_regex   = re.compile('^\s*endfacet\s*$');  

        loop_begin_regex  = re.compile('^\s*outer\s+loop\s*$');
        loop_end_regex    = re.compile('^\s*endloop\s*$');

        vertex_regex      = re.compile('^\s*vertex\s+(%s)\s+(%s)\s+(%s)\s*$' % (float_val_pattern, float_val_pattern, float_val_pattern));

        stl_file = open(file_name, 'r')

        # check if file is ASCII stl file
        line = stl_file.readline()
        if not re.match('^\s*solid\s+\S*\s*$', line) :
            raise Exception("Input is not valid ASCII STL file")

        state = 0
        for line in stl_file :
            if state == 0 : 
                r = facet_begin_regex.match(line) 
                if r :
                    facet = StlFacet()
                    facet.setNormal(r.group(1), r.group(2), r.group(3))
                    state = 1
            elif state == 1 :
                if loop_begin_regex.match(line) :
                    state = 2
            elif state == 2 :
                r = vertex_regex.match(line)
                if r :
                    facet.addVertex( r.group(1), r.group(2), r.group(3) )
                elif loop_end_regex.match(line) :            
                    state = 3
            elif state == 3 :
                if facet_end_regex.match(line) :
                    self.addFacet(facet)
                    facet = None
                    state = 0
        
class StlFacet :
    def __init__(self) :
        self.vertices = []
        self.normal = [0, 0, 0]
        
    def setNormal(self, x, y, z) :
        self.normal = [x, y, z]        
        
    def addVertex(self, x, y, z) :
        if len(self.vertices) < 3 : 
            self.vertices.append([x, y, z])
        else :
            raise Exception("Too mane vertices")
            
    def __str__(self) :
        s = []
        for v in self.vertices :
             s.append( '[%s]' % string.join(v, ',') )             
        return '{"n":[%s],"v":[%s]}' % (string.join(self.normal, ','), string.join(s, ','))
        
