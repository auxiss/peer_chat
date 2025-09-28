#!venv/bin/python3
from scapy.all import *



class UDP_Pucher:
    def __init__(self, my_adder, friend_adder):
        my_ip, my_port = my_adder
        friend_ip, friend_port = friend_adder
        self.my_ip = my_ip
        self.my_port = my_port
        self.friend_ip = friend_ip
        self.friend_port = friend_port

        self.running = True


    
    def listener(self):
        def packet_handler(pkt):
            if pkt.haslayer(UDP):
                if pkt[IP].dst == self.my_ip and pkt[UDP].dport == self.my_port:

                    print(pkt.summary())
                    #print(f"Received packet from {pkt[IP].src}:{pkt[UDP].sport} , data: {pkt[Raw].load.decode()}")
                    self.running = False

        while self.running:

            sniff(iface='lo', filter='udp', prn=packet_handler, count=1, store=0)
            
    
    def start(self):
        # Create a UDP packet
        pkt = IP(dst=self.friend_ip) / UDP(dport=self.friend_port) / Raw(load="start")
        
        # Send the packet
        send(pkt)

        self.listener()
        
        
if __name__ == "__main__":
    my_adder = '0.0.0.0', 12346
    friend_adder = '31.152.137.132', 2256
    udp_pucher = UDP_Pucher(my_adder, friend_adder)
    udp_pucher.start()