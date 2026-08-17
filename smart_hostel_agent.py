"""
Smart Hostel / Airbnb Unified Management Agent
===============================================================================
A single intelligent agent incorporating three core AI decision-making paradigms:
- Functionality 1 (Simple Reflex): Room Behavior Monitoring (Person 1)
- Functionality 2 (Goal-Based): Roommate Compatibility & Goal Check (Person 2)
- Functionality 3 (Utility-Based): Room Selection & Utility Scoring (Person 3)
===============================================================================
"""

class SmartHostelAgent:
    def __init__(self, name="SmartHostelAgent-Unified"):
        self.name = name
        
        # =====================================================================
        # AGENT CONFIGURATION & KNOWLEDGE BASE
        # =====================================================================
        # Default weights for utility calculation (Sum to 1.0) - Person 3
        self.utility_weights = {
            "affordability": 0.25,
            "distance": 0.15,
            "facilities": 0.20,
            "noise": 0.15,
            "compatibility": 0.25,
        }

        # Lifestyle attribute importance weights for Goal-Based matching - Person 2
        self.preference_weights = {
            "smoking": 0.30,        # Critical deal-breaker
            "sleep_schedule": 0.25,
            "cleanliness": 0.20,
            "noise_tolerance": 0.15,
            "study_habits": 0.10,
        }

    # =========================================================================
    # FUNCTIONALITY 3: UTILITY-BASED ROOM SELECTION
    # Implemented by: Person 3 (Het - First Contributor)
    # Architecture: Utility-Based Agent
    # =========================================================================
    def normalize_room_attributes(self, room, max_rent=15000, max_distance=10):
        """
        Normalizes raw multi-attribute factors into standard 0-100 scores:
        - Rent: lower rent -> higher affordability score
        - Distance: closer distance -> higher proximity score
        - Facilities: direct 0-10 rating scaled to 0-100
        - Noise: Low=100, Med=50, High=20
        - Compatibility: direct percentage (0-100)
        """
        # Affordability: 100 is cheapest, 0 is max_rent or above
        affordability_score = max(0.0, min(100.0, (1.0 - (room["rent"] / max_rent)) * 100.0))
        
        # Proximity: 100 is 0km away, 0 is max_distance or further
        distance_score = max(0.0, min(100.0, (1.0 - (room["distance_km"] / max_distance)) * 100.0))
        
        # Facilities score (0-10 scaled to 0-100)
        facilities_score = max(0.0, min(100.0, (room["facilities_rating"] / 10.0) * 100.0))

        # Noise level scoring
        noise_map = {"Low": 100.0, "Medium": 50.0, "High": 20.0}
        noise_score = noise_map.get(room.get("noise_level", "Medium"), 50.0)
        
        # Roommate compatibility score (0-100)
        compatibility_score = float(room.get("roommate_compatibility", 50.0))

        return {
            "affordability": round(affordability_score, 2),
            "distance": round(distance_score, 2),
            "facilities": round(facilities_score, 2),
            "noise": round(noise_score, 2),
            "compatibility": round(compatibility_score, 2),
        }

    def calculate_room_utility(self, room, custom_weights=None):
        """
        Computes total utility U(room) = SUM(weight_i * normalized_score_i).
        Returns total utility score and component-wise score breakdown.
        """
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
        """
        Evaluates candidate rooms, ranks them by utility, and selects the optimal room.
        """
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

        # Sort rooms in descending order of utility
        evaluated_rooms.sort(key=lambda x: x["utility_score"], reverse=True)
        return best_room, highest_utility, evaluated_rooms

    # =========================================================================
    # FUNCTIONALITY 2: GOAL-BASED ROOMMATE MATCHING
    # Implemented by: Person 2 (Second Contributor)
    # Architecture: Goal-Based Agent
    # =========================================================================
    def calculate_roommate_compatibility(self, user_prefs, candidate_prefs):
        """
        Calculates weighted lifestyle compatibility score between user and candidate.
        Considers: smoking (strict constraint), sleep schedule, cleanliness, noise tolerance, study habits.
        """
        score = 0.0

        # Strict Deal-breaker: Smoking mismatch
        if user_prefs.get("smoking") == "No" and candidate_prefs.get("smoking") == "Yes":
            # Significant penalty for non-smoker paired with smoker
            smoking_score = 0.0
        elif user_prefs.get("smoking") == candidate_prefs.get("smoking"):
            smoking_score = 100.0
        else:
            smoking_score = 30.0
        score += self.preference_weights["smoking"] * smoking_score

        # Sleep Schedule comparison
        if user_prefs.get("sleep_schedule") == candidate_prefs.get("sleep_schedule"):
            sleep_score = 100.0
        elif "Flexible" in (user_prefs.get("sleep_schedule", ""), candidate_prefs.get("sleep_schedule", "")):
            sleep_score = 75.0
        else:
            sleep_score = 25.0
        score += self.preference_weights["sleep_schedule"] * sleep_score

        # Cleanliness comparison
        clean_ranks = {"Low": 1, "Medium": 2, "High": 3}
        u_clean = clean_ranks.get(user_prefs.get("cleanliness", "Medium"), 2)
        c_clean = clean_ranks.get(candidate_prefs.get("cleanliness", "Medium"), 2)
        clean_diff = abs(u_clean - c_clean)
        clean_score = 100.0 if clean_diff == 0 else (60.0 if clean_diff == 1 else 10.0)
        score += self.preference_weights["cleanliness"] * clean_score

        # Noise Tolerance comparison
        noise_ranks = {"Low": 1, "Medium": 2, "High": 3}
        u_noise = noise_ranks.get(user_prefs.get("noise_tolerance", "Medium"), 2)
        c_noise = noise_ranks.get(candidate_prefs.get("noise_tolerance", "Medium"), 2)
        noise_diff = abs(u_noise - c_noise)
        noise_pref_score = 100.0 if noise_diff == 0 else (60.0 if noise_diff == 1 else 10.0)
        score += self.preference_weights["noise_tolerance"] * noise_pref_score

        # Study Habits comparison
        if user_prefs.get("study_habits") == candidate_prefs.get("study_habits"):
            study_score = 100.0
        else:
            study_score = 40.0
        score += self.preference_weights["study_habits"] * study_score

        return round(score, 2)

    def match_roommate_goal(self, candidates, user_prefs, goal_threshold=70.0):
        """
        Goal-Based Agent Decision Engine:
        Evaluates candidate pool to find candidates satisfying the Goal:
            Goal: CompatibilityScore(user, candidate) >= goal_threshold
        Filters valid candidates and returns the best match.
        """
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

    # =========================================================================
    # FUNCTIONALITY 1: SIMPLE REFLEX ROOM BEHAVIOR MONITOR
    # Implemented by: Person 1 (Third Contributor)
    # Architecture: Simple Reflex Agent
    # =========================================================================
    def monitor_room_conditions(self, percepts):
        """
        Simple Reflex Engine:
        Direct Condition-Action (If-Then) mapping based solely on current sensor percepts.
        Maintains no state history and performs no search/planning.
        
        Evaluates percepts:
        - noise_db (int): Live sound level in decibels
        - door_locked (bool): Door security status
        - light_on (bool): Room lighting status
        - occupied (bool): Motion / PIR occupancy sensor
        - smoke_detected (bool, optional): Smoke sensor
        - temperature_c (float, optional): Room temperature
        """
        actions = []

        # Reflex Rule 1: Noise Level Violation
        noise_level = percepts.get("noise_db", 0)
        if noise_level > 60:
            actions.append(f"Noise level high ({noise_level} dB) -> Triggered warning alert")

        # Reflex Rule 2: Security & Door Lock Check
        if not percepts.get("door_locked", True):
            actions.append("Door unlocked -> Auto-locked door & sent security notification")

        # Reflex Rule 3: Energy Conservation (Empty Room with Lights ON)
        if percepts.get("light_on", False) and not percepts.get("occupied", False):
            actions.append("Room unoccupied with lights on -> Automatically turned off lights")

        # Reflex Rule 4: Fire / Smoke Hazard Reflex
        if percepts.get("smoke_detected", False):
            actions.append("Smoke detected -> Triggered fire alarm and unlocked exits")

        # Reflex Rule 5: HVAC / Climate Control
        temp = percepts.get("temperature_c")
        if temp is not None:
            if temp > 28.0:
                actions.append(f"Room temperature high ({temp}C) -> Activated AC cooling")
            elif temp < 18.0:
                actions.append(f"Room temperature low ({temp}C) -> Activated heating")

        # Default Reflex: Normal Operation
        if not actions:
            actions.append("All room conditions are normal")

        return actions

    # =========================================================================
    # UNIFIED EXECUTION PIPELINE
    # =========================================================================
    def run_full_pipeline(self, room_percepts, user_prefs, candidates, available_rooms, goal_threshold=70.0):
        """
        Runs the complete accommodation agent decision cycle.
        """
        print("\n" + "=" * 60)
        print("          SMART HOSTEL MANAGEMENT SYSTEM")
        print("=" * 60)

        # -------------------------------------------------------------
        # MODULE 1: ROOM BEHAVIOR MONITORING (Simple Reflex)
        # -------------------------------------------------------------
        print("\n--- 1. Live Room Monitoring ---")
        print(f"Status: Noise {room_percepts.get('noise_db')}dB | Door: {'Locked' if room_percepts.get('door_locked') else 'Unlocked'} | "
              f"Light: {'ON' if room_percepts.get('light_on') else 'OFF'} | Occupied: {'Yes' if room_percepts.get('occupied') else 'No'} | Temp: {room_percepts.get('temperature_c', 'N/A')}C")
        
        actions = self.monitor_room_conditions(room_percepts)
        print("Actions Taken:")
        for action in actions:
            print(f"  * {action}")

        # -------------------------------------------------------------
        # MODULE 2: ROOMMATE COMPATIBILITY (Goal-Based)
        # -------------------------------------------------------------
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

        # -------------------------------------------------------------
        # MODULE 3: ROOM SELECTION (Utility-Based)
        # -------------------------------------------------------------
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


# =============================================================================
# DEMO EXECUTION
# =============================================================================
if __name__ == "__main__":
    agent = SmartHostelAgent()

    # 1. Test Percepts for Person 1 (Simple Reflex)
    sample_percepts = {
        "noise_db": 74,
        "door_locked": False,
        "light_on": True,
        "occupied": False,
        "smoke_detected": False,
        "temperature_c": 30.5
    }

    # 2. Test Preferences & Candidates for Person 2 (Goal-Based)
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

    # 3. Test Room Listings for Person 3 (Utility-Based)
    hostel_rooms = [
        {"room_id": "101", "rent": 8000, "distance_km": 2.0, "facilities_rating": 8.0, "noise_level": "Low"},
        {"room_id": "102", "rent": 6500, "distance_km": 5.0, "facilities_rating": 7.0, "noise_level": "High"},
        {"room_id": "103", "rent": 9000, "distance_km": 1.0, "facilities_rating": 10.0, "noise_level": "Low"}
    ]

    # Run the full agent integration
    agent.run_full_pipeline(
        room_percepts=sample_percepts,
        user_prefs=user_lifestyle,
        candidates=roommate_candidates,
        available_rooms=hostel_rooms,
        goal_threshold=70.0
    )
