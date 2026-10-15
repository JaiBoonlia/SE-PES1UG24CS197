# Lab 5: Static Code Analysis — Issue Log

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Mutable default argument | Code quality / Bug | 9 | `zone_records=[]` is shared across function calls. | Use `None` as the default and initialize a new list when needed. |
| Bare exception handling | Code quality / Reliability | 16, 22, 29, 43 | Bare `except` blocks catch unexpected errors and hide their causes. | Catch specific exceptions and handle them appropriately. |
| Weak random number generation | Security | 11 | Bandit flags `random.randint()` for generating permit identifiers. | Use `secrets` for security-sensitive identifiers. |
| Silent exception handling | Security / Reliability | 22–23 | `except: pass` hides errors when revoking a permit. | Handle a missing permit explicitly. |
| Global state mutation | Maintainability | 40–44 | `load_permit_database()` replaces the global `permits` dictionary. | Return loaded data and update the state explicitly. |
| Unsafe file handling | Reliability | 42, 47 | Files are opened without context managers or explicit encoding. | Use `with open(...)` and specify an encoding. |
| Inconsistent expiry format | Functional bug | 27, 51–52 | `setExpiry()` accepts a date format that `is_expired()` cannot parse. | Validate and standardize dates as YYYY-MM-DD. |
| Invalid plate and zone values | Input validation | 12, 60–63 | Empty plates, `None`, and unsupported zones can be registered. | Validate inputs before creating permits. |
| Missing docstrings | Code quality | Multiple | The module and functions lack explanatory docstrings. | Add module and function docstrings. |
| Inconsistent naming | Style | 51 | `setExpiry` does not follow Python snake_case naming. | Rename it to `set_expiry`. |
