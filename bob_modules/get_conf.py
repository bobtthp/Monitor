import json
import os
import ConfigParser
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

def get_conf():

    with open(root_path + '/conf/config.json') as f:
        try:
            config = json.loads(f.read())
            #print config
        except ValueError  as e:
            print (e)
    return config

def get_log_conf(pname):
    if pname in get_conf().get('pname'):
        #print pname
        pconf = ConfigParser.ConfigParser()
        ppath = root_path + '/conf/' + pname + '.conf'
        if os.access(ppath,os.F_OK):
            pconf.read(ppath)
        else:
            print ('please check file' + ppath)
        return pconf
    else:
        print ('please check if '  + pname  + ' config.json !')


