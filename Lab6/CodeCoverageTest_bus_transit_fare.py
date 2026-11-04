import pytest
from bus_transit_fare import (
    process_commute_manifest,
    inspect_smartcard_turnstiles,
)


def test_single_regular_local_ride():
    result = process_commute_manifest(
        [{"route_active": True, "route_type": "local",
          "commuters": [{"zones": 2, "type": "regular"}]}], 2.0
    )
    assert result == {"total_fare": 4.5, "status": "COMPLETED"}


def test_invalid_manifest_argument():
    with pytest.raises(ValueError):
        process_commute_manifest("not-a-list", 2.0)


def test_negative_booking_fee():
    with pytest.raises(ValueError):
        process_commute_manifest([], -1.0)


def test_inactive_route_is_skipped():
    result = process_commute_manifest([{"route_active": False}], 2.0)
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_default_local_route_and_default_commuter_values():
    result = process_commute_manifest([{"route_active": True, "commuters": [{}]}], 2.0)
    assert result == {"total_fare": 3.5, "status": "COMPLETED"}


def test_express_shuttle_and_local_fares():
    manifests = [
        {"route_active": True, "route_type": "express", "commuters": [{"zones": 2}]},
        {"route_active": True, "route_type": "shuttle", "commuters": [{"zones": 2}]},
        {"route_active": True, "route_type": "local", "commuters": [{"zones": 2}]},
    ]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {"total_fare": 18.5, "status": "COMPLETED"}


def test_unknown_route_is_rejected():
    result = process_commute_manifest(
        [{"route_active": True, "route_type": "intercity", "commuters": []}], 2.0
    )
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_non_positive_zones_are_rejected():
    result = process_commute_manifest(
        [{"route_active": True, "commuters": [{"zones": 0}, {"zones": -2}]}], 2.0
    )
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_student_senior_and_regular_fares():
    result = process_commute_manifest(
        [{"route_active": True, "route_type": "local", "commuters": [
            {"zones": 2, "type": "student"},
            {"zones": 2, "type": "senior"},
            {"zones": 2, "type": "regular"},
        ]}], 2.0
    )
    assert result == {"total_fare": 8.7, "status": "COMPLETED"}


def test_blacklisted_local_commuter_adds_no_fare():
    result = process_commute_manifest(
        [{"route_active": True, "route_type": "local", "commuters": [
            {"zones": 2, "type": "regular", "blacklisted": True},
            {"zones": 2, "type": "regular"},
        ]}], 2.0
    )
    assert result == {"total_fare": 4.5, "status": "COMPLETED"}


def test_blacklisted_express_commuter_cancels_manifest_fare():
    result = process_commute_manifest(
        [{"route_active": True, "route_type": "express", "priority_boarding": False,
          "commuters": [{"zones": 2}, {"zones": 2, "blacklisted": True}, {"zones": 1}]}], 2.0
    )
    assert result == {"total_fare": 0.0, "status": "ZERO_RIDERSHIP"}


def test_priority_boarding_adds_booking_fee():
    result = process_commute_manifest(
        [{"route_active": True, "commuters": [{"zones": 1}], "priority_boarding": True}], 2.0
    )
    assert result == {"total_fare": 5.5, "status": "COMPLETED"}


def test_priority_fee_can_make_zero_ridership_nonzero():
    result = process_commute_manifest(
        [{"route_active": True, "commuters": [], "priority_boarding": True}], 2.0
    )
    assert result == {"total_fare": 2.0, "status": "COMPLETED"}


def test_audit_rejected_after_more_than_four_rejections():
    manifests = [{"route_active": True, "route_type": "unknown", "commuters": []} for _ in range(5)]
    result = process_commute_manifest(manifests, 2.0)
    assert result == {"total_fare": 0.0, "status": "AUDIT_REJECTED"}


def test_turnstile_empty_matrix():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"
    assert inspect_smartcard_turnstiles(None) == "NO_DATA"


def test_turnstile_operational_with_no_consecutive_high_failures():
    assert inspect_smartcard_turnstiles([[4, 2, 5], [3, 4]]) == "OPERATIONAL"


def test_turnstile_jam_on_two_consecutive_high_failures():
    assert inspect_smartcard_turnstiles([[4, 5]]) == "TURNSTILE_JAM"


def test_turnstile_failure_streak_resets_after_three_or_less():
    assert inspect_smartcard_turnstiles([[4, 3, 4]]) == "OPERATIONAL"
