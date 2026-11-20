from hypothesis import given, settings, strategies as st
from processor import parse_transit_corridor, lookup_concession_discount, compute_passenger_density


# ---------------------------------------------------------------------------
# 1. Pure fuzzing: random text or None must never crash any function
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_transit_corridor_no_crash(s):
    try:
        parse_transit_corridor(s)
    except Exception as e:
        assert False, f"parse_transit_corridor crashed on {s!r} with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_lookup_concession_discount_safe(s):
    try:
        lookup_concession_discount(s)
    except Exception as e:
        assert False, f"lookup_concession_discount crashed on {s!r} with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_compute_passenger_density_safe(s):
    try:
        compute_passenger_density(s)
    except Exception as e:
        assert False, f"compute_passenger_density crashed on {s!r} with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 2. Structured fuzzing: inputs that *look* valid, to reach deeper edge cases
#    (empty parts, negative / huge numbers, zero km, extra separators, ...)
# ---------------------------------------------------------------------------

corridor_like = st.builds(
    lambda a, b, z, extra: f"{a}-{b}-{z}{extra}",
    st.text(max_size=5),
    st.text(max_size=5),
    st.one_of(st.integers(), st.text(max_size=5), st.just("9" * 5000)),
    st.sampled_from(["", "-", "-X", " "]),
)

@given(corridor_like)
def test_parse_transit_corridor_structured_no_crash(s):
    try:
        parse_transit_corridor(s)
    except Exception as e:
        assert False, f"parse_transit_corridor crashed on {s!r} with: {type(e).__name__}: {e}"


category_like = st.one_of(
    st.sampled_from(["STANDARD", "student", " Senior ", "MILITARY", "child", "VIP", ""]),
    st.text(),
    st.integers(),
    st.lists(st.text(), max_size=3),
)

@given(category_like)
def test_lookup_concession_discount_structured_no_crash(s):
    try:
        lookup_concession_discount(s)
    except Exception as e:
        assert False, f"lookup_concession_discount crashed on {s!r} with: {type(e).__name__}: {e}"


number_like = st.one_of(
    st.integers().map(str),
    st.floats(allow_nan=True, allow_infinity=True).map(str),
    st.sampled_from(["0", "-0", "0.0", "nan", "inf", "-inf", "1e400", ""]),
    st.text(max_size=5),
)

@given(number_like, number_like, st.sampled_from(["", "/", "/1"]))
def test_compute_passenger_density_structured_no_crash(p, km, extra):
    s = f"{p}/{km}{extra}"
    try:
        compute_passenger_density(s)
    except Exception as e:
        assert False, f"compute_passenger_density crashed on {s!r} with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# 3. Correctness properties on genuinely valid inputs (fix must not break them)
# ---------------------------------------------------------------------------

@given(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=4),
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=4),
    st.integers(min_value=0, max_value=100),
)
def test_parse_transit_corridor_valid_fare(orig, dest, zones):
    result = parse_transit_corridor(f"{orig}-{dest}-{zones}")
    expected_fare = 2.50 + zones * 0.75
    assert result == f"Route {orig}->{dest}: {zones} Zones, Fare ${expected_fare:.2f}"


@given(st.sampled_from(["STANDARD", "STUDENT", "SENIOR", "MILITARY", "CHILD"]))
def test_lookup_concession_discount_valid(cat):
    result = lookup_concession_discount(f"  {cat.lower()} ")
    assert isinstance(result, float) and 0.0 <= result <= 1.0


@given(
    st.integers(min_value=0, max_value=10_000),
    st.floats(min_value=0.1, max_value=1_000, allow_nan=False, allow_infinity=False),
)
def test_compute_passenger_density_valid(passengers, km):
    result = compute_passenger_density(f"{passengers}/{km}")
    assert result == round(passengers / km, 2)
