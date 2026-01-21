import pickle
import hashlib
import uuid
from typing import Any, List, Dict


def packetize_object(
    obj: Any,
    max_chunk_size: int = 1024
) -> List[Dict]:
    """
    Convert a Python object into a list of packets:
    [INIT, DATA_0, DATA_1, ..., DATA_N]
    """

    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be positive")

    session_id = uuid.uuid4().int

    # Serialize object
    serialized_data = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
    total_size = len(serialized_data)

    # Split into chunks
    chunks = [
        serialized_data[i:i + max_chunk_size]
        for i in range(0, total_size, max_chunk_size)
    ]

    total_chunks = len(chunks)

    # Init packet
    packets = [{
        "packet_type": "INIT",
        "session_id": session_id,
        "object_type": type(obj).__name__,
        "total_size": total_size,
        "chunk_size": max_chunk_size,
        "total_chunks": total_chunks,
    }]

    # Data packets
    for chunk_id, chunk in enumerate(chunks):
        packets.append({
            "packet_type": "DATA",
            "session_id": session_id,
            "chunk_id": chunk_id,
            "payload_size": len(chunk),
            "payload": chunk,
            "hash": hashlib.sha256(chunk).hexdigest(),
        })

    return packets



if __name__ == "__main__":


    data = ['awdawdaw','awdawdawdawd','awdawdawdawd']

    packet_list = packetize_object(data,8)


    for packet in packet_list:
        print(packet)