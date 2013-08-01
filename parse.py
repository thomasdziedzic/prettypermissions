from lxml import etree
import glob

#tree = etree.parse(open("Standard.profile"))

#root = tree.getroot()

obj = "Account"

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
                    permission_str += "r"
                else: # not readable
                    permission_str += "nr"

                permission_str += " - "

                if editable == "true":
                    permission_str += "e"
                else: # not editable
                    permission_str += "ne"

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
