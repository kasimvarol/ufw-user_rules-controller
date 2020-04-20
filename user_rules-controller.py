USER_RULES = "/etc/ufw/user.rules"

# List updated rules
def list_rules():
	print('{0:10}{1:^10}{2:^20}{3:10}'.format("PORT", "PROTOCOL", "IP", "ACTION"))
	with open(USER_RULES, "r") as in_file:
		data = in_file.readlines()
	for line in data:
		if "tuple" in line:
			rule = line[14:].split()
			print('{0:10}{1:^10}{2:^20}{3:10}'.format(rule[2], rule[1], rule[5], rule[0]))
	print("\n1. Port Allow\n2. IP Permissions\n3. IP-Port Permissions\n0. Exit")


### Check the value with regex (22, 7100, 7100:7200) NEED TO BE REVISED
def get_port():
	port = raw_input("Which port(s): ")
	if(":" in port):
		protocol = raw_input("Which protocol(tcp,udp): ")
	else:
		protocol = raw_input("Which protocol(any,tcp,udp): ")
	return port,protocol

### Check the value with regex (10.10.10.0/24 or 10.10.10.10) NEED TO BE REVISED
def get_ip():
	ip = raw_input("Network address: ")
	acts = ("allow", "deny", "reject")
	ch=4
	while(ch>3 or ch<1):
		ch=int(raw_input("Which action(allow=1, deny=2, reject=3):"))
	action=acts[ch-1]
	return ip,action




# Hints about rules
print("\n" + "*"*25 + "HINTS" + "*"*25)
print("- You can add prefix after network address such as IP/24\n- Ports can be single or multi such as 22, 7100:7200\n Second and third options are prior!\n")
print("*"*55 + "\n")

# Add rules unless user exists LOOP
while (True):
	list_rules()

# Initial variables
	choice = -1
	newrule = ""
	port = "any"
	protocol = "any"
	ip = "0.0.0.0/0"
	action = "allow"

	while choice<0 or choice>3:
		choice=int(input("What is your choice: "))

#Exit
	if choice==0:
		break

# Port(s) Allowing
	if choice==1:
		port, protocol = get_port()

# IP Permissions
	elif choice==2:
		ip, action = get_ip()

# IP-Port Permissions
	elif choice==3:
		ip, action = get_ip()
		port, protocol = get_port()

# Writing rule
	newrule = '\n### tuple ### {} {} {} 0.0.0.0/0 any {} in\n'.format(action, protocol, port, ip)
	with open(USER_RULES, "r") as in_file:
		buf = in_file.readlines()

	with open(USER_RULES, "w") as out_file:

	# if it is a port rule then add it at the bottom
		if choice == 1:
			for i in range(len(buf)):
				if i!=len(buf)-1 and buf[i+1] == "### END RULES ###\n":
					buf[i] = buf[i] + newrule
				out_file.write(buf[i])

	# if it is an ip rule then add it at the top    
		else:
			for i in range(len(buf)):
				if buf[i] == "### RULES ###\n":
					buf[i] = buf[i] + newrule
				out_file.write(buf[i])