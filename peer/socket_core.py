import socket
import threading
import time 



#not tested


class P2Psocket:
    def __init__(self, peer_ip, peer_port, external_ip, external_port):

        self.peer_ip = peer_ip
        self.peer_port = peer_port

        self.external_ip = external_ip
        self.external_port = external_port

        your_ip = "" #we can only open ports on this machine not the one with the external ip (the router)
        your_port = self.external_port

        self.last_seen_time = None
        self.peer_sate = "Disconnected"

        self.send_queue = []
        self.receive_queue = []

        self.running = True  


        print("Starting UDP hole punching...")
        print(f"-from address: {self.external_ip}:{self.external_port}")
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
                self.peer_sate = "Connected"
                if data.decode() == "KEEPALAIVE":
                    #print(f"keepalive from {addr}")
                    pass
                else:
                    print(f"message from {addr}: {data.decode()}")
                    self.receive_queue.append(data.decode())

        #send message packet
        def send_message():
            while self.running:
                if not self.send_queue:
                    time.sleep(0.1)
                    continue
                else:
                    if self.peer_sate == "Connected":
                        message = self.send_queue.pop(0)

                        sock.sendto(message.encode(), (self.peer_ip, self.peer_port))
                        print(f"Sent message to {self.peer_ip}:{self.peer_port}")




        threading.Thread(target=send_punch_packets, daemon=True).start()
        threading.Thread(target=receive_messages, daemon=True).start()
        threading.Thread(target=send_message, daemon=True).start()



        #check connection
        while self.running:
            try:
                time.sleep(5)
                if self.last_seen_time is not None:
                    time_since_last_seen = time.time() - self.last_seen_time

                    if time_since_last_seen > 2:
                        self.peer_sate = "Disconnected"
                    else:
                        self.peer_sate = "Connected"
                else:
                    self.peer_sate = "Disconnected"

            except KeyboardInterrupt:
                print("Exiting...")
                self.running = False
                break

        sock.close()
        print("Socket closed.")
        return 0


    def stop(self):
        if not self.running:
            print("Peer is not running.")
        else:
            print("Exiting...")
            self.running = False
        

    def peer_status(self):

        if self.last_seen_time is not None:
            time_since_last_seen = time.time() - self.last_seen_time
            if time_since_last_seen > 2:
                self.peer_sate = "Disconnected"
            else:
                self.peer_sate = "Connected"
        else:
            self.peer_sate = "Disconnected"

        status = {
            "running": self.running,
            "peer_ip": self.peer_ip if hasattr(self, 'peer_ip') else None,
            "peer_port": self.peer_port if hasattr(self, 'peer_port') else None,
            "satate": self.peer_sate,
            "last_seen": self.last_seen_time,
            "send_queue_length": len(self.send_queue),
            "receive_queue_length": len(self.receive_queue)
            }
        
        return status
    

    def send_message(self, message):
        self.send_queue.append(message)

    def recive_message(self):
        if not self.receive_queue:
            return None
        else:
            return self.receive_queue.pop(0)



if __name__ == "__main__":
    import stun_func
    import settings_loader

    settings = settings_loader.load_settings()

    stun_list = settings['stun_list']
    print(stun_list)

    info = stun_func.get_external_info(stun_list)
    print(info)



    peer_pi = ''
    peer_port = ''

    if peer_pi == '':
        exit()

    socket_1 = P2Psocket(peer_pi, peer_port, info['ip'], info['port'])