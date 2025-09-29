import socket
import threading
import time 
import stun



class Peer:
    def __init__(self, stun_list):
        self.stun_list = stun_list
        self.last_seen_time = None



        # Get external IP and port using STUN servers        
        self.external_ip = None
        self.external_port = None

        self.external_info = None

        for stun_ip, stun_port in self.stun_list:
            try:
                nat_type, external_ip, external_port = stun.get_ip_info(stun_host=stun_ip, stun_port=stun_port)

                '''print(f'Successfully connected to STUN server {stun_ip}:{stun_port}')
                print(f'Your public IP: {external_ip}')
                print(f'Your public port: {external_port}')
                print(f'Your NAT type: {nat_type}')'''

                self.external_ip = external_ip
                self.external_port = external_port

                self.external_info = {"ip": self.external_ip, 
                                 "port": self.external_port, 
                                 "nat_type": nat_type}

                break

            except Exception as e:
                print(f'Failed to connect to STUN server {stun_ip}:{stun_port} - {e}')

        if self.external_ip is None or self.external_port is None:
            raise Exception("Failed to retrieve external IP and port from all STUN servers.")
        



    def get_info(self):
        return self.external_info
    
    def peer_status(self):

        if self.last_seen_time is not None:
            time_since_last_seen = time.time() - self.last_seen_time
            if time_since_last_seen > 10:
                peer_sate = "Disconnected"
            else:
                peer_sate = "Connected"
        else:
            peer_sate = "Disconnected"

        status = {
            "peer_ip": self.peer_ip if hasattr(self, 'peer_ip') else None,
            "peer_port": self.peer_port if hasattr(self, 'peer_port') else None,
            "satate": peer_sate,
            "last_seen": self.last_seen_time
            }



    def start(self, peer_ip, peer_port):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.running = True
        your_ip = ""
        your_port = self.external_port

        print("Starting UDP hole punching...")
        print(f"-my address: {self.external_ip}:{self.external_port}")
        print(f"-peer address: {peer_ip}:{peer_port}")

        #CREATE A UDP SOCKET
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.bind((your_ip, your_port))
        print(f"-My local address: {sock.getsockname()}")



        # send punch pakcets to other peer 
        def send_punch_packets():
            while self.running:
                sock.sendto(b"KEEPALAIVE", (peer_ip , peer_port))
                #print(f"Sent punch to {peer_ip}:{peer_port}")
                time.sleep(1)

        # LISTEN FOR MESSAGES
        def receive_messages():
            while self.running:
                try:
                    data, addr = sock.recvfrom(1024) 
                except:
                    continue

                self.last_seen_time = time.time()
                if data.decode() == "KEEPALAIVE":
                    #print(f"keepalive from {addr}")
                    pass
                else:
                    print(f"message from {addr}: {data.decode()}")

        #send message packet
        def send_message():
            while self.running:
                message = input()
                sock.sendto(message.encode(), (self.peer_ip, self.peer_port))
                #print(f"Sent message to {self.peer_ip}:{self.peer_port}")




        threading.Thread(target=send_punch_packets, daemon=True).start()
        threading.Thread(target=receive_messages, daemon=True).start()
        threading.Thread(target=send_message, daemon=True).start()



        #keep the main thread alive
        while True:
            try:
                time.sleep(1)

            except KeyboardInterrupt:
                print("Exiting...")
                self.running = False
                break

        sock.close()



if __name__ == "__main__":
    stun_list = [
    ("stun.l.google.com", 19302),
    ("stun.nextcloud.com", 443)
    ]



    peer_ip = "31.152.245.203"
    peer_port = 2736

    peer = Peer(stun_list)
    print("Your external info:", peer.get_info())
    peer.start(peer_ip, peer_port)




