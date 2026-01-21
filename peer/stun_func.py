import stun




def get_external_info(stun_list):
    # Get external IP and port using STUN servers        

    external_ip = None
    external_port = None

    for stun_ip, stun_port in stun_list:
        try:
            nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_ip, stun_port=stun_port)

            '''print(f'Successfully connected to STUN server {stun_ip}:{stun_port}')
            print(f'Your public IP: {external_ip}')
            print(f'Your public port: {external_port}')
            print(f'Your NAT type: {nat_type}')'''

            external_ip = external_ip
            external_port = external_port

            external_info = {"ip": external_ip, 
                                "port": external_port, 
                                "nat_type": nat_type}

            return external_info

        except Exception as e:
            #print(f'Failed to connect to STUN server {stun_ip}:{stun_port} - {e}')
            return 1

    if external_ip is None or external_port is None:
        raise Exception("Failed to retrieve external IP and port from all STUN servers.")