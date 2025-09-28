from flask import Flask, request, jsonify



app = Flask(__name__)

peers = []


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

        for peer in peers:
            if peer['public_key'] == target_key:
                target_ip = peer['ip']
                target_port = peer['port']

                target_peer = {
                    "public_key": target_key,
                    "ip": target_ip,
                    "port": target_port
                }

                print("Target peer found:", target_peer)
                return jsonify({"message": "Peer found", "target_info": target_peer}), 200
        
        return jsonify({"error": "Peer not found"}), 404



    return jsonify({"error": "Invalid action"}), 400


    

if __name__ == "__main__":
    app.run(debug=True, port=5000)


