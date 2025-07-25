import streamlit as st
import time
from datetime import datetime

# Mock functions - replace these with your actual implementations
def get_upcoming_matches():
    """
    Mock function to simulate getting upcoming matches.
    Replace this with your actual API call or data source.
    """
    # Simulate API delay
    time.sleep(0.5)
    
    return [
        {
            "team_a": "Manchester United",
            "team_b": "Liverpool",
            "date": "2025-07-26",
            "fixture_id": 12345
        },
        {
            "team_a": "Arsenal",
            "team_b": "Chelsea",
            "date": "2025-07-27",
            "fixture_id": 12346
        },
        {
            "team_a": "Manchester City",
            "team_b": "Tottenham",
            "date": "2025-07-28",
            "fixture_id": 12347
        },
        {
            "team_a": "Newcastle",
            "team_b": "Brighton",
            "date": "2025-07-29",
            "fixture_id": 12348
        },
        {
            "team_a": "West Ham",
            "team_b": "Everton",
            "date": "2025-07-30",
            "fixture_id": 12349
        }
    ]

def run_prediction(match_data):
    """
    Mock function to simulate running prediction.
    Replace this with your actual prediction model.
    """
    # Simulate prediction processing time
    time.sleep(2)
    
    # Mock prediction result
    prediction_result = {
        "predicted_winner": match_data["team_a"],
        "confidence": 78.5,
        "score_prediction": f"{match_data['team_a']} 2-1 {match_data['team_b']}",
        "key_factors": [
            "Home advantage",
            "Recent form favors Team A",
            "Head-to-head record",
            "Player availability"
        ],
        "win_probability": {
            match_data["team_a"]: 65.2,
            "Draw": 22.1,
            match_data["team_b"]: 12.7
        }
    }
    
    return prediction_result

# Page configuration
st.set_page_config(
    page_title="⚽ Football Match Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .match-card {
        background-color: #f0f2f6;
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .match-card:hover {
        border-color: #ff6b6b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .team-vs {
        font-size: 1.2em;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin: 10px 0;
    }
    .match-date {
        color: #7f8c8d;
        text-align: center;
        font-size: 0.9em;
    }
    .prediction-result {
        background-color: #e8f5e8;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stButton > button {
        width: 100%;
        background-color: #ff6b6b;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff5252;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'selected_match' not in st.session_state:
    st.session_state.selected_match = None
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None
if 'matches_loaded' not in st.session_state:
    st.session_state.matches_loaded = False

# Main title
st.title("⚽ Football Match Predictor")
st.markdown("---")

# Load matches on first run
if not st.session_state.matches_loaded:
    with st.spinner("Loading upcoming matches..."):
        st.session_state.matches = get_upcoming_matches()
        st.session_state.matches_loaded = True

# Header with refresh button
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 📅 Upcoming Matches")
with col2:
    if st.button("🔄 Refresh Matches", key="refresh_btn"):
        with st.spinner("Refreshing matches..."):
            st.session_state.matches = get_upcoming_matches()
            st.session_state.selected_match = None
            st.session_state.prediction_result = None
        st.success("Matches refreshed!")

# Display matches
if st.session_state.matches:
    st.markdown("**Select a match to predict the result:**")
    
    # Create columns for match display
    for i, match in enumerate(st.session_state.matches):
        with st.container():
            # Format date
            match_date = datetime.strptime(match["date"], "%Y-%m-%d").strftime("%B %d, %Y")
            
            # Create match card
            st.markdown(f"""
            <div class="match-card">
                <div class="team-vs">{match["team_a"]} vs {match["team_b"]}</div>
                <div class="match-date">📅 {match_date}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Selection button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"Select & Predict", key=f"select_{i}"):
                    st.session_state.selected_match = match
                    st.session_state.prediction_result = None

# Show selected match and prediction
if st.session_state.selected_match:
    st.markdown("---")
    st.markdown("### 🎯 Selected Match")
    
    selected = st.session_state.selected_match
    match_date = datetime.strptime(selected["date"], "%Y-%m-%d").strftime("%B %d, %Y")
    
    st.markdown(f"""
    <div class="prediction-result">
        <h4 style="margin-top: 0;">⚽ {selected["team_a"]} vs {selected["team_b"]}</h4>
        <p><strong>Date:</strong> {match_date}</p>
        <p><strong>Fixture ID:</strong> {selected["fixture_id"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔮 Predict Result", key="predict_btn"):
            with st.spinner("🤖 Running prediction model..."):
                st.session_state.prediction_result = run_prediction(selected)

# Display prediction result
if st.session_state.prediction_result:
    st.markdown("---")
    st.markdown("### 📊 Prediction Result")
    
    result = st.session_state.prediction_result
    
    # Main prediction
    st.markdown(f"""
    <div class="prediction-result">
        <h4 style="margin-top: 0;">🏆 Predicted Winner: {result["predicted_winner"]}</h4>
        <p><strong>📈 Confidence:</strong> {result["confidence"]}%</p>
        <p><strong>⚽ Score Prediction:</strong> {result["score_prediction"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Win probabilities
    with st.expander("📊 Win Probabilities", expanded=True):
        for team, probability in result["win_probability"].items():
            st.progress(probability / 100, text=f"{team}: {probability}%")
    
    # Key factors
    with st.expander("🔍 Key Factors", expanded=False):
        for factor in result["key_factors"]:
            st.markdown(f"• {factor}")
    
    # Additional details in expandable section
    with st.expander("📋 Detailed Analysis", expanded=False):
        st.markdown(f"""
        **Match Details:**
        - **Teams:** {st.session_state.selected_match["team_a"]} vs {st.session_state.selected_match["team_b"]}
        - **Date:** {st.session_state.selected_match["date"]}
        - **Fixture ID:** {st.session_state.selected_match["fixture_id"]}
        
        **Prediction Summary:**
        - **Most Likely Outcome:** {result["predicted_winner"]} victory
        - **Confidence Level:** {result["confidence"]}% (High confidence)
        - **Expected Score:** {result["score_prediction"]}
        
        *Note: This prediction is based on historical data, current form, and statistical analysis. Actual results may vary.*
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
    ⚽ Football Match Predictor | Powered by AI & Statistics
</div>
""", unsafe_allow_html=True)
