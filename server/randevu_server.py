from flask import Flask, request, jsonify, Response
import queue


app = Flask(__name__)

peers = []
notifications = {}  # public_key -> Queue

@app.route("/events/<public_key>")               #not working yet
def sse(public_key):
    def event_stream():
        q = notifications.setdefault(public_key, queue.Queue())
        while True:
            msg = q.get()
            yield f"data: {msg}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/meet", methods=["POST"])
def receive():
    data = request.get_json()
    print("Received data:", data)


    if data['action'] == 'subscribe':
        print("Subscribing peer...")

        peer_key = data['public_key']
        peer_ip = data['peer_ip']
        peer_port = data['peer_port']

        print("-- key:", peer_key)
        print("-- ip:", peer_ip)  
        print("-- port:", peer_port)      


        if peer_key in peers: #update if already exists
            for p in peers:
                if p['public_key'] == peer_key:
                    p['ip'] = peer_ip
                    p['port'] = peer_port

            print("Peer updated:", p)
            return jsonify({"message": "updated successfully", "your_data": p}), 200


        else: #add new peer
            peer = {
                "public_key": peer_key,
                "ip": peer_ip,
                "port": peer_port
            }
            peers.append(peer)

            print("New peer added:", peer)
            return jsonify({"message": "subscribed successfully", "your_data": peer}), 200



    if data['action'] == 'connect_to_peer':
        target_key = data['target_key']
        peer_key = data['public_key']
        

        for peer in peers:
            if peer['public_key'] == target_key:
                target_ip = peer['ip']
                target_port = peer['port']

                target_peer = {
                    "public_key": target_key,
                    "ip": target_ip,
                    "port": target_port
                }

                for p in peers: #finde source peer inforamasion to send to target peer
                    if p['public_key'] == peer_key:
                        peer_ip = p['ip']
                        peer_port = p['port']
                        break

                # Notify target peer via SSE                                  #not tested yet
                msg = f"Peer {peer_key} is trying to connect to you. from address {peer_ip}:{peer_port}"
                notifications.setdefault(target_key, queue.Queue()).put(msg)
                

                print("Target peer found:", target_peer)
                return jsonify({"message": "Peer found", "target_info": target_peer}), 200
        
        return jsonify({"error": "Peer not found"}), 404



    return jsonify({"error": "Invalid action"}), 400


    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)


