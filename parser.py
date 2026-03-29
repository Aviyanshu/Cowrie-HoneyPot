import json
import logging
import glob
from geo_ip_lookup import GeoIPLookup

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

files = glob.glob("cowrie/cowrie.json*")

def Parser():
    with open("data/cowrie.csv","w", encoding="utf-8") as log_data:

        for file in files:
            with open(file, "r") as f:
                events = f.readlines()
                for event in events:
                    event = event.strip()
                    if not event:
                        continue

                    try:
                        event = json.loads(event)

                        if event.get("eventid") == "cowrie.login.success":
                            log.info(f"""Successful Login; 
                                    Event Time: {event['timestamp']};
                                    Source IP: {event['src_ip']}; 
                                    Username: {event['username']}; 
                                    Password: {event['password']}; 
                                    """)
                            if event['src_ip'] != "127.0.0.1":
                                location = GeoIPLookup(event['src_ip'])
                                log_data.write(f"{event['timestamp']},{event['src_ip']},{event['username']},{event['password']},{location['country']},{location['latitude']},{location['longitude']}\n")  
                            
                    except json.JSONDecodeError:
                        log.error(f"Failed to parse event: {event}")
                        continue