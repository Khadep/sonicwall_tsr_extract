import re

with open("C:/Users/lucidity/Downloads/techSupport_8FF542_11-16.wri") as v:
    txt = v.read()


def extractobject(txt):
    # The following regex matches the network objects section of the tsr
    x = re.search(
        r"(?s)--Address Object Table--(.*)Network Object Manager", txt)
    objectstring = x.group(0)
    objects = objectstring.splitlines()
    objectdict = {}

    # The following function takes the objects and puts them into a dictionary called objectdict the key is the object name and the value is the ip info
    for x in objects:
        if '------' and '(' in x:
            pass
            #print('not an object header')
        elif x == '':
            pass
            #print('This is empty')
        elif '------' in x:
            objectitem = (objects[objects.index(x)+4])
            objectitems = objectitem.split(":")
            # the following regex matches on the name of the object.
            objectname1 = re.search(r"(?s)(?<=-------).*?(?=-------)", x)
            objectname = objectname1.group(0)
            objectdict[objectname] = objectitems
        elif 'Network Object Manager' in x:
            break
    print(objectdict)


def extractgroupobject(txt):
    # The following regex matches the network objects group section of the tsr
    y = re.search(
        r"(?s)--Address Group Table--(.*?)--Address Object Table--", txt)
    objectgroupstring = y.group(0)
    objectgroups = objectgroupstring.splitlines()
    objectgroupdict = {}
    # The following function takes the object groups and puts them into a dictionary called objectgroup dict. The key is the object group name and the values are the group members
    try:
        for y in objectgroups:
            if '-------' in y and 'Custom' in (objectgroups[objectgroups.index(y)+2]) and (objectgroups[objectgroups.index(y)+4]) != '':
                i = objectgroups.index(y)+4
                # the following regex matches on the name of the object.
                objectgroupname1 = re.search(
                    r"(?s)(?<=-------).*?(?=-------)", y)
                objectgroupname = objectgroupname1.group(0)
                objectlist = []
                # the following appends members of the group to a list that is added as a value to the dictionary.
                while i > 0:
                    objectmember1 = re.search(
                        r"(?s)(?<=Name:).*?(?=Handle:)", objectgroups[i])
                    objectmember = objectmember1.group(0)
                    objectlist += [objectmember]
                    i += 1
                    if objectgroups[i] == '':
                        objectgroupdict.update({objectgroupname: objectlist})
                        break
    except IndexError:
        print(IndexError)
    print(objectgroupdict)


def extractserviceobject(txt):
    # The following regular expression matches on service objects within the tsr file.
    z = re.search(
        r"(?s)--Service Object Table--(.*)--Route Advertisement--", txt)
    serviceobjectstring = z.group(0)
    serviceobjects = serviceobjectstring.splitlines()
    serviceobjectdict = {}
    # the following function adds service objects to the service object dictionary. It adds the IP type(tcp vs udp etc) and the port number/range then adds the values to the dictionary with the service object name as the key.
    for z in serviceobjects:
        if '-------' in z and 'Ports:' in (serviceobjects[serviceobjects.index(z)+1]):
            serviceobjectstring = serviceobjects[serviceobjects.index(z)+1]
            # the following regex matches on the service object ports.
            serviceobjectports1 = re.search(r"Ports:.*$", serviceobjectstring)
            # the following regex matches on the name of the object.
            serviceobjectname1 = re.search(
                r"(?s)(?<=-------).*?(?=-------)", z)
            # the following regex matches on IP type which is based on a number.
            serviceobjecttype1 = re.search(
                r"(?s)(?<=IpType: ).*?(?=,)", serviceobjectstring)
            serviceobjecttypenumber = serviceobjecttype1.group(0)
            serviceobjectports = serviceobjectports1.group(0)
            serviceobjectname = serviceobjectname1.group(0)
            serviceobject = serviceobjectports.split(":")
            serviceobjectconvert = serviceobject[1].replace("~", "-")
            # the following if then statement finds the IP type based on the number.
            if serviceobjecttypenumber == '6':
                serviceobjecttype = 'TCP'
            elif serviceobjecttypenumber == '17':
                serviceobjecttype = 'UDP'
            elif serviceobjecttypenumber == '1':
                serviceobjecttype = 'ICMP'
            elif serviceobjecttypenumber == '58':
                serviceobjecttype = 'IPv6-ICMP'
            serviceobjectlist = []
            normalizeserviceobject = serviceobjectconvert.split("-")
            # If the starting port number and ending port numberare the same, then just use one port number
            if normalizeserviceobject[0].strip() == normalizeserviceobject[1]:
                serviceobjectconvert = normalizeserviceobject[1]
            serviceobjectlist += [serviceobjecttype]
            serviceobjectlist += [serviceobjectconvert.strip()]
            serviceobjectdict[serviceobjectname] = [serviceobjectlist]
        elif '--Route Advertisement--' in z:
            break

    print(serviceobjectdict)


extractobject(txt)
extractgroupobject(txt)
extractserviceobject(txt)
