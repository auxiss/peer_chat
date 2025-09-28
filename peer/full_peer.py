import randevu_client
import stun_peer


if __name__ == "__main__":
    your_public_key = "oddy"
    target_public_key = "gim"


    your_public_key = input("Enter your public key: ")
    target_public_key = input("Enter target peer's public key: ")

    
    
    url = "http://217.69.14.234:5000/meet" #randevu server url


    stun_list = [
    ("stun.l.google.com", 19302),
    ("stun.nextcloud.com", 443)
    ]


    peer = stun_peer.Peer(stun_list)
    
    info = peer.get_info()
    my_external_ip = info['ip']
    my_external_port = info['port']
    my_nut_type = info['nat_type']

    print(f'Atemping to subscribe to randevu server at {url}...')
    sub_res = randevu_client.subscribe(url, your_public_key, my_external_ip, my_external_port)
    if sub_res is not None:
        print(f"Subscription to {url} was successful:\n--- {sub_res}\n")
    else:
        print("Subscription failed.")



    print(f"Attempting to connect to server ({url}) for peer ({target_public_key}) info...")
    con_res = randevu_client.connect_to_peer(url, your_public_key, target_public_key)
    if con_res is not None:
        #print("Connection response:", con_res)
        if 'message' in con_res and con_res['message'] == 'peer not found':
            print("Peer not found.")
        elif 'message' in con_res and con_res['message'] == 'Peer found':
            target_info = con_res['target_info']
            peer_ip = target_info['ip']
            peer_port = target_info['port']
            peer_key = target_info['public_key']

            print(f"Peer {peer_key} found at: {peer_ip}:{peer_port}")
            print("Attempting to connect...")
            peer.start(peer_ip, peer_port)
    else:
        print("Connection failed.")



    

    