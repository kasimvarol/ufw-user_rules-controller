import xml.etree.ElementTree as ET

XML_FILE = 'ufw.xml'
USER_RULES = '/etc/ufw/user.rules'

ufw = ET.parse(XML_FILE)
rules = ufw.getroot()
rules=rules[0]
rule_arr=[]

for rule in rules:
	newrule = {"protocol" : "any", "port" : "any", "ip" : "0.0.0.0/0"}
	for key in newrule:
		if key in rule.attrib.keys() and len(rule.attrib[key])!=0: 
			newrule[key]=rule.attrib[key]
	newrule["action"] = rule.tag
	rule_arr.append(newrule)

for member in rule_arr:
	newrule = '\n### tuple ### {} {} {} 0.0.0.0/0 any {} in\n'.format(member["action"], member["protocol"], member["port"], member["ip"])
	with open(USER_RULES, "r") as in_file:
		buf = in_file.readlines()
	with open(USER_RULES, "w") as out_file:
		if member["ip"]=="0.0.0.0/0":
			for i in range(len(buf)):
				if i!=len(buf)-1 and buf[i+1] == "### END RULES ###\n":
					buf[i] = buf[i] + newrule
				out_file.write(buf[i])
		else:
			for i in range(len(buf)):
				if buf[i] == "### RULES ###\n":
					buf[i] = buf[i] + newrule
				out_file.write(buf[i])