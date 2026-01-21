from typing import Any, List, Dict
import packetizer


class session_manager:
    def __init__(self):
        self.RX_sessoins = []
        self.TX_sessions = []

    def send_obj(self, obj: Any):
        #start a new TX_session
        pass
    
    def enterpret_pkt(self, pkt: dict):
        #hire we check if the pa
        packet_type = pkt['packet_type']
        session_id = pkt['session_id']

        if packet_type == 'INIT':
            #start RX_session
            pass

        elif packet_type == 'IACC':
            for TX_session in self.TX_sessions:
                if TX_session.get_id() == session_id:
                    TX_session.start_data_phase()
                    return 0
            return 0

        elif packet_type == 'DATA':
            for TX_session in self.TX_sessions:
                if TX_session.get_id() == session_id:
                    TX_session.start_data_phase()
                    return 0
            return 0




            



        




class TX_session:
    def __init__(self, obj: Any):
        packet_list = packetizer.packetize_object(obj)
        self.session_id = packet_list[0]['session_id']

        #send the fist init packet at index 0

    def get_id(self):
        return self.session_id
    
    def start_data_phase(self):
        pass
    def resend_chunks(self,chunk_id_list):
        pass
    def stop_data_phase(self):
        #when recipient confirms that all chunks have ben recivd corectly 
        pass

    



class RX_session:
    def __init__(self, pkt: dict):
        if pkt['packet_type'] != 'INIT': raise ValueError
        self.session_id = pkt['session_id']
        self.object_type = pkt['object_type']
        self.total_size = pkt['total_size']
        self.chunk_size = pkt['chunk_size']
        self.total_chunks = pkt['total_chunks']

        self.chunks = []
        self.missing_chunks = []
        for i in range(0,self.total_chunks):
            self.missing_chunks.append(str(i))

    def get_id(self):
        return self.session_id
    
    def add_chunk(self, pkt: dict):
        chunk_id = pkt['chunk_id']
    




if __name__ == "__main__":

    text= input()
    test_bytes = text.encode()




    TX_session(test_bytes)