
import pickle
import gzip
import os
from numpy import array 

             

def Save(obj, filename='_memory_.dat'):
    """Saves an object to disk
    
    Example:  Save([1,2,3])
    """

    f = gzip.open(filename,'wb')
    pickle.dump(obj,f,protocol=2)
    f.close()


def Load(filename='_memory_.dat'):
    """Loads an object from disk

    Example:  a=Load()
    """
    f = gzip.open(filename,'rb')
    try: 
        obj = pickle.load(f)
    except:
        obj = dict()
    f.close()

    return obj



def RememberOrig(*args,**kwargs):

    try:
        filename=kwargs['filename']
    except KeyError:
        filename='_memory_.dat'

    if len(args)>0:
        Save(args,filename)
        return

    Q=Load(filename)
    if len(Q)==1:
        Q=Q[0]
        
    return Q
    
data={}
data['default']=[]
def reset(name=None):
    global data
    
    if name==None:
        data={}
        data['default']=[]
    else:
        data[name]=[]
    
def store(*args,**kwargs):
    global data
    
    if 'name' in kwargs:
        name=kwargs['name']
    else:
        name='default'
    
    if name not in data:
        data[name]=[]
        
    if not args:
        data[name]=[]
    
    if not data[name]:
        for arg in args:
            data[name].append([arg])
            
    else:
        for d,a in zip(data[name],args):
            d.append(a)
    

def recall(name='default'):
    global data
    
    if name not in data:
        data[name]=[]
    
    for i in range(len(data[name])):
        data[name][i]=array(data[name][i])
    
    ret=tuple(data[name])
    if len(ret)==1:
        return ret[0]
    else:
        return ret




if __name__ == "__main__":
    import sys
    import os.path
    
    class Object:
        x = 7
        y = "This is an object."
    
    filename = sys.argv[1]
    if os.path.isfile(filename):
        o = load(filename)
        print("Loaded %s" % o)
    else:
        o = Object()
        save(o, filename)
        print("Saved %s" % o)

