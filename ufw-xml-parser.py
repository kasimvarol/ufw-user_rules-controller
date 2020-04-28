import xml.etree.ElementTree as ET

XML_FILE = 'ufw.xml'
USER_RULES = '/etc/ufw/user.rules'

# Parse and access rule members.
ufw = ET.parse(XML_FILE)
rules = ufw.getroot()
rules=rules[0]
rule_arr=[]

# Create a new rule from parsed member.
for rule in rules:
	newrule = {"protocol" : "any", "port" : "any", "ip" : "0.0.0.0/0"}
	for key in newrule:
		if key in rule.attrib.keys() and len(rule.attrib[key])!=0:

			# multiports are not allowed for both protocols
			if key=="port" and ":" in rule.attrib["port"]:
				if "protocol" not in rule.attrib.keys() or not (rule.attrib["protocol"]=="tcp" or rule.attrib["protocol"]=="udp"):
					raise ValueError('If you specify multiports, protocol should be either tcp or udp!')
			newrule[key]=rule.attrib[key]

	# rule should have either ip or port values.		
	if newrule["ip"]=="0.0.0.0/0" and newrule["port"]=="any":
		raise ValueError('For each rule at least ip or port should be specified!')

	newrule["action"] = rule.tag
	rule_arr.append(newrule)

# Writing parsed rule
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