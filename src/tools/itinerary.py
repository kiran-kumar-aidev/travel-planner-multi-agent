"""
Naive itinerary builder (greedy nearest-next).

Inputs:
 - places: list of {"name","lat","lon"} (order doesn't matter)
 - matrix: output from compute_matrix_from_places(...) with keys:
     "names", "duration_s", "duration_readable"
 - start_index: index in places to start each day from (default 0)
 - places_per_day: max number of places to visit in a single day (default 4)
 - start_time_str: "09:00" default start time for each day
 - dwell_time_min: minutes spent at each place (default 60)
 - max_drive_time_per_day_s: maximum driving seconds per day (default 4 hours)

Returns:
 - itinerary: list of day dicts. Each day dict contains ordered visits with timing info
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import math

def _parse_time_str(t: str) -> (int, int):
    hh, mm = t.split(":")
    return int(hh), int(mm)

def build_itinerary(
    places: List[Dict[str, Any]],
    matrix: Dict[str, Any],
    start_index: int = 0,
    places_per_day: int = 4,
    start_time_str: str = "09:00",
    dwell_time_min: int = 60,
    max_drive_time_per_day_s: int = 4 * 3600
) -> List[Dict[str, Any]]:
    n = len(places)
    if n == 0:
        return []

    # Basic validation
    if "duration_s" not in matrix:
        raise ValueError("matrix must contain 'duration_s' (pairwise durations in seconds)")

    durations = matrix["duration_s"]  # matrix: list of lists
    names = matrix["names"]

    # Map place names -> index for safe lookup (defensive)
    name_to_index = {names[i]: i for i in range(len(names))}

    # We'll keep a visited set of indices
    visited = set()

    # Start from start_index each day (hotel/center)
    # But to avoid revisiting start as a POI, if start_index is also in places list we treat it as starting location.
    itinerary = []
    dwell_td = timedelta(minutes=dwell_time_min)
    hh, mm = _parse_time_str(start_time_str)

    # If start_index is outside range, default to 0
    if start_index < 0 or start_index >= n:
        start_index = 0

    # If start_index is a POI that should not be counted as visited automatically, we won't mark it visited until explicitly visited.
    # But the algorithm treats start_index as the day's origin each morning.
    remaining = set(range(n))

    # We'll repeat until all places are visited or cannot fit
    while remaining:
        day = {"date_start_time": None, "visits": []}
        # day clock starts at start_time (naive date - we don't use actual dates, just times)
        day_clock = datetime.combine(datetime.today(), datetime.min.time()).replace(hour=hh, minute=mm, second=0, microsecond=0)
        if day["date_start_time"] is None:
            day["date_start_time"] = day_clock.isoformat()

        current_idx = start_index
        day_drive_seconds = 0
        places_count = 0

        # If start is itself in remaining and we want to visit it, it will be handled like other places.
        # Greedy loop: pick nearest unvisited from current_idx
        while remaining and places_count < places_per_day:
            # Find nearest unvisited
            best = None
            best_dur = math.inf
            for cand in remaining:
                if cand == current_idx:
                    # if candidate is same as current, treat travel time = 0
                    dur = 0
                else:
                    try:
                        dur = durations[current_idx][cand]
                        # if duration is inf or very large, skip
                        if dur is None:
                            dur = math.inf
                    except Exception:
                        dur = math.inf
                if dur < best_dur:
                    best_dur = dur
                    best = cand

            if best is None or best_dur == math.inf:
                # No reachable remaining places
                break

            # Check travel budget: if adding best_dur would exceed max_drive_time_per_day_s, stop day
            if day_drive_seconds + (0 if current_idx == best else best_dur) > max_drive_time_per_day_s:
                break

            # Add travel time to day_drive_seconds and advance the clock
            travel_sec = 0 if current_idx == best else best_dur
            # Move clock by travel time
            day_clock += timedelta(seconds=travel_sec)
            day_drive_seconds += travel_sec

            # Record arrival time
            arrival = day_clock

            # Record visit
            visit = {
                "place_index": best,
                "name": places[best].get("name"),
                "arrival_time": arrival.isoformat(),
                "travel_from_index": current_idx,
                "travel_time_s": int(travel_sec),
                "travel_time_readable": _sec_to_readable(travel_sec)
            }

            # Spend dwell time
            day_clock += dwell_td
            visit["departure_time"] = day_clock.isoformat()

            day["visits"].append(visit)

            # Mark visited and increment counters
            remaining.discard(best)
            visited.add(best)
            places_count += 1

            # Move current pointer to best
            current_idx = best

        itinerary.append(day)

        # Safety: if no progress (can't visit any place because of travel budget), try to force one (to avoid infinite loop)
        if places_count == 0:
            # pick one remaining (lowest index) and force it onto day regardless of budget
            forced = min(remaining)
            travel_sec = durations[current_idx][forced] if current_idx != forced else 0
            day_clock += timedelta(seconds=travel_sec)
            arrival = day_clock
            day_clock += dwell_td
            visit = {
                "place_index": forced,
                "name": places[forced].get("name"),
                "arrival_time": arrival.isoformat(),
                "departure_time": day_clock.isoformat(),
                "travel_from_index": current_idx,
                "travel_time_s": int(travel_sec),
                "travel_time_readable": _sec_to_readable(travel_sec)
            }
            day["visits"].append(visit)
            remaining.discard(forced)
            visited.add(forced)

    return itinerary


def _sec_to_readable(sec: float) -> str:
    if sec is None or sec == float("inf"):
        return "∞"
    s = int(round(sec))
    if s < 60:
        return f"{s}s"
    mins = s // 60
    if mins < 60:
        return f"{mins}m {s%60}s"
    hours = mins // 60
    mins = mins % 60
    return f"{hours}h {mins}m"
