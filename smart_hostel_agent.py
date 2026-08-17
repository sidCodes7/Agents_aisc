class SmartHostelAgent:
    def __init__(self, name="SmartHostelAgent-Unified"):
        self.name = name
        
        # Utility weights (must sum to 1.0)
        self.utility_weights = {
            "affordability": 0.25,
            "distance": 0.15,
            "facilities": 0.20,
            "noise": 0.15,
            "compatibility": 0.25,
        }

        # Weights for roommate preference matching
        self.preference_weights = {
            "smoking": 0.30,
            "sleep_schedule": 0.25,
            "cleanliness": 0.20,
            "noise_tolerance": 0.15,
            "study_habits": 0.10,
        }

    # --- Utility-based Room Selection ---

    def normalize_room_attributes(self, room, max_rent=15000, max_distance=10):
        # Scale attributes to 0-100 scores
        affordability_score = max(0.0, min(100.0, (1.0 - (room["rent"] / max_rent)) * 100.0))
        distance_score = max(0.0, min(100.0, (1.0 - (room["distance_km"] / max_distance)) * 100.0))
        facilities_score = max(0.0, min(100.0, (room["facilities_rating"] / 10.0) * 100.0))

        noise_map = {"Low": 100.0, "Medium": 50.0, "High": 20.0}
        noise_score = noise_map.get(room.get("noise_level", "Medium"), 50.0)
        compatibility_score = float(room.get("roommate_compatibility", 50.0))

        return {
            "affordability": round(affordability_score, 2),
            "distance": round(distance_score, 2),
            "facilities": round(facilities_score, 2),
            "noise": round(noise_score, 2),
            "compatibility": round(compatibility_score, 2),
        }

    def calculate_room_utility(self, room, custom_weights=None):
        weights = custom_weights or self.utility_weights
        norm_scores = self.normalize_room_attributes(room)

        breakdown = {}
        total_utility = 0.0

        for factor, weight in weights.items():
            factor_contribution = weight * norm_scores[factor]
            breakdown[factor] = round(factor_contribution, 2)
            total_utility += factor_contribution

        return round(total_utility, 2), breakdown

    def select_best_room(self, rooms, custom_weights=None):
        if not rooms:
            return None, 0.0, []

        evaluated_rooms = []
        best_room = None
        highest_utility = -1.0

        for room in rooms:
            utility, breakdown = self.calculate_room_utility(room, custom_weights)
            evaluated_rooms.append({
                "room": room,
                "utility_score": utility,
                "breakdown": breakdown
            })
            if utility > highest_utility:
                highest_utility = utility
                best_room = room

        evaluated_rooms.sort(key=lambda x: x["utility_score"], reverse=True)
        return best_room, highest_utility, evaluated_rooms

    # --- Goal-based Roommate Matching ---

    def calculate_roommate_compatibility(self, user_prefs, candidate_prefs):
        score = 0.0

        # Smoking is a strict deal breaker
        if user_prefs.get("smoking") == "No" and candidate_prefs.get("smoking") == "Yes":
            smoking_score = 0.0
        elif user_prefs.get("smoking") == candidate_prefs.get("smoking"):
            smoking_score = 100.0
        else:
            smoking_score = 30.0
        score += self.preference_weights["smoking"] * smoking_score

        # Sleep schedule
        if user_prefs.get("sleep_schedule") == candidate_prefs.get("sleep_schedule"):
            sleep_score = 100.0
        elif "Flexible" in (user_prefs.get("sleep_schedule", ""), candidate_prefs.get("sleep_schedule", "")):
            sleep_score = 75.0
        else:
            sleep_score = 25.0
        score += self.preference_weights["sleep_schedule"] * sleep_score

        # Cleanliness
        clean_ranks = {"Low": 1, "Medium": 2, "High": 3}
        u_clean = clean_ranks.get(user_prefs.get("cleanliness", "Medium"), 2)
        c_clean = clean_ranks.get(candidate_prefs.get("cleanliness", "Medium"), 2)
        clean_diff = abs(u_clean - c_clean)
        clean_score = 100.0 if clean_diff == 0 else (60.0 if clean_diff == 1 else 10.0)
        score += self.preference_weights["cleanliness"] * clean_score

        # Noise tolerance
        noise_ranks = {"Low": 1, "Medium": 2, "High": 3}
        u_noise = noise_ranks.get(user_prefs.get("noise_tolerance", "Medium"), 2)
        c_noise = noise_ranks.get(candidate_prefs.get("noise_tolerance", "Medium"), 2)
        noise_diff = abs(u_noise - c_noise)
        noise_pref_score = 100.0 if noise_diff == 0 else (60.0 if noise_diff == 1 else 10.0)
        score += self.preference_weights["noise_tolerance"] * noise_pref_score

        # Study habits
        if user_prefs.get("study_habits") == candidate_prefs.get("study_habits"):
            study_score = 100.0
        else:
            study_score = 40.0
        score += self.preference_weights["study_habits"] * study_score

        return round(score, 2)

    def match_roommate_goal(self, candidates, user_prefs, goal_threshold=70.0):
        evaluation_results = []
        qualified_candidates = []
        best_candidate = None
        best_score = -1.0

        for candidate in candidates:
            score = self.calculate_roommate_compatibility(user_prefs, candidate["preferences"])
            is_goal_met = score >= goal_threshold

            record = {
                "name": candidate["name"],
                "score": score,
                "goal_threshold": goal_threshold,
                "goal_achieved": is_goal_met,
                "details": candidate["preferences"]
            }
            evaluation_results.append(record)

            if is_goal_met:
                qualified_candidates.append(candidate)
                if score > best_score:
                    best_score = score
                    best_candidate = candidate

        return best_candidate, best_score, evaluation_results

    # --- Simple Reflex Room Monitoring ---

    def monitor_room_conditions(self, percepts):
        actions = []

        noise_level = percepts.get("noise_db", 0)
        if noise_level > 60:
            actions.append(f"Noise level high ({noise_level} dB) -> Triggered warning alert")

        if not percepts.get("door_locked", True):
            actions.append("Door unlocked -> Auto-locked door & sent security notification")

        if percepts.get("light_on", False) and not percepts.get("occupied", False):
            actions.append("Room unoccupied with lights on -> Automatically turned off lights")

        if percepts.get("smoke_detected", False):
            actions.append("Smoke detected -> Triggered fire alarm and unlocked exits")

        temp = percepts.get("temperature_c")
        if temp is not None:
            if temp > 28.0:
                actions.append(f"Room temperature high ({temp}C) -> Activated AC cooling")
            elif temp < 18.0:
                actions.append(f"Room temperature low ({temp}C) -> Activated heating")

        if not actions:
            actions.append("All room conditions are normal")

        return actions

    # --- Pipeline ---

    def run_full_pipeline(self, room_percepts, user_prefs, candidates, available_rooms, goal_threshold=70.0):
        print("\n" + "=" * 60)
        print("          SMART HOSTEL MANAGEMENT SYSTEM")
        print("=" * 60)

        # 1. Live room monitoring
        print("\n--- 1. Live Room Monitoring ---")
        print(f"Status: Noise {room_percepts.get('noise_db')}dB | Door: {'Locked' if room_percepts.get('door_locked') else 'Unlocked'} | "
              f"Light: {'ON' if room_percepts.get('light_on') else 'OFF'} | Occupied: {'Yes' if room_percepts.get('occupied') else 'No'} | Temp: {room_percepts.get('temperature_c', 'N/A')}C")
        
        actions = self.monitor_room_conditions(room_percepts)
        print("Actions Taken:")
        for action in actions:
            print(f"  * {action}")

        # 2. Roommate compatibility
        print("\n--- 2. Roommate Compatibility (Goal: >= 70%) ---")
        best_cand, best_cand_score, cand_results = self.match_roommate_goal(
            candidates, user_prefs, goal_threshold=goal_threshold
        )

        for res in cand_results:
            status = "MATCH" if res["goal_achieved"] else "NO MATCH"
            print(f"  * {res['name']:<8} : {res['score']:>5.1f}% compatibility [{status}]")

        if best_cand:
            print(f"Selected Roommate: {best_cand['name']} ({best_cand_score}%)")
        else:
            print("Selected Roommate: None (No candidate met threshold)")

        # 3. Room selection
        print("\n--- 3. Room Selection (Utility Scoring) ---")
        assigned_comp = best_cand_score if best_cand_score > 0 else 50.0
        for room in available_rooms:
            room["roommate_compatibility"] = assigned_comp

        best_room, best_utility, all_evaluated = self.select_best_room(available_rooms)
        
        for item in all_evaluated:
            r = item["room"]
            print(f"  * Room {r['room_id']:<3} -> Utility: {item['utility_score']:>5.1f}/100 "
                  f"(Rent: Rs.{r['rent']}, Dist: {r['distance_km']}km, Facilities: {r['facilities_rating']}/10, Noise: {r['noise_level']})")

        if best_room:
            print(f"Recommended Room: Room {best_room['room_id']} (Best Utility Score: {best_utility}/100)")
        
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    agent = SmartHostelAgent()

    sample_percepts = {
        "noise_db": 74,
        "door_locked": False,
        "light_on": True,
        "occupied": False,
        "smoke_detected": False,
        "temperature_c": 30.5
    }

    user_lifestyle = {
        "sleep_schedule": "Early",
        "cleanliness": "High",
        "noise_tolerance": "Low",
        "smoking": "No",
        "study_habits": "Quiet"
    }

    roommate_candidates = [
        {
            "name": "Rahul",
            "preferences": {
                "sleep_schedule": "Early",
                "cleanliness": "High",
                "noise_tolerance": "Low",
                "smoking": "No",
                "study_habits": "Quiet"
            }
        },
        {
            "name": "Amit",
            "preferences": {
                "sleep_schedule": "Late",
                "cleanliness": "Low",
                "noise_tolerance": "High",
                "smoking": "Yes",
                "study_habits": "Group"
            }
        },
        {
            "name": "Jay",
            "preferences": {
                "sleep_schedule": "Early",
                "cleanliness": "High",
                "noise_tolerance": "Low",
                "smoking": "No",
                "study_habits": "Group"
            }
        }
    ]

    hostel_rooms = [
        {"room_id": "101", "rent": 8000, "distance_km": 2.0, "facilities_rating": 8.0, "noise_level": "Low"},
        {"room_id": "102", "rent": 6500, "distance_km": 5.0, "facilities_rating": 7.0, "noise_level": "High"},
        {"room_id": "103", "rent": 9000, "distance_km": 1.0, "facilities_rating": 10.0, "noise_level": "Low"}
    ]

    agent.run_full_pipeline(
        room_percepts=sample_percepts,
        user_prefs=user_lifestyle,
        candidates=roommate_candidates,
        available_rooms=hostel_rooms,
        goal_threshold=70.0
    )
