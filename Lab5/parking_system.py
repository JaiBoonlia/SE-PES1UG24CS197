"""Manage campus parking permits and validate parking zones."""

import json
import secrets
from datetime import datetime, timedelta

# Global state
permits = {}
ZONES = ["A", "B", "C"]


def register_permit(vehicle_plate, zone_id, zone_records=None):
    """Register a vehicle and return its permit number."""
    if not isinstance(vehicle_plate, str) or not vehicle_plate.strip():
        raise ValueError("Vehicle plate must be a non-empty string.")
    if zone_id not in ZONES:
        raise ValueError("Invalid parking zone.")

    if zone_records is None:
        zone_records = []

    permit_no = f"P{secrets.randbelow(90000) + 10000}"
    expiry = datetime.now() + timedelta(days=180)

    permits[vehicle_plate] = {
        "zone": zone_id,
        "permit": permit_no,
        "expiry": expiry.strftime("%Y-%m-%d"),
    }
    zone_records.append((vehicle_plate, zone_id))
    return permit_no


def revoke_permit(vehicle_plate):
    """Revoke a vehicle's permit if it exists."""
    return permits.pop(vehicle_plate, None) is not None


def is_expired(vehicle_plate):
    """Return whether a vehicle's permit has expired."""
    permit = permits.get(vehicle_plate)
    if permit is None:
        return False

    try:
        expiry = datetime.strptime(permit["expiry"], "%Y-%m-%d")
    except (KeyError, TypeError, ValueError):
        return True

    return expiry.date() < datetime.now().date()


def scan_zone(zone_id, plates_seen):
    """Return plates that are not permitted in the specified zone."""
    flagged = []
    for plate in plates_seen:
        permit = permits.get(plate)
        if (
            permit is None
            or permit["zone"] != zone_id
            or is_expired(plate)
        ):
            flagged.append(plate)
    return flagged


def load_permit_database(file="permits.json"):
    """Load permit records from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as database:
            data = json.load(database)
        if not isinstance(data, dict):
            raise ValueError("Permit database must contain a JSON object.")
        return data
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, OSError, ValueError):
        return {}


def save_permit_database(file="permits.json"):
    """Save permit records to a JSON file."""
    with open(file, "w", encoding="utf-8") as database:
        json.dump(permits, database, indent=4)


def set_expiry(vehicle_plate, date_text):
    """Set a permit expiry date using YYYY-MM-DD format."""
    if vehicle_plate not in permits:
        raise KeyError("Vehicle does not have a registered permit.")

    expiry = datetime.strptime(date_text, "%Y-%m-%d")
    permits[vehicle_plate]["expiry"] = expiry.strftime("%Y-%m-%d")


def main():
    """Run the parking permit demonstration."""
    permits.update(load_permit_database())

    register_permit("KA01AB1234", "A")
    register_permit("KA05XY9999", "B")

    set_expiry("KA01AB1234", "2020-01-01")
    revoke_permit("MH12ZZ0000")

    print(
        "Flagged in zone A:",
        scan_zone("A", ["KA01AB1234", "KA05XY9999", "TN09QQ1111"]),
    )
    plate = input("Plate to revoke (Enter to skip): ").strip()
    if plate:
        revoke_permit(plate)

    save_permit_database()
    print("Permits on file:", len(permits))


if __name__ == "__main__":
    main()
