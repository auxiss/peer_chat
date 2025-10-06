# check for the existance of setteing.txt
import os
import json
import rsa_enryption

if not os.path.exists("settings.conf"):
    print("settings.txt not found! Createing settings.txt")
    # file is of jsaon type

    pem_private, pem_public = rsa_enryption.generate_rsa_keys()

    default_settings = {

        "public_key": pem_public.decode('utf-8'),

        "private_key": pem_private.decode('utf-8'),

        "known_peers": [],

        "randevu_servers": [
            "http://16.198.47.48:5000/meet",   #fake server dose not work intensionally.
            "http://217.69.14.234:5000/meet"   #real server should work.
            ],

        "stun_list": [
            ("stun.l.google.com", 19302),
            ("stun.nextcloud.com", 443),
            ]
        }
    with open("settings.conf", "w") as f:
        json.dump(default_settings, f, indent=4)
    print("settings.txt created! Edit the file to change settings.")



def load_settings():
    with open("settings.txt", "r") as f:
        settings = json.load(f)
    return settings

        