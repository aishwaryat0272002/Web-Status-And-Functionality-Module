import socket
def get_public_ip():
	try:
		ip_address = socket.gethostbyname('api.ocp.nic.in')
		print(ip_address)
	except:
		print("Non-Existent Domain")



print(get_public_ip())
	
	
	