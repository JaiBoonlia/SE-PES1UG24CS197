import math

MAX_ZONES = 1000          # sanity cap so huge numbers can't overflow the fare
MAX_INPUT_LENGTH = 100    # reject absurdly long inputs early

CONCESSION_DISCOUNTS = {
    "STANDARD": 1.00,
    "STUDENT": 0.50,
    "SENIOR": 0.35,
    "MILITARY": 0.20,
    "CHILD": 0.00,
}


def parse_transit_corridor(corridor_code):
    """Parse 'ORIG-DEST-ZONES' and return a route/fare string, or None if invalid."""
    if not isinstance(corridor_code, str):
        return None
    corridor_code = corridor_code.strip()
    if not corridor_code or len(corridor_code) > MAX_INPUT_LENGTH:
        return None

    parts = corridor_code.split('-')
    if len(parts) != 3:
        return None
    orig, dest, zones_str = (p.strip() for p in parts)
    if not orig or not dest or not zones_str:
        return None
    if not (orig.isalnum() and dest.isalnum()):
        return None

    # Only plain ASCII digits (no sign, no unicode digits, no '1_000')
    if not (zones_str.isascii() and zones_str.isdigit()):
        return None
    zones = int(zones_str)
    if zones > MAX_ZONES:
        return None

    base_fare = 2.50 + (zones * 0.75)
    return f"Route {orig.upper()}->{dest.upper()}: {zones} Zones, Fare ${base_fare:.2f}"


def lookup_concession_discount(category_name):
    """Return the fare multiplier for a concession category, or None if unknown."""
    if not isinstance(category_name, str):
        return None
    category = category_name.strip().upper()
    return CONCESSION_DISCOUNTS.get(category)


def compute_passenger_density(occupancy_ratio_str):
    """Parse 'PASSENGERS/KM' and return passengers per km (2 dp), or None if invalid."""
    if not isinstance(occupancy_ratio_str, str):
        return None
    occupancy_ratio_str = occupancy_ratio_str.strip()
    if not occupancy_ratio_str or len(occupancy_ratio_str) > MAX_INPUT_LENGTH:
        return None

    parts = occupancy_ratio_str.split('/')
    if len(parts) != 2:
        return None

    try:
        passengers = float(parts[0])
        km = float(parts[1])
    except (ValueError, OverflowError):
        return None

    # Reject nan / inf, negative passengers and non-positive distance
    if not (math.isfinite(passengers) and math.isfinite(km)):
        return None
    if passengers < 0 or km <= 0:
        return None

    density = passengers / km
    if not math.isfinite(density):     # e.g. 1e308 / 1e-308 overflows to inf
        return None
    return round(density, 2)


def main():
    print("==== Running parse_transit_corridor ====")
    c_input = input("Enter corridor (e.g. DT-UP-3): ")
    result = parse_transit_corridor(c_input)
    print(result if result is not None else "Invalid corridor code. Expected format ORIG-DEST-ZONES, e.g. DT-UP-3")

    print("\n==== Running lookup_concession_discount ====")
    cat_input = input("Enter concession category (e.g. STUDENT, SENIOR): ")
    multiplier = lookup_concession_discount(cat_input)
    if multiplier is not None:
        print("Multiplier:", multiplier)
    else:
        print("Unknown concession category. Valid options:", ", ".join(CONCESSION_DISCOUNTS))

    print("\n==== Running compute_passenger_density ====")
    d_input = input("Enter passengers/km (e.g. 50/10.0): ")
    density = compute_passenger_density(d_input)
    if density is not None:
        print("Density:", density)
    else:
        print("Invalid input. Expected PASSENGERS/KM with passengers >= 0 and km > 0, e.g. 50/10.0")


if __name__ == "__main__":
    main()
