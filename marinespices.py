import navegador5 as nv 
import navegador5.url_tool as nvurl
import navegador5.head as nvhead
import navegador5.body as nvbody
import navegador5.cookie 
import navegador5.cookie.cookie as nvcookie
import navegador5.cookie.rfc6265 as nvrfc6265
import navegador5.jq as nvjq
import navegador5.js_random as nvjr
import navegador5.file_toolset as nvft
import navegador5.shell_cmd as nvsh
import navegador5.html_tool as nvhtml
import navegador5.solicitud as nvsoli
import navegador5.content_parser 
import navegador5.content_parser.amf0_decode as nvamf0
import navegador5.content_parser.amf3_decode as nvamf3

from lxml import etree
import lxml.html
import collections
import copy
import re
import urllib
import os
import json
import sys

from xdict.jprint import  pobj
from xdict.jprint import  print_j_str
from xdict import cmdline





#Taxonomic data
#http://www.marinespecies.org/rest/AphiaChildrenByAphiaID/1?marine_only=false&offset=2 
#-H "accept: application/json"


# /AphiaChildrenByAphiaID/{ID}Get the direct children (max. 50) for a given AphiaID


def get_json(info_container):
    js = info_container['resp_body_bytes'].decode('utf-8')
    js = json.loads(js)
    return(js)



def mkdir(path,force=False):
    if(os.path.exists(path)):
        if(force):
            nvsh.pipe_shell_cmds({1:'rm -r '+path})
        else:
            pass
    else:
        os.makedirs(path)







def marinespecies_init(base_url='http://www.marinespecies.org/'):
    info_container = nvsoli.new_info_container()
    info_container['base_url'] = base_url
    info_container['method'] = 'GET'
    req_head_str = '''Accept: application/json\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en;q=1.0, zh-CN;q=0.8'''
    info_container['req_head'] = nvhead.build_headers_dict_from_str(req_head_str,'\r\n')
    info_container['req_head']['Connection'] = 'close'
    #### init records_container
    records_container = nvsoli.new_records_container()
    return((info_container,records_container))



def AphiaChildrenByAphiaID_internal(info_container,records_container,ID,marine_only=True,offset=1):
    if(marine_only):
        marine_only = 'true'
    else:
        marine_only = 'false'
    url_query_dict = {'marine_only':marine_only,'offset':str(offset)}
    url_dict = {
        'fragment': '', 
        'query_dict': url_query_dict, 
        'host': 'www.marinespecies.org', 
        'port': 80, 
        'params': '', 
        'scheme': 'http', 
        'path': ''.join(('rest/AphiaChildrenByAphiaID/',str(ID))), 
        'netloc': 'www.marinespecies.org'
    }
    url = nvurl.dict_to_url(url_dict).rstrip('#')
    info_container['url'] = url
    info_container = nvsoli.walkon(info_container,records_container=records_container)
    info_container = nvsoli.auto_redireced(info_container,records_container)
    return((info_container,records_container))


def AphiaChildrenByAphiaID(info_container,records_container,marine_only=True):
    rslt = []
    curr_offset = 1
    info_container,records_container = AphiaChildrenByAphiaID_internal(info_container,records_container,1,marine_only=marine_only,offset=curr_offset)
    cond = not(info_container['resp_body_bytes'] == b'')
    while(cond):
        js = get_json(info_container)
        rslt = rslt + js
        curr_offset = curr_offset + js.__len__()
        info_container,records_container = AphiaChildrenByAphiaID_internal(info_container,records_container,1,marine_only=marine_only,offset=curr_offset)
        cond = not(info_container['resp_body_bytes'] == b'')
    return((info_container,records_container,rslt))


info_container,records_container = marinespecies_init()
info_container,records_container,rslt = AphiaChildrenByAphiaID(info_container,records_container,marine_only=True)


next_unhandled = {}
for each in rslt:
    parent_path = '../Biota/'
    dir_name = each['scientificname']
    path = parent_path + dir_name
    mkdir(path)
    fn = path + '/info.json' 
    nvft.write_to_file(fn=fn,mode='b+')
    next_unhandled[path] = each['url']

unhandled = next_unhandled
next_unhandled = {}

while(unhandled.__len__()>0):
    for path in unhandled:
        parent_path = path
        info_container['url'] = unhandled[path]
        info_container,records_container,children = AphiaChildrenByAphiaID(info_container,records_container,marine_only=True)
        for child in children:
            dir_name = child['scientificname']
            path = parent_path + dir_name
            mkdir(path)
            fn = path + '/info.json' 
            nvft.write_to_file(fn = fn,mode='b+')
            if(child['AphiaID'] == 0):
                pass
            else:
                next_unhandled[path] = child['url']
#"AphiaID": 0
#
