import randevu_client
import peer_core
import time
import threading
import rsa_enryption





class p2peer:
    def __init__(self, stun_list, randevu_server_list):
        self.stun_list = stun_list
        self.randevu_server_list = randevu_server_list
        self.active_randevu_servers = []
        self.peer = peer_core.Peer(stun_list)
        self.running = False
    
        info = self.peer.get_info()
        my_external_ip = info['ip']
        my_external_port = info['port']
        my_nut_type = info['nat_type']


        for url in self.randevu_server_list:
            print(f'Atemping to subscribe to randevu server at {url}...')
            sub_res = randevu_client.subscribe(url, your_public_key, my_external_ip, my_external_port)
            if sub_res is not None:
                print(f"-- Subscription to {url} was successful:\n--    {sub_res}\n")
                self.active_randevu_servers.append(url)
            else:
                print(f"-- Subscription to {url} failed.")

        if sub_res is None:
            print("No randevu servers avelable! Exiting.")
            exit(0)
        else:
            print(f"Active randevu servers:")
            for url in self.active_randevu_servers:
                print(f"- {url}")
            print()


    def close(self):
        if self.running:
            self.running = False
            self.peer.stop()
            self.connection_thread.join()

    def status(self):
        return self.peer.peer_status()
    
    def info(self):
        return self.peer.get_info()
    
    def send_message(self, message):
        self.peer.send_message(message)

    def recive_message(self):
        return self.peer.recive_message()
    
    def start(self, your_public_key, target_public_key):
        self.running = True
        

        def connect(your_public_key, target_public_key):
                while self.running:
                    for url in self.active_randevu_servers:
                    
                        print(f"Attempting to connect to server ({url}) for peer ({target_public_key}) info...")
                        con_res = randevu_client.connect_to_peer(url, your_public_key, target_public_key)
                        if con_res is not None:

                            #print("Connection response:", con_res)
                            if 'message' in con_res and con_res['message'] == 'peer not found':
                                print("-- Peer not found.")
                                


                            elif 'message' in con_res and con_res['message'] == 'Peer found':

                                target_info = con_res['target_info']
                                peer_ip = target_info['ip']
                                peer_port = target_info['port']
                                peer_key = target_info['public_key']

                                print(f"-- Peer {peer_key} found at: {peer_ip}:{peer_port}")
                                print("-- Attempting to connect to peer...\n")
                                self.peer.start(peer_ip, peer_port)
                                break


                        else:
                            print("Connection failed.")

                    time.sleep(60)


        #print("Starting connection thread...")
        self.connection_thread = threading.Thread(target=connect, args=(your_public_key, target_public_key), daemon=True)
        self.connection_thread.start()
        #print("Connection thread started.")
    
            










if __name__ == "__main__":
    import settings_loader


    print('''
       ____ ____  ____        ____ _           _        
      |  _ \___ \|  _ \      / ___| |__   __ _| |_      
 _____| |_) |__) | |_) |____| |   | '_ \ / _` | __|____ 
|_____|  __// __/|  __/_____| |___| | | | (_| | ||_____|
      |_|  |_____|_|         \____|_| |_|\__,_|\__|   _ 
                                        __   __/ _ \ / |
                            by auxiss   \ \ / / | | || |
                                         \ V /| |_| || |
                                          \_/  \___(_)_|
''')

    settings = settings_loader.load_settings()
    your_public_key = settings["public_key"]
    print("Your public key:")
    print(your_public_key)

    
    

    stun_list = settings["stun_list"]
    randevu_server_list = settings["randevu_servers"]

    peers = settings["known_peers"]

    p2p = p2peer(stun_list, randevu_server_list)
    

    while True:
        try:
            stdinput_text = input("-$ ")
            
            if stdinput_text.lower() == "exit":
                p2p.close()
                break
            elif stdinput_text.lower() == "status":
                print(p2p.status())
            elif stdinput_text.lower() == "info":
                print(p2p.info())
            elif stdinput_text.lower().startswith("send "):
                message = stdinput_text[5:]
                p2p.send_message(message)

            elif stdinput_text.lower() == "recive":
                message = p2p.recive_message()
                if message is None:
                    print("No new messages.")
                else:
                    print("Recived message:", message)

            elif stdinput_text.lower() == "connect":
                target_public_key = input("Enter target peer's public key: ")
                p2p.start(your_public_key, target_public_key)

            elif stdinput_text.lower() == "getfriendreq":
                randevu_client.get_freind_requests_from_sse(randevu_server_list[1], your_public_key)  #not tested yet

            elif stdinput_text.lower() == "getpeers":
                for url in p2p.active_randevu_servers:
                    print(f"Getting peer list from {url}...")
                    peer_list = randevu_client.get_all_peers(url)
                    if peer_list is not None and 'peers' in peer_list:
                        print("Peer list:")
                        for peer in peer_list['peers']:
                            print(f"- {peer}")
                    else:
                        print("Failed to get peer list or no peers available.")
                print()

            elif stdinput_text.strip() == "":
                continue
                
            else:
                print("Unknown command. Available commands: getfriendreq, connect, send <message>, recive, status, info, getpeers, exit")

        except KeyboardInterrupt:
            print("Exiting...")
            p2p.close()
            break





    