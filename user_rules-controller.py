# USER_RULES = "/etc/ufw/user.rules"

USER_RULES = "deneme"

# List updated rules
def list_rules():
    print('{0:10}{1:^10}{2:^20}{3:10}'.format("PORT", "PROTOCOL", "IP", "ACTION"))
    with open(USER_RULES) as f:
        data = f.read()
    for line in data.split("\n"):
        if "tuple" in line:
            rule = line[14:].split()
            print('{0:10}{1:^10}{2:^20}{3:10}'.format(rule[2], rule[1], rule[5], rule[0]))
    print("1. Port Allow\n2. IP allow/drop/deny\n0. Exit")

# Add rules unless user exists
selection = -1
while (True):
	list_rules()
	selection=int(input("What is your choice: "))
	rule = ""

# Port(single)
	if(selection==1):
		port=int(input("Which port: "))
		protocol=raw_input("Which protocol: ")
		rule = '\n### tuple ### allow {} {} 0.0.0.0/0 any 0.0.0.0/0 in\n'.format(protocol, port)
		if protocol=="any":
			rule = rule + '-A ufw-user-input -p tcp --dport {0} -j ACCEPT\n-A ufw-user-input -p udp --dport {0} -j ACCEPT\n'.format(port)
		else:
			rule = rule + '-A ufw-user-input -p {} --dport {} -j ACCEPT\n'.format(protocol, port)

# Allow ip(with prefix)
	elif(selection==2):
		print("Give IP address or if you want to specify subnet add prefix after IP/24 etc.")
		ip=raw_input("What is the ip: ")
		acts = ("allow", "deny", "reject")
		verbs = ("ACCEPT", "DROP", "REJECT")
		ch=4
		while(ch>3 or ch<1):
			ch=int(raw_input("Which action(allow=1, deny=2, reject=3):"))
		act=acts[ch-1]
		verb=verbs[ch-1]
	    

		rule = '\n### tuple ### {} any any 0.0.0.0/0 any {} in\n'.format(act, ip)
		rule = rule + '-A ufw-user-input -s {} -j {}\n'.format(ip, verb)

# Exit    
	elif(selection==0):
		break

# Writing rule
	with open(USER_RULES, "r") as in_file:
		buf = in_file.readlines()

	with open(USER_RULES, "w") as out_file:

	# if it is a port rule then add it at the bottom
		if selection == 1:
			print("rule")
			for i in range(len(buf)):
				if i!=len(buf)-1 and buf[i+1] == "### END RULES ###\n":
					buf[i] = buf[i] + rule
				out_file.write(buf[i])

	# if it is an ip rule then add it at the top    
		if selection == 2:
			print("failip")
			for i in range(len(buf)):
				if buf[i] == "### RULES ###\n":
					buf[i] = buf[i] + rule
				out_file.write(buf[i])