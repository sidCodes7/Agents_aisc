# 🏠 Smart Hostel / Airbnb Roommate Management System

> **An AI Agent-Based Case Study for Intelligent Room Monitoring, Roommate Matching, and Room Selection**

---

## 📌 1. Case Study Overview

The **Smart Hostel / Airbnb Roommate Management System** is an agent-based AI case study designed to improve the experience of students and guests living in shared accommodation.

The system consists of **three intelligent agents**, where each agent uses a different type of AI agent architecture:

1. **Room Behavior Monitoring Agent** — Simple Reflex Agent
2. **Roommate Compatibility Agent** — Goal-Based Agent
3. **Room Selection Agent** — Utility-Based Agent

Each agent receives specific information from its environment, processes it according to its architecture, and produces an appropriate action or recommendation.

The project is intentionally designed as a **case study rather than a complete application**. Each team member implements one independent agent.

---

# 🎯 2. Objectives

The main objectives of the case study are:

* Monitor room conditions and detect basic violations.
* Identify compatible roommates based on lifestyle preferences.
* Select the most suitable room from available options.
* Demonstrate different types of intelligent agents.
* Understand the relationship between **sensors, percepts, decision-making, and actuators**.
* Compare Simple Reflex, Goal-Based, and Utility-Based agent architectures.

---

# 🧠 3. Overall Agent-Based Architecture

```text
                         SMART HOSTEL / AIRBNB
                              ENVIRONMENT
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       Room Conditions      User Preferences     Available Rooms
              │                   │                   │
              ▼                   ▼                   ▼
     ┌────────────────┐  ┌──────────────────┐  ┌──────────────────┐
     │  AGENT 1       │  │     AGENT 2      │  │     AGENT 3      │
     │ Room Behavior  │  │    Roommate      │  │  Room Selection  │
     │    Monitor     │  │   Compatibility  │  │      Agent       │
     └───────┬────────┘  └────────┬─────────┘  └────────┬─────────┘
             │                    │                     │
             ▼                    ▼                     ▼
      Simple Reflex          Goal-Based            Utility-Based
             │                    │                     │
             ▼                    ▼                     ▼
       Immediate Action      Goal Satisfaction     Best Utility
             │                    │                     │
             ▼                    ▼                     ▼
         Alerts /             Compatible             Best Room
         Actions              Roommate             Recommendation
```

---

# 👥 4. Agents in the System

| Agent       | Agent Type    | Primary Responsibility     |
| ----------- | ------------- | -------------------------- |
| **Agent 1** | Simple Reflex | Monitor room conditions    |
| **Agent 2** | Goal-Based    | Find a compatible roommate |
| **Agent 3** | Utility-Based | Select the best room       |

---

# 🤖 5. Agent 1 — Room Behavior Monitoring Agent

### Agent Type

**Simple Reflex Agent**

### Purpose

The Room Behavior Monitoring Agent observes the current state of a room and immediately responds to predefined conditions.

It does not maintain a history of previous states or perform long-term planning.

### Architecture

```text
         ROOM ENVIRONMENT
                │
                ▼
       ┌─────────────────┐
       │     Sensors     │
       │                 │
       │ • Noise Level   │
       │ • Light Status  │
       │ • Door Status   │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │   Rule Engine   │
       │                 │
       │ IF condition    │
       │ THEN action     │
       └────────┬────────┘
                │
                ▼
       ┌─────────────────┐
       │    Actuators    │
       │                 │
       │ • Warning       │
       │ • Lock Door     │
       │ • Turn Lights   │
       └─────────────────┘
```

### Inputs / Percepts

* Noise level
* Light status
* Door status
* Occupancy status

### Example Rules

| Percept                 | Rule                          | Action                |
| ----------------------- | ----------------------------- | --------------------- |
| Noise > 60 dB           | High noise detected           | Generate warning      |
| Door = Unlocked         | Security issue                | Lock door / alert     |
| Light = ON + Room Empty | Unnecessary electricity usage | Turn off light        |
| All normal              | No violation                  | Maintain normal state |

### Example

```text
Input:
Noise = 72 dB
Door = Unlocked
Light = ON
Room Occupied = False

Output:
⚠ High Noise Detected
⚠ Door is Unlocked
💡 Room is Empty → Turn Off Lights
```

### Agent Characteristics

* No memory
* Rule-based
* Immediate response
* No planning
* Suitable for simple environmental monitoring

---

# 🤝 6. Agent 2 — Roommate Compatibility Agent

### Agent Type

**Goal-Based Agent**

### Purpose

The Roommate Compatibility Agent searches for a roommate who satisfies the user's desired lifestyle requirements.

Unlike the Simple Reflex Agent, this agent works toward a **specific goal**.

### Goal

> **Find a roommate whose compatibility score satisfies the required threshold.**

For example:

```text
Goal:
Compatibility >= 70%
```

### Architecture

```text
          USER
           │
           ▼
   ┌─────────────────┐
   │ User Preferences│
   │                 │
   │ • Sleep Pattern │
   │ • Cleanliness   │
   │ • Noise         │
   │ • Smoking       │
   │ • Study Habits  │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Candidate        │
   │ Roommates        │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │ Compatibility   │
   │ Evaluation      │
   └────────┬────────┘
            │
            ▼
   ┌─────────────────┐
   │   Goal Check    │
   │                 │
   │ Score >= Goal?  │
   └───────┬─────────┘
           │
      ┌────┴─────┐
      ▼          ▼
     YES         NO
      │           │
      ▼           ▼
 Recommend     Reject /
 Roommate      Check Next
```

### Inputs

#### User Preferences

* Sleep schedule
* Cleanliness preference
* Noise tolerance
* Smoking preference
* Study/work preference

#### Candidate Information

The same attributes are collected for potential roommates.

### Example

**User:**

```text
Sleep: Early
Cleanliness: High
Noise: Low
Smoking: No
Study: Yes
```

**Candidates:**

| Candidate | Compatibility |
| --------- | ------------: |
| Rahul     |           85% |
| Amit      |           62% |
| Jay       |           78% |

With the goal:

```text
Compatibility >= 70%
```

The agent can recommend:

```text
Recommended Roommate: Rahul
Compatibility: 85%
Goal Achieved: YES
```

### Agent Characteristics

* Has a defined goal
* Evaluates possible candidates
* Takes decisions based on goal satisfaction
* Can reject candidates that do not satisfy the goal
* More flexible than a Simple Reflex Agent

---

# 🏡 7. Agent 3 — Room Selection Agent

### Agent Type

**Utility-Based Agent**

### Purpose

The Room Selection Agent chooses the best available room by comparing multiple factors.

Instead of using a single condition, it considers several competing factors and calculates an overall **utility score**.

### Architecture

```text
             AVAILABLE ROOMS
                    │
                    ▼
          ┌──────────────────┐
          │ Room Information │
          │                  │
          │ • Rent           │
          │ • Distance       │
          │ • Facilities     │
          │ • Noise          │
          │ • Compatibility  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Utility Function │
          │                  │
          │ Calculate score  │
          │ for each room    │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Compare Scores   │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Highest Utility  │
          │      Room        │
          └────────┬─────────┘
                   │
                   ▼
             Recommendation
```

### Inputs

* Monthly rent
* Distance from college/work
* Facilities
* Noise level
* Roommate compatibility

### Example Utility Function

Each factor is normalized to a value between `0` and `100`.

```text
Utility =
    0.25 × Affordability
  + 0.15 × Distance
  + 0.20 × Facilities
  + 0.15 × Low Noise
  + 0.25 × Compatibility
```

### Example

| Room     |   Rent | Distance | Facilities | Noise | Compatibility | Utility |
| -------- | -----: | -------: | ---------: | ----: | ------------: | ------: |
| Room 101 | ₹8,000 |     2 km |       8/10 |   Low |           90% |      82 |
| Room 102 | ₹6,500 |     5 km |       7/10 |  High |           70% |      71 |
| Room 103 | ₹9,000 |     1 km |      10/10 |   Low |           80% |  **88** |

### Decision

```text
Room 101 → Utility = 82
Room 102 → Utility = 71
Room 103 → Utility = 88

Best Room → Room 103
```

### Agent Characteristics

* Evaluates multiple alternatives
* Uses preferences/weights
* Calculates utility
* Selects the highest-value option
* Suitable when several factors influence the decision

---

# 🔄 8. Comparison of the Three Agents

| Feature        | Agent 1          | Agent 2                 | Agent 3             |
| -------------- | ---------------- | ----------------------- | ------------------- |
| Name           | Behavior Monitor | Roommate Matcher        | Room Selector       |
| Type           | Simple Reflex    | Goal-Based              | Utility-Based       |
| Memory         | ❌                | Optional                | Optional            |
| Planning       | ❌                | ✅                       | ✅                   |
| Decision Basis | Rules            | Goal                    | Utility             |
| Main Input     | Room state       | Lifestyle preferences   | Room attributes     |
| Output         | Action/Alert     | Roommate recommendation | Room recommendation |
| Complexity     | Low              | Medium                  | Medium              |

---

# 👨‍💻 9. Division of Work

The case study is divided equally among three team members.

### Member 1 — Simple Reflex Agent

**Agent:** Room Behavior Monitoring Agent

**Responsible for:**

* Taking room-condition inputs
* Implementing condition-action rules
* Detecting violations
* Generating appropriate actions/alerts
* Demonstrating Simple Reflex architecture

**Expected implementation:**

```text
Input → Rules → Action
```

---

### Member 2 — Goal-Based Agent

**Agent:** Roommate Compatibility Agent

**Responsible for:**

* Taking user preferences
* Maintaining candidate roommate profiles
* Calculating compatibility
* Defining compatibility goal
* Selecting a candidate who satisfies the goal
* Demonstrating Goal-Based architecture

**Expected implementation:**

```text
Preferences → Candidate Evaluation → Goal Check → Recommendation
```

---

### Member 3 — Utility-Based Agent

**Agent:** Room Selection Agent

**Responsible for:**

* Taking available room information
* Normalizing room attributes
* Assigning weights
* Calculating utility scores
* Comparing rooms
* Recommending the highest-utility room
* Demonstrating Utility-Based architecture

**Expected implementation:**

```text
Room Data → Utility Calculation → Score Comparison → Best Room
```

---

# 🧩 10. PEAS Representation

PEAS stands for:

* **P — Performance Measure**
* **E — Environment**
* **A — Actuators**
* **S — Sensors**

## Agent 1 — Room Behavior Monitoring

| Component       | Description                          |
| --------------- | ------------------------------------ |
| **Performance** | Safety, low noise, energy efficiency |
| **Environment** | Hostel/Airbnb room                   |
| **Actuators**   | Warning, lock door, turn off lights  |
| **Sensors**     | Noise, light, door, occupancy        |

## Agent 2 — Roommate Compatibility

| Component       | Description                                 |
| --------------- | ------------------------------------------- |
| **Performance** | Compatibility and user satisfaction         |
| **Environment** | Available roommate candidates               |
| **Actuators**   | Recommend roommate                          |
| **Sensors**     | Lifestyle preferences and roommate profiles |

## Agent 3 — Room Selection

| Component       | Description                                      |
| --------------- | ------------------------------------------------ |
| **Performance** | Cost, comfort, convenience                       |
| **Environment** | Available rooms                                  |
| **Actuators**   | Recommend best room                              |
| **Sensors**     | Rent, distance, facilities, noise, compatibility |

---

# 📊 11. Example System Scenario

Consider a student looking for hostel accommodation.

### Step 1 — Room Monitoring

The Behavior Monitoring Agent detects:

```text
Noise = 68 dB
Door = Unlocked
Room = Occupied
```

Output:

```text
⚠ Noise exceeds permitted level.
⚠ Door is unlocked.
```

---

### Step 2 — Roommate Matching

The student specifies:

```text
Sleep: Early
Noise: Low
Cleanliness: High
Smoking: No
```

The Goal-Based Agent evaluates available candidates.

```text
Candidate A → 55%
Candidate B → 82%
Candidate C → 64%
```

Goal:

```text
Compatibility >= 70%
```

Output:

```text
Recommended Roommate: Candidate B
Compatibility: 82%
```

---

### Step 3 — Room Selection

The Utility-Based Agent evaluates available rooms.

```text
Room 101 → 78 Utility
Room 102 → 84 Utility
Room 103 → 72 Utility
```

Output:

```text
Recommended Room: Room 102
Utility Score: 84
```

---

# 🔗 12. Relationship Between Agents

The agents are implemented independently but conceptually work together.

```text
             USER / HOSTEL ENVIRONMENT
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
  Room State      User Preferences   Room Data
       │               │                │
       ▼               ▼                ▼
  ┌─────────┐     ┌─────────┐     ┌─────────┐
  │ Agent 1 │     │ Agent 2 │     │ Agent 3 │
  │ Simple  │     │  Goal   │     │ Utility │
  │ Reflex  │     │  Based  │     │  Based  │
  └────┬────┘     └────┬────┘     └────┬────┘
       │               │                │
       ▼               ▼                ▼
    Alerts        Roommate Match     Best Room
```

The project does **not require a centralized controller or database**, since the primary objective is to demonstrate different intelligent-agent architectures.

---

# 🛠️ 13. Technology Stack

The agents can be implemented using basic programming tools.

### Recommended

* **Language:** Python 3
* **Input:** Console / predefined datasets
* **Libraries:** Python standard library
* **Output:** Console-based recommendations and alerts

No machine learning model or external API is required.

---

# 📁 14. Suggested Repository Structure

```text
smart-hostel-airbnb-agents/
│
├── README.md
│
├── agent_1_behavior_monitor/
│   └── behavior_monitor.py
│
├── agent_2_roommate_matching/
│   └── roommate_matching.py
│
├── agent_3_room_selection/
│   └── room_selection.py
│
└── requirements.txt
```

Since the project uses basic Python functionality, `requirements.txt` may remain empty if no external packages are used.

---

# 🚀 15. Expected Output

The final system demonstrates three different forms of intelligent decision-making:

```text
Agent 1:
Room conditions
      ↓
Rules
      ↓
Immediate Action

Agent 2:
User preferences
      ↓
Candidate evaluation
      ↓
Goal satisfaction
      ↓
Compatible roommate

Agent 3:
Room alternatives
      ↓
Utility calculation
      ↓
Comparison
      ↓
Best room
```

---

# 📚 16. Key AI Concepts Demonstrated

* Intelligent Agents
* Agent Environment
* Sensors and Actuators
* Percepts and Actions
* Simple Reflex Agents
* Goal-Based Agents
* Utility-Based Agents
* Rule-Based Decision Making
* Goal Satisfaction
* Utility Functions
* Decision Making under Multiple Criteria
* PEAS Framework

---

# ✅ 17. Conclusion

The **Smart Hostel / Airbnb Roommate Management System** demonstrates how different intelligent-agent architectures can be applied to everyday accommodation problems.

The three agents solve different types of problems:

> **Simple Reflex Agent → "What should I do right now?"**

> **Goal-Based Agent → "What do I need to achieve?"**

> **Utility-Based Agent → "Which option gives me the best overall result?"**

By implementing these three agents independently, the case study provides a simple but practical demonstration of how AI agents perceive their environment, make decisions, and take actions.

---

## 👥 Team Contribution

| Member   | Contribution             | Agent Architecture |
| -------- | ------------------------ | ------------------ |
| Member 1 | Room Behavior Monitoring | Simple Reflex      |
| Member 2 | Roommate Compatibility   | Goal-Based         |
| Member 3 | Room Selection           | Utility-Based      |

---

## ⭐ Summary

**Smart Hostel / Airbnb Roommate Management System**

```text
┌─────────────────────────────────────────────────┐
│          SMART HOSTEL / AIRBNB SYSTEM           │
├─────────────────┬────────────────┬──────────────┤
│ Behavior        │ Roommate       │ Room         │
│ Monitoring      │ Matching       │ Selection    │
├─────────────────┼────────────────┼──────────────┤
│ Simple Reflex   │ Goal-Based     │ Utility-Based│
├─────────────────┼────────────────┼──────────────┤
│ Rules           │ Goals          │ Utility      │
│ ↓               │ ↓              │ ↓            │
│ Immediate       │ Goal           │ Best Overall │
│ Action          │ Satisfaction   │ Choice       │
└─────────────────┴────────────────┴──────────────┘
```
