# Issues found - delivery_system.py

Name: Swaroop Venkateshwar
SRN: PES1UG24CS923

Line numbers are from the original file (before my changes).

Pylint score: 6.27/10 before -> 10.00/10 after. Bandit: 3 issues -> 0. Flake8: 12 issues -> 0.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Pickle used to load data (B301, B403) | Security (Bandit Medium + Low) | 2, 49 | `pickle.load` can run any code if someone swaps the orders.pkl file, so it's unsafe | Switched the backup to json (`json.dump` / `json.load`). Json turns int keys into strings so I convert them back to int in restore_orders |
| Mutable default arg `order_history=[]` (W0102) | Bug | 11 | The same list is shared between all calls of create_order so it keeps growing | Default is now `None` and a new list is made inside the function |
| Bare `except:` with `pass` (E722, W0702, B110) | Bug / Security | 22-25 | Every error is hidden, so updating a wrong order id or wrong status fails silently | Removed the try/except. Now it checks if the order exists and if the status is in VALID_STATUSES and prints a message |
| Unknown dishes silently cost 99 | Logic bug (no tool flagged it) | 15 | "sushi" is not on the menu but it got added at 99, so Ravi's total was 249 | Now raises ValueError for a dish that is not in the menu, and main() catches it and prints it |
| Invalid status accepted | Logic bug (no tool flagged it) | 21-25 | "teleported" was saved as a status. VALID_STATUSES was defined but never used | Check `status in VALID_STATUSES` before updating |
| Empty order allowed | Logic bug (no tool flagged it) | 60, 64 | `create_order("", [])` made an order with no customer and no items, and it even got marked delivered | Raise ValueError if customer is empty or items is empty |
| Files opened without `with` (R1732) + no encoding (W1514) | Code quality | 30, 43, 49 | File may not get closed if an error happens in between | Used `with open(..., encoding="utf-8")` everywhere |
| Catching too general `Exception` (W0718) | Code quality | 32 | Catches every error, even ones that have nothing to do with a missing menu file | Only catch `OSError` and `json.JSONDecodeError` |
| `global` statements (W0603) | Design | 12, 28, 48 | Rebinding globals makes the code hard to follow/test. Also next_id went back to 1 after a restore, so ids could clash | Changed to mutate the dicts (`menu.clear()/update()`, `orders.clear()/update()`) and get the new id with `max(orders, default=0) + 1` |
| Bad names `printQueue`, `next_id` (C0103) | Style | 7, 51 | Not snake_case / constant naming | Renamed printQueue to print_queue, and next_id isn't needed anymore |
| Missing docstrings (C0114, C0116) | Style | 1, 11, 21, 27, 35, 42, 47, 51, 56 | Module and all functions had no docstring | Added short docstrings |
| Old `%` string formatting (C0209) | Style | 52 | Pylint wants an f-string | Used an f-string |
| Blank lines E302 / E305 | Style (Flake8) | 11, 21, 27, 35, 42, 47, 51, 56, 70 | Need 2 blank lines around functions | Added blank lines |
| Line too long E501 | Style (Flake8) | 16, 54 | Lines over 79 characters | Split the dict and the print over multiple lines |
| `main()` called at import time | Style / Design | 70 | The demo runs whenever the file is imported | Put it under `if __name__ == "__main__":` |

## Commits

1. Bandit fixes (pickle -> json, removed try/except/pass)
2. Flake8 fixes (blank lines, long lines, main guard)
3. Pylint fixes (docstrings, naming, with open, no globals, validation)
4. Added the reports, issues.md and reflection.md

Reports are in `reports/before` and `reports/after`.
