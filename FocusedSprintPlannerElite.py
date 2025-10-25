import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Focus Sprint Planner · Elite",
    page_icon="🏆",
    layout="wide",
)

########################################
# ACCESS GATE (unique code per buyer)
########################################
VALID_KEYS = {
    "GX7R-PL9F-23KQ": {"active": True,  "note": "Gumroad buyer #1"},
    "M11A-B82C-Z5Q9": {"active": True,  "note": "VIP early supporter"},
    "TEST-TEST-TEST": {"active": False, "note": "Refunded / revoked"},
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "license_code" not in st.session_state:
    st.session_state.license_code = None

def login_screen():
    st.title("Focus Sprint Planner · Elite 🏆")
    st.caption("Exclusive version ($7). Enter your personal access code.")

    code_input = st.text_input(
        "Your access code:",
        placeholder="GX7R-PL9F-23KQ"
    )
    unlock_clicked = st.button("Unlock Elite")

    if unlock_clicked:
        entered = code_input.strip()
        if entered in VALID_KEYS:
            info = VALID_KEYS[entered]
            if info.get("active", False):
                st.session_state.authenticated = True
                st.session_state.license_code = entered
                st.success("Elite access granted. Let's work.")
            else:
                st.error("This code is no longer active. Contact support.")
        else:
            st.error("Invalid code. Please check your purchase email.")

    if not st.session_state.authenticated:
        st.stop()

login_screen()

########################################
# SESSION / STATE SETUP
########################################
# sprint counter
if "sprint_count_today" not in st.session_state:
    st.session_state.sprint_count_today = 1  # first sprint

# tone choice
if "tone_choice" not in st.session_state:
    st.session_state.tone_choice = "Confident and direct"

# reset form flag (used after "Plan Another Sprint")
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# default values for the form inputs we control
default_values = {
    "task_input": "",
    "reason_input": "",
    "s1": "",
    "s2": "",
    "s3": "",
    "intensity_input": "Focused",
    "start_in": "Right now",
    "reward_input": "",
}

# if user just clicked "Plan Another Sprint", wipe the form values before rendering widgets
if st.session_state.reset_form:
    for k, v in default_values.items():
        st.session_state[k] = v
    st.session_state.reset_form = False  # clear the flag

########################################
# PLACEHOLDER WEEKLY STATS
########################################
fake_total_sprints_this_week = 7        # showcase only (no persistence yet)
fake_total_minutes_this_week = 7 * 25   # 175 min
fake_biggest_blocker = "Perfectionism before starting."

########################################
# SIDEBAR
########################################
with st.sidebar:
    st.header("Your Elite Dashboard")

    st.caption("License code:")
    st.code(st.session_state.license_code or "—")

    st.caption("Your Focus Scoreboard (this week so far)")
    st.metric("Deep Work Sprints", f"{fake_total_sprints_this_week}")
    st.metric("Focused Minutes", f"{fake_total_minutes_this_week}")
    st.write("Most common blocker:")
    st.write(f"“{fake_biggest_blocker}”")

    st.divider()

    st.subheader("Today's Energy")
    st.session_state.tone_choice = st.radio(
        "Pick how you're showing up:",
        [
            "Calm and steady",
            "Confident and direct",
            "No excuses / I'm done negotiating"
        ],
        index=[
            "Calm and steady",
            "Confident and direct",
            "No excuses / I'm done negotiating"
        ].index(st.session_state.tone_choice),
        key="tone_choice_radio"
    )

    st.info(f"Locked in: {st.session_state.tone_choice}")

    st.divider()

    st.write(f"Sprint you're setting up now: #{st.session_state.sprint_count_today} today")
    st.caption("You can plan Sprint #2, #3, etc. without leaving the app.")

########################################
# MAIN CONTENT
########################################
st.header("Your Elite Sprint Plan")
st.caption("You're not allowed to spiral. You're here to ship proof.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Non-Negotiable Outcome")
    task = st.text_area(
        "By the end of this sprint, what must exist?",
        placeholder="Example: Send pricing update to client X and unblock approval.",
        height=100,
        key="task_input"
    )

    st.subheader("2. Why This Matters (to Future You)")
    reason = st.text_area(
        "If you dodge this again, what happens?",
        placeholder="Example: Approval slips. I look slow. This keeps renting space in my head.",
        height=80,
        key="reason_input"
    )

with col2:
    st.subheader("3. Exact Battle Plan (~25 min)")
    step1 = st.text_input(
        "Step 1 (0–5 min):",
        placeholder="Open draft. Paste template.",
        key="s1"
    )
    step2 = st.text_input(
        "Step 2 (5–15 min):",
        placeholder="Write ugly bullet points fast.",
        key="s2"
    )
    step3 = st.text_input(
        "Step 3 (15–25 min):",
        placeholder="Polish, send, close tab. Log it as DONE.",
        key="s3"
    )

    st.subheader("How are you showing up?")
    intensity = st.select_slider(
        "Pick your commitment level:",
        options=["Calm", "Focused", "No excuses", "I refuse to fail"],
        value=st.session_state.get("intensity_input", "Focused"),
        key="intensity_input"
    )

colA, colB = st.columns(2)

with colA:
    start_in = st.selectbox(
        "When do you start?",
        ["Right now", "In 5 min", "In 10 min", "In 30 min"],
        index=["Right now", "In 5 min", "In 10 min", "In 30 min"].index(
            st.session_state.get("start_in", "Right now")
        ),
        key="start_in"
    )

with colB:
    reward = st.text_input(
        "Your reward after you finish:",
        placeholder="Tea. Music. Walk. Text someone 'sent.'",
        key="reward_input"
    )

st.markdown("---")

st.subheader("End-of-day Accountability Check-In")
reflection_question = "What did I actually ship that proves I moved forward today?"
st.code(reflection_question)
st.caption("You don't get to say 'I was busy.' You answer with outcomes only.")

st.markdown("---")

########################################
# SUMMARY / COMMITMENT BLOCK
########################################
summary = f"""
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]

SPRINT #{st.session_state.sprint_count_today} TODAY

NON-NEGOTIABLE OUTCOME:
{task or '[not filled]'}

WHY THIS MATTERS:
{reason or '[not filled]'}

BATTLE PLAN:
1. {step1 or '[not filled]'}
2. {step2 or '[not filled]'}
3. {step3 or '[not filled]'}

INTENSITY: {intensity}
START: {start_in}
REWARD: {reward or '[not filled]'}

YOUR ENERGY TODAY:
{st.session_state.tone_choice}

END-OF-DAY QUESTION:
{reflection_question}
"""

st.subheader("Your Elite Commitment")
st.code(summary.strip())

########################################
# EXPORT / SHARE BLOCK
########################################
st.download_button(
    label="Download this sprint as .txt",
    data=summary.strip(),
    file_name=f"elite_sprint_{st.session_state.sprint_count_today}.txt",
    mime="text/plain"
)

st.success("This is your contract with yourself. Send it to someone who will actually call you out.")

########################################
# NEW SPRINT BUTTON
########################################
st.markdown("---")
if st.button("Plan Another Sprint"):
    # increase sprint count
    st.session_state.sprint_count_today += 1

    # set flag so next rerun clears all inputs
    st.session_state.reset_form = True

    st.info(f"Okay. Setting up Sprint #{st.session_state.sprint_count_today} now.")
    st.rerun()

st.caption("Elite is for people who are done negotiating with themselves.")
