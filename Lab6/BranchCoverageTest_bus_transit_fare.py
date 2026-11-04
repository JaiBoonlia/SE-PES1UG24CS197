import pytest
from bus_transit_fare import (
    process_commute_manifest,
    inspect_smartcard_turnstiles,
)


@pytest.mark.parametrize("manifests,fee,expected", [
    ([], 2.0, {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}),
    ([{"route_active": False}], 2.0, {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}),
    ([{"route_active": True, "route_type": "local", "commuters": [{"zones": 2}]}], 2.0,
     {"total_fare": 4.5, "status": "COMPLETED"}),
    ([{"route_active": True, "route_type": "express", "commuters": [{"zones": 2}]}], 2.0,
     {"total_fare": 8.0, "status": "COMPLETED"}),
    ([{"route_active": True, "route_type": "shuttle", "commuters": [{"zones": 2}]}], 2.0,
     {"total_fare": 6.0, "status": "COMPLETED"}),
    ([{"route_active": True, "route_type": "other", "commuters": []}], 2.0,
     {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}),
    ([{"route_active": True, "commuters": [{"zones": 0}]}], 2.0,
     {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}),
    ([{"route_active": True, "commuters": [{"zones": 1, "type": "student"}]}], 2.0,
     {"total_fare": 1.5, "status": "COMPLETED"}),
    ([{"route_active": True, "commuters": [{"zones": 1, "type": "senior"}]}], 2.0,
     {"total_fare": 2.1, "status": "COMPLETED"}),
    ([{"route_active": True, "commuters": [{"zones": 1, "type": "regular"}]}], 2.0,
     {"total_fare": 3.5, "status": "COMPLETED"}),
    ([{"route_active": True, "commuters": [{"zones": 1, "blacklisted": True}]}], 2.0,
     {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}),
    ([{"route_active": True, "route_type": "express", "commuters": [
        {"zones": 1}, {"zones": 1, "blacklisted": True}]}], 2.0,
     {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}),
    ([{"route_active": True, "commuters": [], "priority_boarding": True}], 2.0,
     {"total_fare": 2.0, "status": "COMPLETED"}),
    ([{"route_active": True, "commuters": []}], 2.0,
     {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}),
    ([{"route_active": True, "route_type": "bad", "commuters": []} for _ in range(5)], 2.0,
     {"total_fare": 0.0, "status": "AUDIT_REJECTED"}),
])
def test_manifest_branch_scenarios(manifests, fee, expected):
    assert process_commute_manifest(manifests, fee) == expected


@pytest.mark.parametrize("manifests,fee", [
    ("invalid", 2.0),
    ([], -0.1),
])
def test_manifest_validation_raises(manifests, fee):
    with pytest.raises(ValueError):
        process_commute_manifest(manifests, fee)


@pytest.mark.parametrize("matrix,expected", [
    ([], "NO_DATA"),
    (None, "NO_DATA"),
    ([[1, 4, 2, 5]], "OPERATIONAL"),
    ([[4, 5]], "TURNSTILE_JAM"),
    ([[4, 3, 4]], "OPERATIONAL"),
    ([[4], [5, 4]], "TURNSTILE_JAM"),
    ([[3, 3, 3]], "OPERATIONAL"),
])
def test_turnstile_branch_scenarios(matrix, expected):
    assert inspect_smartcard_turnstiles(matrix) == expected
