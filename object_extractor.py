#!/usr/bin/python

import re
import csv
import sys

with open(sys.argv[1], 'r') as tsr_path:
    txt = tsr_path.read()


def extractobject(txt):
    # The following regex matches the network objects section of the tsr
    x = re.search(
        r"(?s)--Address Object Table--(.*)Network Object Manager", txt)
    objectstring = x.group(0)
    objects = objectstring.splitlines()
    objectlist = []
    # The following function takes the objects and puts them into a dictionary called objectdict the key is the object name and the value is the ip info
    for x in objects:
        if '------' in x and 'Custom' in objects[objects.index(x)+2]:
            objectdict = {}
            objectitem = (objects[objects.index(x)+4])
            objectitems = objectitem.split(":")
            print(objectitem)
            # the following regex matches on the name of the object.
            objectname1 = re.search(r"(?s)(?<=-------).*?(?=-------)", x)
            objectname = objectname1.group(0)
            # remove the following hash if you want to keep whitespaces, backslash, and parenthesis in the object name comment out the second "objectdict['NAME']" line
            #objectdict['NAME'] = objectname
            objectdict['NAME'] = objectname.replace('(', '_').replace(')', '_').replace(
                '/', '_').replace('\\', '_').replace(' ', '_')
            objectdict['TYPE'] = objectitems[0]
            objectdict['VALUE'] = objectitems[1].strip()
            objectlist.append(objectdict)
        elif '-------' in x:
            objectdict = {}
            objectitem = (objects[objects.index(x)+3])
            objectitems = objectitem.split(":")
            print(objectitem)
            # the following regex matches on the name of the object.
            objectname1 = re.search(r"(?s)(?<=-------).*?(?=-------)", x)
            objectname = objectname1.group(0)
            # remove the following hash if you want to keep whitespaces, backslash, and parenthesis in the object name comment out the second "objectdict['NAME']" line
            #objectdict['NAME'] = objectname
            objectdict['NAME'] = objectname.replace('(', '_').replace(')', '_').replace(
                '/', '_').replace('\\', '_').replace(' ', '_')
            objectdict['TYPE'] = objectitems[0]
            objectdict['VALUE'] = objectitems[1].strip()
            objectlist.append(objectdict)
        elif 'Network Object Manager' in x:
            break
    print(objectlist)
    extractobject.var = objectlist
    return(objectlist)


def extractobjectgroup(txt):
    # The following regex matches the network objects group section of the tsr
    y = re.search(
        r"(?s)--Address Group Table--(.*?)--Address Object Table--", txt)
    objectgroupstring = y.group(0)
    objectgroups = objectgroupstring.splitlines()
    objectgroupdict = {}
    extractgrouplist = []
    # The following function takes the object groups and puts them into a dictionary called objectgroup dict. The key is the object group name and the values are the group members
    try:
        for y in objectgroups:
            if '-------' in y and 'Custom' in (objectgroups[objectgroups.index(y)+2]) and (objectgroups[objectgroups.index(y)+4]) != '':
                i = objectgroups.index(y)+4
                print(y)
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
                    objectlist += [objectmember.strip().replace('(', '_').replace(
                        ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')]
                    i += 1
                    if objectgroups[i] == '':
                        extractgroupdict = {}
                        objectgroupdict.update({objectgroupname.strip().replace('(', '_').replace(
                            ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_'): objectlist})
                        extractgroupdict['NAME'] = objectgroupname.strip().replace('(', '_').replace(
                            ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')
                        extractgroupdict['Members'] = objectlist
                        extractgrouplist.append(extractgroupdict)
                        break
            elif '-------' in y and "member" in (objectgroups[objectgroups.index(y)+3]):
                i = objectgroups.index(y)+3
                print(y)
                print(i)
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
                    objectlist += [objectmember.strip().replace('(', '_').replace(
                        ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')]
                    i += 1
                    if objectgroups[i] == '':
                        extractgroupdict = {}
                        objectgroupdict.update({objectgroupname.strip().replace('(', '_').replace(
                            ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_'): objectlist})
                        extractgroupdict['NAME'] = objectgroupname.strip().replace('(', '_').replace(
                            ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')
                        extractgroupdict['Members'] = objectlist
                        extractgrouplist.append(extractgroupdict)
                        break
    except IndexError:
        print(IndexError)
    print(objectgroupdict)
    extractobjectgroup.var = extractgrouplist


def extractserviceobject(txt):
    z = re.search(
        r"(?s)--Service Object Table--(.*)--Route Advertisement--", txt)
    serviceobjectstring = z.group(0)
    serviceobjects = serviceobjectstring.splitlines()
    serviceobjectlist = []
    servicelist = []
    # the following function adds service objects to the service object dictionary. It adds the IP type(tcp vs udp etc) and the port number/range then adds the values to the dictionary with the service object name as the key.
    for z in serviceobjects:
        if '-------' in z and 'IpType:' in (serviceobjects[serviceobjects.index(z)+1]):
            serviceobjectstring = serviceobjects[serviceobjects.index(z)+1]
            # the following regex matches on the service object ports.
            serviceobjectports1 = re.search(r"Ports:.*$", serviceobjectstring)
            # the following regex matches on the name of the object.
            if z.count('(') > 1:
                serviceobjectname1 = re.search(
                    r"(?s)(?<=-------).*?(.*?\(){2}", z)
            elif z.count('(') == 1:
                serviceobjectname1 = re.search(
                    r"(?s)(?<=-------).*?(?=\()", z)
            else:
                serviceobjectname1 = re.search(
                    r"(?s)(?<=-------).*?(?=-------)", z)
            # the following regex matches on IP type which is based on a number.
            serviceobjecttype1 = re.search(
                r"(?s)(?<=IpType: ).*?(?=,)", serviceobjectstring)
            icmptype = ""
            icmpcode = ""
            serviceobjectports = ""
            print(serviceobjectstring)
            if 'IcmpType' in serviceobjectstring:
                icmptype1 = re.search(
                    r"(?s)(?<=IcmpType: ).*?(?=I)", serviceobjectstring)
                icmpcode1 = re.search(
                    r"(?s)(?<=IcmpCode: ).*?(?<=$)", serviceobjectstring)
                icmptype = icmptype1.group(0)
                icmpcode = icmpcode1.group(0)
            else:
                serviceobjectports = serviceobjectports1.group(0)
                serviceobject = serviceobjectports.split(":")
                serviceobjectconvert = serviceobject[1].replace("~", "-")
                normalizeserviceobject = serviceobjectconvert.split("-")
                # If the starting port number and ending port numberare the same, then just use one port number
                if normalizeserviceobject[0].strip() == normalizeserviceobject[1]:
                    serviceobjectconvert = normalizeserviceobject[1]
            serviceobjecttypenumber = serviceobjecttype1.group(0)
            serviceobjectname = serviceobjectname1.group(0)
            serviceobjectname = serviceobjectname.rstrip('(')
            # the following if then statement finds the IP type based on the number.
            if serviceobjecttypenumber == '6':
                serviceobjecttype = 'TCP'
            elif serviceobjecttypenumber == '17':
                serviceobjecttype = 'UDP'
            elif serviceobjecttypenumber == '1':
                serviceobjecttype = 'ICMP'
            elif serviceobjecttypenumber == '58':
                serviceobjecttype = 'IPv6-ICMP'
            # NAME,PROTOCOL,PORT,ICMPCODE,ICMPTYPE
            serviceobjectdict = {}
            # remove the following hash if you want to keep whitespaces, backslash, and parenthesis in the object name comment out the second "serviceobjectdict['NAME']" line
            #serviceobjectdict['NAME'] = serviceobjectname
            serviceobjectdict['NAME'] = serviceobjectname.strip().replace('(', '_').replace(
                ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')
            servicelist += [serviceobjectname.replace('(', '_').replace(')', '_').replace(
                '/', '_').replace('\\', '_').replace(' ', '_')]
            serviceobjectdict['PROTOCOL'] = serviceobjecttype
            if icmpcode != "":
                serviceobjectdict['ICMPCODE'] = icmpcode
                serviceobjectdict['ICMPTYPE'] = icmptype
            else:
                serviceobjectdict['PORT'] = serviceobjectconvert.strip()
            serviceobjectlist.append(serviceobjectdict)
        elif '--Route Advertisement--' in z:
            break
    print(serviceobjectlist)
    print(servicelist)
    extractserviceobject.list = servicelist
    extractserviceobject.var = serviceobjectlist

    return(serviceobjectlist)


def extractservicegroup(txt):
    # The following regex matches the network  service objects group section of the tsr
    a = re.search(
        r"(?s)--Service Group Table--(.*?)--Service Object Table--", txt)
    servicegroupstring = a.group(0)
    servicegroups = servicegroupstring.splitlines()
    servicegroupdict = {}
    extractservicegrouplist = []
    # The following function takes the object groups and puts them into a dictionary called servicegroupdict. The key is the object group name and the values are the group members
    for a in servicegroups:
        if '-------' in a and 'member' in (servicegroups[servicegroups.index(a)+3]):
            i = servicegroups.index(a)+3
            # the following regex matches on the name of the object.
            #objectgroupname1 = re.search(r"(?s)(?<=-------).*?(?=-------)", a)
            if a.count('(') > 1:
                objectgroupname1 = re.search(
                    r"(?s)(?<=-------).*?(.*?\(){2}", a)
            elif a.count('(') == 1:
                objectgroupname1 = re.search(r"(?s)(?<=-------).*?(?=\()", a)
            else:
                objectgroupname1 = re.search(
                    r"(?s)(?<=-------).*?(?=-------)", a)
            objectgroupname = objectgroupname1.group(0)
            objectlist = []
            # the following appends members of the group to a list that is added as a value to the dictionary.
            while i > 0:
                objectmember1 = re.search(
                    r"(?s)(?<=Name:).*?(?=Handle:)", servicegroups[i])
                objectmember = objectmember1.group(0)
                if objectmember.strip().replace('(', '_').replace(
                        ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_') not in extractserviceobject.list:
                    print(objectmember + " member is not custom")
                objectlist += [objectmember.strip().replace('(', '_').replace(
                    ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')]

                i += 1
                if servicegroups[i] == '':
                    extractservicegroupdict = {}
                    servicegroupdict.update({objectgroupname.strip().replace('(', '_').replace(
                        ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_'): objectlist})
                    extractservicegroupdict['NAME'] = objectgroupname.strip().replace('(', '_').replace(
                        ')', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')
                    extractservicegroupdict['Members'] = objectlist
                    extractservicegrouplist.append(extractservicegroupdict)
                    break
    extractservicegroup.var = extractservicegrouplist
    print(extractservicegrouplist)
    print("***")
    print(servicegroupdict)


def exportobject_tocsv():
    # Here we are exporting the objects to csv
    extractobject(txt)
    csv_columns = ['NAME', 'DESCRIPTION', 'TYPE', 'VALUE', 'LOOKUP']
    csv_file = "sonicwallobjects.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=csv_columns, lineterminator='\n')
            writer.writeheader()
            for data in extractobject.var:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def exportobject_groups_tocsv():
    extractobjectgroup(txt)
    # Here we are exporting the service objects to csv
    csv_columns = ['NAME', 'Members']
    csv_file = "sonicwallobjectgroups.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=csv_columns, lineterminator='\n')
            writer.writeheader()
            for data in extractobjectgroup.var:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def exportservice_object_tocsv():
    extractserviceobject(txt)
    # Here we are exporting the service objects to csv
    csv_columns = ['NAME', 'PROTOCOL', 'PORT', 'ICMPCODE', 'ICMPTYPE']
    csv_file = "sonicwallserviceobjects.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=csv_columns, lineterminator='\n')
            writer.writeheader()
            for data in extractserviceobject.var:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def exportservice_groups_tocsv():
    extractservicegroup(txt)
    # Here we are exporting the service objects to csv
    csv_columns = ['NAME', 'Members']
    csv_file = "sonicwallservicegroups.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=csv_columns, lineterminator='\n')
            writer.writeheader()
            for data in extractservicegroup.var:
                writer.writerow(data)
    except IOError:
        print("I/O error")


exportobject_tocsv()
exportobject_groups_tocsv()
exportservice_object_tocsv()
exportservice_groups_tocsv()
