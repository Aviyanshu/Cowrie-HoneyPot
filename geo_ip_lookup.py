import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def GeoIPLookup(ip_address):
    import geoip2.database

    # Path to the GeoLite2 database
    database_path = './GeoLite2-City_20260320/GeoLite2-City.mmdb'

    try:
        # Create a GeoIP reader
        reader = geoip2.database.Reader(database_path)

        # Perform the lookup
        response = reader.city(ip_address)

        # Extract relevant information
        result = {
            "ip_address": ip_address,
            "country": response.country.name,
            "city": response.city.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude
        }

        # Return the result as a dictionary
        return result

    except Exception as e:
        log.error(f"Error performing GeoIP lookup for {ip_address}: {e}")