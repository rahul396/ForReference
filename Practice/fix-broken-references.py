import re
import os
import transaction as zt
from ZODB.utils import p64
from persistent import Persistent


refs_file = open('fsrefs-output.txt', 'r')
oids = []
for line in refs_file:
    if "missing: '<unknown>'" in line:
    	tokens = line.split(' ')
    	oid = tokens[1]
        if oid not in oids:
    	   oids.append(oid)


i = 0
for oid in oids:
    zt.begin()
    i += 1
    print("create fake obj [%s] for: %s" % (i, str(oid)))
    a = Persistent()
    try:
        oid_int = int(oid, 16)
    except ValueError:
        print("ValueEror on %s, skip!" % oid)
        zt.abort()
        continue
    a._p_oid = p64(oid_int)
    a._p_jar = app._p_jar
    app._p_jar._register(a)
    app._p_jar._added[a._p_oid] = a
    zt.commit()
print("finished!")

