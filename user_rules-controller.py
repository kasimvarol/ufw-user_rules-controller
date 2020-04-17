USER_RULES = "/etc/ufw/user.rules"

# List updated rules
def list_rules():
    print('{0:10}{1:^10}{2:^20}{3:10}'.format("PORT", "PROTOCOL", "IP", "ACTION"))
    with open(USER_RULES) as f:
        data = f.read()
    for line in data.split("\n"):
        if "tuple" in line:
            rule = line[14:].split()
            print('{0:10}{1:^10}{2:^20}{3:10}'.format(rule[2], rule[1], rule[5], rule[0]))
    print("1. Add Port Allow\n2. Add IP Allow\n3. Exit")

# Add rules unless user exists
selection = 0                
while (True):
    list_rules()
    selection=int(input("What is your choice: "))
    rule = ""

# Allow port(single)
    if(selection==1):
        port=int(input("Which port: "))
        protocol=raw_input("Which protocol: ")#
        rule = '\n### tuple ### allow {} {} 0.0.0.0/0 any 0.0.0.0/0 in\n'.format(protocol, port)
        if protocol=="any":    
            rule = rule + '-A ufw-user-input -p tcp --dport {0} -j ACCEPT\n-A ufw-user-input -p udp --dport {0} -j ACCEPT\n'.format(port)
        else:
        	rule = rule + '-A ufw-user-input -p {} --dport {} -j ACCEPT\n'.format(protocol, port)

# Allow ip(with prefix)
    elif(selection==2):
    	print("Give IP address or if you want to specify subnet add prefix after IP/24 etc.")
    	ip=raw_input("What is the ip: ")
    	rule = '\n### tuple ### allow any any 0.0.0.0/0 any {} in\n'.format(ip)
    	rule = rule + '-A ufw-user-input -s {} -j ACCEPT\n'.format(ip)

# Exit    
    elif(selection==3):
    	break

# Append rule after rules line
    with open(USER_RULES, "r") as in_file:
    	buf = in_file.readlines()

	with open(USER_RULES, "w") as out_file:
	    for line in buf:
	        if line == "### RULES ###\n":
	            line = line + rule
	        out_file.write(line)
