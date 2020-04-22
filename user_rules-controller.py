USER_RULES = "/etc/ufw/user.rules"



# List updated rules
def get_rule_index():
	print('{:<7}|{:^10}|{:^10}|{:^20}|{:>10}'.format("Numbers", "PORT", "PROTOCOL", "IP", "ACTION"))
	with open(USER_RULES, "r") as in_file:
		data = in_file.readlines()
	rule_list=[]
	k = 0
	for i in range(len(data)):
		if "tuple" in data[i]:
			rule = data[i][14:].split()
			print('{:^7}|{:^10}|{:^10}|{:^20}|{:>10}'.format(k+1,rule[2], rule[1], rule[5], rule[0]))
			k+=1
			rule_list.append(i)


	print("\n1. Port Allow\n2. IP Permissions\n3. IP-Port Permissions\n4. Delete Rule\n5. Edit Rule\n0. Exit")
	return rule_list


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
	ch=raw_input("Which action(allow, deny, reject): ")
	return ip,action

### Get selected index
def get_index(rule_list):
	selected_rule=0
	while selected_rule<1 or selected_rule>len(rule_list):
			selected_rule=int(raw_input("What is rule number: "))
	selected_rule-=1
	return selected_rule


# Hints about rules
print("\n" + "*"*25 + "HINTS" + "*"*25)
print("- You can add prefix after network address such as IP/24\n- Ports can be single or multi such as 22, 7100:7200\n Second and third options are prior!\n")
print("*"*55 + "\n")

# Add rules unless user exists LOOP
while (True):
	rule_list = get_rule_index()

# Initial variables
	choice = -1
	selected_rule = -1
	newrule = ""
	port = "any"
	protocol = "any"
	ip = "0.0.0.0/0"
	action = "allow"

	while choice<0 or choice>5:
		choice=int(raw_input("What is your choice: "))

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

# Deleting rule
	elif choice==4:
		selected_rule = get_index(rule_list)

# Editing rule
	else:
		selected_rule = get_index(rule_list)
		print('Just press "Enter" if you don\'t want to change that field.')
		ip, action = get_ip()
		port, protocol = get_port()
		rule = rule_list[selected_rule][14:].split()
		if len(ip) == 0:
			ip == rule[5]
		if len(action) == 0:
			action == rule[0]
		if len(port) == 0:
			port == rule[2]
		if len(protocol) == 0:
			protocol == rule[1]

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
		elif choice==2 or choice==3:
			for i in range(len(buf)):
				if buf[i] == "### RULES ###\n":
					buf[i] = buf[i] + newrule
				out_file.write(buf[i])

	# deleting specific line
		elif choice==4:
			for i in range(len(buf)):
				if i!= rule_list[selected_rule]:
					out_file.write(buf[i])

	# editing rule
		else:
			for i in range(len(buf)):
				if i==rule_list[selected_rule]:
					out_file.write(buf[i])
					break
				out_file.write(buf[i])


