import os
import zipfile
import json

def tuple2str(var):
    from copy import deepcopy
    
    if not isinstance(var,dict):
        return var
    
    newvar={}
    for key in var:
        if isinstance(key,tuple):  # either a board or board and player
            newtuple=[]
            for v in key:
                try:
                    len(v)
                    newtuple.append(tuple(v))
                except TypeError:
                    newtuple.append(v)

            newvar[str(tuple(newtuple))]=tuple2str(var[key])
        else:
            newvar[key]=tuple2str(var[key])
            
        
    return newvar

def str2table(var):
    from copy import deepcopy
    
    if not isinstance(var,dict):
        return var
    
    newvar=Table()
    for key in var:
        if (isinstance(key,str) or isinstance(key,unicode)) and key.startswith('(') and key.endswith(')'): # this is a tuple
            newkey=eval(key)
            newvar[newkey]=str2table(var[key])
        else:
            try:
                newkey=int(key)
            except ValueError:
                newkey=key
                
            newvar[newkey]=str2table(var[key])
            
        
    return newvar


def make_immutable(var):
    from copy import deepcopy
    
    try:
        var=var.immutable()
    except AttributeError:
        var=deepcopy(var)

    if isinstance(var,tuple):
        var=list(var)
    
    if isinstance(var,list):
        for i in range(len(var)):
            var[i]=make_immutable(var[i])
        return tuple(var)
    else:
        return var
        
class Table(dict):

    def __init__(self, other=None,**kwargs):
        
        if other:
            # Doesn't do keyword args
            if isinstance(other, dict):
                for k,v in list(other.items()):
                    k=make_immutable(k)
                    dict.__setitem__(self, k, v)
            else:
                for k,v in other:
                    k=make_immutable(k)
                    dict.__setitem__(self, k.lower(), v)

        if kwargs:
            for k,v in kwargs:
                k=make_immutable(k)
                dict.__setitem__(self, k.lower(), v)
            

    def max(self):
        s=[]
        for key in self.keys():
            s.append(self[key])

        return max(s)

    def argmax(self):
        
        s=[]
        for key in self.keys():
            s.append(self[key])

        argmax=max(zip(s, range(len(s))))[1]
        return argmax

    def min(self):
        s=[]
        for key in self.keys():
            s.append(self[key])

        return min(s)

    def __getitem__(self, key):
        key=make_immutable(key)
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        key=make_immutable(key)
        dict.__setitem__(self, key, value)

    def __contains__(self, key):
        key=make_immutable(key)
        try:
            value=dict.__contains__(self, key)
        except TypeError:
            print("Key is %s" % str(key))
            raise
        return value

    def has_key(self, key):
        key=make_immutable(key)
        return dict.has_key(self, key)

    def get(self, key, def_val=None):
        key=make_immutable(key)
        return dict.get(self, key, def_val)

    def setdefault(self, key, def_val=None):
        key=make_immutable(key)
        return dict.setdefault(self, key, def_val)

    def update(self, other):
        for k,v in list(other.items()):
            k=make_immutable(k)
            dict.__setitem__(self, k.lower(), v)

    def fromkeys(self, iterable, value=None):
        d = Dict()
        for k in iterable:
            k=make_immutable(k)
            
            dict.__setitem__(d, k, value)
        return d

    def pop(self, key, def_val=None):
        key=make_immutable(key)
        
        return dict.pop(self, key, def_val)
    
    def save(self,filename):
        SaveTable(self,filename)
        
    def load(self,filename):
    
        obj=LoadTable(filename)
        
        for key in obj:
            self[key]=obj[key]
        

def SaveTable(obj, filename='_memory_.json'):
    """Saves an object to disk
    
    Example:  Save([1,2,3])
    """
    
    if filename.endswith('.zip'):
        with zipfile.ZipFile(filename, 'w', compression=zipfile.ZIP_DEFLATED) as f:
            f.writestr(filename[:-4],json.dumps(tuple2str(obj),sort_keys=True, indent=4))
    else:
        with open(filename, 'w') as f:
            json.dump(tuple2str(obj),f, sort_keys=True, indent=4,)

def LoadTable(filename='_memory_.json',handle_exist=True):
    """Loads an object from disk

    Example:  a=Load()
    """
    if handle_exist:
        if not os.path.exists(filename):
            T=Table()
            SaveTable(T,filename)
            return T

    if '.zip' in filename:
        with zipfile.ZipFile(filename, 'r') as f:
            data = f.read(filename[:-4])
            obj = json.loads(data)
    else:
        with open(filename,'r') as f:
            obj = json.load(f)

            
    obj=str2table(obj)
        
        
    return obj
