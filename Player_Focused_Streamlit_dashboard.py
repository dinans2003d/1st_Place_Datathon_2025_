import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------
# CONFIG
# ---------------------------------------------
MIN_MATCHES = 10  # filter only players with ≥ X matches

st.set_page_config(
    page_title="Clash Royale Player Dashboard",
    layout="wide"
)


# ---------------------------------------------
# LOAD DATA
# ---------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "clash_retention_sampled_100k.csv",
        parse_dates=["battleTime", "next_battleTime"],
        low_memory=False
    )

    df = df.sort_values(["playerId", "battleTime"]).reset_index(drop=True)

    # Convert hour if needed
    if df["hour"].dtype == object:
        df["hour"] = pd.to_numeric(df["hour"], errors="coerce")

    return df


df = load_data()


# ---------------------------------------------
# FILTER TO ACTIVE PLAYERS ONLY
# ---------------------------------------------
df["match_count"] = df.groupby("playerId")["battleTime"].transform("count")
df = df[df["match_count"] >= MIN_MATCHES].copy()

if df.empty:
    st.error(f"No players have ≥ {MIN_MATCHES} matches. Lower MIN_MATCHES.")
    st.stop()


# ---------------------------------------------
# COHORT-LEVEL KPIs (for comparison)
# ---------------------------------------------
cohort_total_matches = len(df)
cohort_win_rate = df["result"].mean() * 100  # result is 1/0

cohort_hours = df["hours_until_next"].dropna()
if not cohort_hours.empty:
    cohort_fast_return_rate = (cohort_hours < 1).mean() * 100
    cohort_avg_gap_hours = cohort_hours.mean()
else:
    cohort_fast_return_rate = np.nan
    cohort_avg_gap_hours = np.nan

cohort_avg_trophy_change = df["TrophyChange"].mean()


# ---------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------
st.sidebar.header("Filters")

n_players = df["playerId"].nunique()
st.sidebar.caption(
    f"Players with ≥ {MIN_MATCHES} matches: **{n_players:,}**"
)

players = np.sort(df["playerId"].dropna().unique())

selected_player = st.sidebar.selectbox(
    "Player ID",
    options=players,
    index=0
)

player_df = df[df["playerId"] == selected_player].copy()

if player_df.empty:
    st.error("No matches found for this player.")
    st.stop()


# ---------------------------------------------
# PAGE HEADER
# ---------------------------------------------
st.title(f"Clash Royale Player Dashboard – {selected_player}")

# Team Name (clean subtle branding)
st.markdown(
    "<p style='color:#485465; font-size:18px; margin-top:-15px;'>"
    "SheetWorks Solutions"
    "</p>",
    unsafe_allow_html=True
)

st.caption(
    "Match history, win/loss performance, and return behavior for a single high-activity player."
)
with st.expander("Raw match data for this player"):
    st.dataframe(player_df.head(50))


# ---------------------------------------------
# PLAYER KPIs
# ---------------------------------------------
total_matches = len(player_df)
wins = int(player_df["result"].sum())
losses = total_matches - wins
win_rate = (wins / total_matches * 100) if total_matches > 0 else 0.0

# Use hours_until_next directly (sanity-checked)
player_hours = player_df["hours_until_next"].dropna()

if not player_hours.empty:
    fast_return_rate = (player_hours < 1).mean() * 100
    avg_gap_hours = player_hours.mean()
else:
    fast_return_rate = np.nan
    avg_gap_hours = np.nan

trophy_net = int(player_df["TrophyChange"].sum())
avg_trophy_change = player_df["TrophyChange"].mean() if total_matches > 0 else 0.0

longest_win_streak = int(player_df["win_streak"].max()) if "win_streak" in player_df.columns else 0
longest_loss_streak = int(player_df["loss_streak"].max()) if "loss_streak" in player_df.columns else 0


# ---------------------------------------------
# PLAYER SUMMARY KPIs
# ---------------------------------------------
st.subheader("Player Summary")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Matches", f"{total_matches}")
c2.metric("Win Rate", f"{win_rate:.1f}%")
c3.metric("Fast Return Rate (<1 hr)", "N/A" if np.isnan(fast_return_rate) else f"{fast_return_rate:.1f}%")
c4.metric("Net Trophy Change", f"{trophy_net:+d}")
c5.metric("Avg Trophy Change / Match", f"{avg_trophy_change:+.1f}")


# ---------------------------------------------
# PLAYER VS COHORT KPIs
# ---------------------------------------------
st.subheader("How does this player compare to similar players?")

vc1, vc2, vc3 = st.columns(3)

# Win rate vs cohort (pp = percentage-points)
delta_win_pp = win_rate - cohort_win_rate
vc1.metric(
    "Win Rate vs Cohort",
    f"{win_rate:.1f}%",
    f"{delta_win_pp:+.1f} pp"
)

# Fast return rate vs cohort
if not np.isnan(fast_return_rate) and not np.isnan(cohort_fast_return_rate):
    delta_fast_pp = fast_return_rate - cohort_fast_return_rate
    vc2.metric(
        "Fast Return Rate (<1 hr) vs Cohort",
        f"{fast_return_rate:.1f}%",
        f"{delta_fast_pp:+.1f} pp"
    )
else:
    vc2.metric("Fast Return Rate (<1 hr) vs Cohort", "N/A", "–")

# Avg return time vs cohort (lower is better, so negative delta is good)
if not np.isnan(avg_gap_hours) and not np.isnan(cohort_avg_gap_hours):
    delta_gap = avg_gap_hours - cohort_avg_gap_hours
    vc3.metric(
        "Avg Return Time vs Cohort",
        f"{avg_gap_hours:.2f} hrs",
        f"{delta_gap:+.2f} hrs"
    )
else:
    vc3.metric("Avg Return Time vs Cohort", "N/A", "–")


# ---------------------------------------------
# TROPHY PROGRESSION CHART
# ---------------------------------------------
st.subheader("Trophy Progression Over Time")

player_plot_df = player_df.sort_values("battleTime").copy()
player_plot_df["result_label"] = player_plot_df["result"].map({0: "Loss", 1: "Win"})

fig = px.line(
    player_plot_df,
    x="battleTime",
    y="StartingTrophies",
    color="result_label",
    markers=True,
    labels={
        "battleTime": "Match Time",
        "StartingTrophies": "Starting Trophies",
        "result_label": "Result"
    },
    color_discrete_map={
        "Win": "#2149A7",   # blue
        "Loss": "#E9C455"   # yellow
    }
)

st.plotly_chart(fig, use_container_width=True)
