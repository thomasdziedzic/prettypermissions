from lxml import etree
import glob

obj = "Schedules_and_Actuals__c"
#obj = "OpportunityLineItem"
#obj = "Schedule_Header__c"

prefix = "{http://soap.sforce.com/2006/04/metadata}"

def initialize_fieldnames():
    fieldnames = []
    for event, element in etree.iterparse(open("Standard.profile", "rb")):
        if element.tag.endswith("fieldPermissions"):
            editable = element.find(prefix + 'editable').text
            field = element.find(prefix + 'field').text
            readable = element.find(prefix + 'readable').text
            if field.startswith(obj):
                fieldnames.append(field)
    return fieldnames

fieldnames = initialize_fieldnames()

print(fieldnames)

def initialize_profilenames():
    return glob.glob("*.profile")

profilenames = initialize_profilenames()

print(profilenames)

lines = []

for profilename in profilenames:
    line = []
    for event, element in etree.iterparse(open(profilename, "rb")):
        if element.tag.endswith("fieldPermissions"):
            editable = element.find(prefix + 'editable').text
            field = element.find(prefix + 'field').text
            readable = element.find(prefix + 'readable').text
            if field.startswith(obj):
                permission_str = ""

                if readable == "true":
                    permission_str += "read"
                else: # not readable
                    permission_str += "no read"

                permission_str += "-"

                if editable == "true":
                    permission_str += "edit"
                else: # not editable
                    permission_str += "no edit"

                line.append(permission_str)
    lines.append(line)

print(lines)

csv = ","
csv += str.join(',',fieldnames)
csv += "\n"
for i, profilename in enumerate(profilenames):
    csv += profilename + ","
    line = lines[i]
    csv += str.join(',', line)
    csv += "\n"

with open("permissions.csv", "w") as f:
    f.write(csv)
