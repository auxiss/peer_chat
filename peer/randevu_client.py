import requests
import sseclient


def subscribe(server_url,your_public_key, your_ip, your_port):
    
    data = {"action": "subscribe", "public_key": your_public_key, "peer_ip": your_ip, "peer_port": your_port}

    try:
        response = requests.post(server_url, json=data, timeout=1)  # send JSON payload
        if response.status_code != 200:
            print("Status code:", response.status_code)
            print("Error:", response.text)
            return None

        if response.headers.get('Content-Type') != 'application/json':
            print("Error: Response is not in JSON format")
            return None
        
        #print("Response:", response.json())
        #print(f"subscribed {server_url} as {your_public_key} at {your_ip}:{your_port}")
        return response.json()
    except Exception as e:
        print("Failed to connect to the server. Exception:", str(e))
        return None



def connect_to_peer(server_url, your_public_key, target_key):
    
    data = {"action": "connect_to_peer", "public_key": your_public_key, "target_key": target_key}

    try:
        response = requests.post(server_url, json=data, timeout=1)  # send JSON payload
        #print("raw response:", response.text)
        #print("status code:", response.status_code)
    except:
        print("Failed to connect to the server.")
        return None
    
        
    if response.status_code == 404:
        #print("peer not found")
        return {'message': 'peer not found'}
    elif response.status_code != 200:
        print("Status code:", response.status_code)
        print("Error:", response.text)    
        return None
    #check for json response
    if response.headers.get('Content-Type') != 'application/json':
        print("Error: Response is not in JSON format")
        return None
    
    #print("Response:", response.json())  # assuming Flask returns JSON
    #print(f"peer {target_key} found")
    return response.json()



def get_freind_requests_from_sse(server_url, your_public_key):
    sse_url = f"{server_url.replace('/meet', '')}/events/{your_public_key}"
    try:
        response = requests.get(sse_url, stream=True)
        print(f'raw response from {sse_url}:', response)
        print("Response headers:", response.headers)
        # Check Content-Type
        if response.headers.get("Content-Type") != "text/event-stream":
            print("Error: Server did not return text/event-stream")
            return
        '''print("Connected to SSE endpoint.")
        client = sseclient.SSEClient(response)
        print(f"Listening for notifications at {sse_url}...")
        for event in client.events():
            print("Notification:", event.data)'''
    except Exception as e:
        print("Failed to connect to SSE endpoint:", str(e))

   
    
    


if __name__ == "__main__":
    your_public_key = "your_unique_public_key"
    
    url = "http://127.0.0.1:5000/meet"  # endpoint on your Flask server