with open("C:/Users/lucidity/Downloads/techSupport_8FF542_11-16.wri") as v:
    txt = v.read()

x = re.search(r"(?s)--Address Object Table--(.*)Network Object Manager", txt)
objectstring = x.group(0)
# print(objectstring.splitlines())
objects = objectstring.splitlines()
objectdict = {}

for x in objects:
    if '------' and '(' in x:
        pass
        #print('not an object header')
    elif x == '':
        pass
        #print('This is empty')
    elif '------' in x:
        # print(x)
        objectitem = (objects[objects.index(x)+4])
        objectitems = objectitem.split(":")
        objectname1 = re.search(r"(?s)(?<=-------).*?(?=-------)", x)
        objectname = objectname1.group(0)
        # print(objectname)
        # print(type(objectname))
        objectdict[objectname] = objectitems
        # print(objectdict)
        #objectdict[str(objectname)] += [objectitem[0], objectitem[1]]
    elif 'Network Object Manager' in x:
        break
print(objectdict)
