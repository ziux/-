import sys
import json
from pprint import pprint
args = sys.argv[1:]
for arg in args:
    try:
        with open(arg,'r',encoding='utf-8') as f:
            pprint(json.loads(f.read()))
    except:
        pprint(arg)