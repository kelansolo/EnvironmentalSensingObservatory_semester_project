from sys import argv
import gps
import requests

print("run")

# Listen on port 2947 of gpsd
session = gps.gps("tcp://localhost", "2947")
print("stuck")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

print("run")
while True:
    print("TRUE")
    try:
        print("test")
        # Get the next GPS data update
        rep = session.next()

        # Only process TPV (Time-Position-Velocity) data
        if rep["class"] == "TPV":
            # Print the latitude and longitude values
            print(f"{rep.lat},{rep.lon}")

    except KeyError as e:
        print(f"KeyError: Missing expected data - {e}")
    except gps.GPSException as e:
        print(f"GPS Exception: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
