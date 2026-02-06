from bambulab import BambuAuthenticator, BambuClient
import json

print("Loading Bambu token from default location (~/.bambu_token)")

auth = BambuAuthenticator()
token = auth.get_or_create_token()

print("Token loaded successfully")

client = BambuClient(token=token)
devices = client.get_devices()

print(f"Found {len(devices)} device(s):\n")

for i, d in enumerate(devices):
    print(f"Device {i} raw data:")
    print(json.dumps(d, indent=2))
    print("-" * 40)
