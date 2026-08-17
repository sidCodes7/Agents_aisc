# 🏠 Smart Hostel / Airbnb Unified Management Agent

> **An AI Agent Case Study featuring a Single Intelligent Agent with Three Core Decision-Making Architectures: Simple Reflex, Goal-Based, and Utility-Based.**

---

## 📌 1. Case Study Overview

The **Smart Hostel / Airbnb Management System** is an AI agent-based case study designed to automate and optimize living conditions, roommate pairing, and accommodation selection in shared hostel/Airbnb environments.

Instead of deploying disconnected scripts, this case study integrates **one comprehensive Intelligent Agent (`SmartHostelAgent`)** equipped with **three distinct decision-making functionalities**:

1. **Room Behavior Monitoring Functionality** — *Simple Reflex Agent Architecture*
2. **Roommate Compatibility Functionality** — *Goal-Based Agent Architecture*
3. **Room Selection Functionality** — *Utility-Based Agent Architecture*

Each functionality represents a foundational intelligent agent architecture, allowing direct comparison of how different decision paradigms (condition-action rules, goal satisfaction, and multi-attribute utility optimization) operate inside a unified system.

---

## 🎯 2. Objectives

* Implement a **single unified agent** possessing three distinct decision mechanisms.
* **Simple Reflex:** Monitor room environmental percepts and trigger instant corrective reflex actions.
* **Goal-Based:** Search and filter candidate roommates against an explicit compatibility goal threshold.
* **Utility-Based:** Balance trade-offs among price, distance, facilities, noise, and compatibility using a multi-criteria utility function to choose the optimal room.
* Demonstrate the relationship between **Sensors, Percepts, Decision Rules, Goals, Utilities, and Actuators** within the **PEAS framework**.
* Support collaborative development through a phased implementation flow ([flow.md](file:///d:/Het/College/sem5/AISC/agentexp/flow.md)).

---

## 🧠 3. Unified Agent Architecture

```text
                           HOSTEL / AIRBNB ENVIRONMENT
                                        │
             ┌──────────────────────────┼──────────────────────────┐
             │                          │                          │
             ▼                          ▼                          ▼
      Room Sensors /             User Lifestyle &           Available Rooms
      Live Percepts             Goal Threshold              & Amenities
             │                          │                          │
             └──────────────────────────┼──────────────────────────┘
                                        │
                                        ▼
    ┌────────────────────────────────────────────────────────────────────────┐
    │                 UNIFIED AGENT: SmartHostelAgent                        │
    ├────────────────────────┬───────────────────────┬───────────────────────┤
    │    FUNCTIONALITY 1     │    FUNCTIONALITY 2    │    FUNCTIONALITY 3    │
    │  Room Behavior Monitor │  Roommate Matcher     │  Room Selection       │
    ├────────────────────────┼───────────────────────┼───────────────────────┤
    │     Simple Reflex      │      Goal-Based       │     Utility-Based     │
    │                        │                       │                       │
    │  • Condition-Action    │  • Goal: Score >= 70% │  • Multi-attribute    │
    │  • No history/planning │  • Evaluates candidates│   utility function   │
    │  • Instant response    │  • Goal check (Y/N)   │  • Trade-off ranking  │
    └───────────┬────────────┴───────────┬───────────┴───────────┬───────────┘
                │                        │                       │
                ▼                        ▼                       ▼
          Alerts / Actions          Matched Roommate        Optimal Room
          (Lock, Lights, Noise)     (Goal Satisfied)        (Highest Utility)
```

---

## 🤖 4. Three Core Agent Functionalities

| Functionality | Architecture Type | Decision Basis | Input Percepts | Primary Output / Actuation |
| :--- | :--- | :--- | :--- | :--- |
| **1. Behavior Monitor** | **Simple Reflex** | Condition-Action Rules | Noise level, door lock, light status, occupancy | Immediate alerts, auto-lock, lights control |
| **2. Roommate Matching** | **Goal-Based** | Goal Satisfaction ($\ge$ Threshold) | User preferences vs. candidate roommate profiles | Goal status & compatible roommate recommendation |
| **3. Room Selection** | **Utility-Based** | Multi-Attribute Utility Function | Rent, distance, facilities, noise, compatibility | Highest-utility room recommendation ($U_{\max}$) |

---

## ⚡ 5. Detailed Breakdown of Functionalities

### 5.1 Functionality 1 — Room Behavior Monitor (Simple Reflex)
* **Design Philosophy:** Operates strictly on immediate percepts without state history or future planning.
* **Mechanism:** Table-lookup condition-action rules:
  $$\text{Condition} \longrightarrow \text{Action}$$
* **Rules & Reflexes:**
  * $\text{Noise} > 60\text{ dB} \longrightarrow \text{"Generate High Noise Alert"}$
  * $\text{Door} = \text{Unlocked} \longrightarrow \text{"Trigger Auto-Lock \& Security Warning"}$
  * $\text{Light} = \text{ON} \land \text{Occupied} = \text{False} \longrightarrow \text{"Turn Off Lights (Energy Saver)"}$
  * $\text{All Normal} \longrightarrow \text{"Maintain Normal Operations"}$

---

### 5.2 Functionality 2 — Roommate Compatibility (Goal-Based)
* **Design Philosophy:** Acts to achieve an explicit target state (Goal).
* **Goal Formulation:** 
  $$\text{Goal: Find Candidate } c \text{ such that } \text{CompatibilityScore}(u, c) \ge \text{GoalThreshold (e.g., } 70\%)$$
* **Attributes Evaluated:** Sleep schedule, cleanliness, noise tolerance, smoking habits, study preferences.
* **Decision Flow:**
  1. Compute match score for each candidate.
  2. Test against goal condition ($\text{Score} \ge 70\%$).
  3. Accept candidate(s) satisfying goal; reject candidates failing goal.

---

### 5.3 Functionality 3 — Room Selection (Utility-Based)
* **Design Philosophy:** Maximizes overall desirability/utility when multiple competing alternatives exist.
* **Utility Formulation:** Normalizes all criteria to $[0, 100]$ scale and applies weighted sum:
  $$U(\text{Room}) = w_1 \cdot \text{Affordability} + w_2 \cdot \text{Distance} + w_3 \cdot \text{Facilities} + w_4 \cdot \text{Noise} + w_5 \cdot \text{Compatibility}$$
* **Default Weights:**
  * Affordability: $0.25$
  * Distance to Campus: $0.15$
  * Facilities / Amenities: $0.20$
  * Low Noise Environment: $0.15$
  * Roommate Compatibility: $0.25$
  * ($\sum w_i = 1.0$)
* **Decision:** Select $\text{Room}^* = \arg\max_{\text{Room}} U(\text{Room})$.

---

## 🧩 6. PEAS Representation of the Unified Agent

| Component | Description |
| :--- | :--- |
| **P — Performance Measure** | Room safety/energy efficiency, user compatibility satisfaction ($\ge 70\%$), and maximum utility of selected accommodation. |
| **E — Environment** | Shared student hostel / Airbnb apartment, candidate roommate pool, and available listings. |
| **A — Actuators** | Warning display / push alerts, electronic lock trigger, power/lighting control, roommate recommendation, room selection report. |
| **S — Sensors / Inputs** | Noise sensor (dB), door status sensor, light & PIR occupancy sensors, user lifestyle survey, candidate database, room listing attributes. |

---

## 👨‍💻 7. Collaborative Implementation Flow

The project follows a structured sequence where each team member implements one agent functionality into the unified `SmartHostelAgent`:

```text
┌───────────────────────────┐     ┌───────────────────────────┐     ┌───────────────────────────┐
│   STEP 1: PERSON 3        │     │   STEP 2: PERSON 2        │     │   STEP 3: PERSON 1        │
│   (Het - First Changes)   │ ──► │   (Second Changes)        │ ──► │   (Third Changes)         │
├───────────────────────────┤     ├───────────────────────────┤     ├───────────────────────────┤
│ • Agent class skeleton    │     │ • Goal-based matching     │     │ • Simple reflex monitor   │
│ • Utility-based room      │     │ • Goal satisfaction check │     │ • Condition-action rules  │
│   selection engine        │     │ • Compatibility scoring   │     │ • Master agent pipeline   │
│ • Weight normalization    │     │                           │     │ • Interactive CLI UI      │
└───────────────────────────┘     └───────────────────────────┘     └───────────────────────────┘
```

> 📖 **Full step-by-step implementation guide:** Refer to [flow.md](file:///d:/Het/College/sem5/AISC/agentexp/flow.md) for code templates, methods, and commit guidelines for each member.

---

## 📁 8. Project Structure

```text
agentexp/
│
├── README.md                 # System overview and case study documentation
├── flow.md                   # Chronological implementation flow (Person 3 -> Person 2 -> Person 1)
└── smart_hostel_agent.py     # Single unified agent containing all 3 functionalities
```

---

## 🚀 9. Running the Unified Agent

To execute the complete unified agent with all three functionalities:

```bash
python smart_hostel_agent.py
```

### Sample Output:
```text
============================================================
          SMART HOSTEL MANAGEMENT SYSTEM
============================================================

--- 1. Live Room Monitoring ---
Status: Noise 74dB | Door: Unlocked | Light: ON | Occupied: No | Temp: 30.5C
Actions Taken:
  * Noise level high (74 dB) -> Triggered warning alert
  * Door unlocked -> Auto-locked door & sent security notification
  * Room unoccupied with lights on -> Automatically turned off lights
  * Room temperature high (30.5C) -> Activated AC cooling

--- 2. Roommate Compatibility (Goal: >= 70%) ---
  * Rahul    : 100.0% compatibility [MATCH]
  * Amit     :  13.8% compatibility [NO MATCH]
  * Jay      :  94.0% compatibility [MATCH]
Selected Roommate: Rahul (100.0%)

--- 3. Room Selection (Utility Scoring) ---
  * Room 103 -> Utility:  83.5/100 (Rent: Rs.9000, Dist: 1.0km, Facilities: 10.0/10, Noise: Low)
  * Room 101 -> Utility:  79.7/100 (Rent: Rs.8000, Dist: 2.0km, Facilities: 8.0/10, Noise: Low)
  * Room 102 -> Utility:  63.7/100 (Rent: Rs.6500, Dist: 5.0km, Facilities: 7.0/10, Noise: High)
Recommended Room: Room 103 (Best Utility Score: 83.5/100)

============================================================
```

---

## 📚 10. Key AI Concepts Summary

* **Simple Reflex:** Direct $S \rightarrow A$ mapping; fast, stateless, ideal for real-time safety.
* **Goal-Based:** Evaluates future states against explicit criteria; flexible, goal-driven search.
* **Utility-Based:** Evaluates trade-offs using continuous objective functions $U(s)$; optimal under competing preferences.
* **Hybrid Unified Agent:** Demonstrates how multiple agent architectures coexist to solve multi-faceted real-world problems.
