# Staying in the Ladder: What Drives Player Retention?
**1st Place – Datathon 2025**

## Project Impact
I analyzed player behavior in *Clash Royale* to identify **when and why players churn**, focusing on retention as the primary revenue driver in free-to-play games. Even a **1–2% improvement in retention** can translate into **millions of additional matches, purchases, and active users**. This project delivers **product-ready insights** that Supercell could use to intervene at the exact moments players are most likely to quit.

## Business Scenario
Supercell’s ladder system is the core engagement loop in Clash Royale. Players climb trophies, experience wins and losses, and decide whether to continue playing or disengage. The problem is that **player frustration is predictable but unmanaged**, leading to avoidable churn—especially in **high-volume Challenger Leagues**, where most players compete.

## Objective
Determine how **losses, momentum, and return timing** influence player retention and identify **where Supercell can intervene early** to prevent churn before it happens.

## Data & Feature Engineering
I transformed a **16.8M-row raw dataset (74 columns)** into a focused **1.9M-row analytical dataset (28 columns)** optimized for retention analysis. I engineered features around:
- Match outcomes and win/loss streaks  
- Return timing buckets and rapid-return behavior  
- Momentum (climb vs drop)  
- Session context (time of day, weekday vs weekend)  
- Arena segmentation, centered on Challenger Leagues  

## Behavioral Framework
I introduced a custom metric called **Behavioral Tilt**, which measures how players respond after losing a match. Behavioral Tilt captures whether a player **returns to play or stops entirely**, allowing frustration and churn risk to be quantified rather than inferred from descriptive statistics alone.

## Analysis & Modeling
Key findings from the analysis:
- Players are far more likely to return after a **win (62.9%)** than after a **loss (36.7%)**
- **Highest churn risk occurs after the first 1–3 losses**, not during long losing streaks
- Once players fall into **long return-time buckets**, churn probability spikes sharply
- Early consecutive losses are the strongest driver of emotional, rapid-return gameplay

These patterns were validated using a **predictive behavioral model (~90% accuracy)** and surfaced through an **interactive Streamlit dashboard** for stakeholder exploration.

## Key Insights
- Early losses are the most dangerous churn trigger  
- Long losing streaks matter less than initial frustration  
- Rapid-return behavior signals emotional tilt and retention risk  
- Timing interventions is more effective than broad incentives  

## Recommendations
1. **Reduce early frustration (1–3 losses)**  
   Introduce light loss protection or easier matchmaking immediately after early losses.

2. **Support long losing streaks (7–10 losses)**  
   Use cooldown prompts or small rewards to prevent disengagement once players mentally check out.

3. **Skill-based matchmaking in lower arenas**  
   Apply model-driven difficulty adjustments to protect retention without compromising competitiveness.

## Outcome
This project demonstrates how **behavioral analytics can directly inform product and game design decisions**. I translated large-scale gameplay data into **actionable retention strategies**, showcasing end-to-end ownership from raw data to executive-level recommendations.
