"""
ISRO Aerospace Dark Scientific Theme CSS for Streamlit Dashboard.
SIH26166 Compliant.
"""

ISRO_THEME_CSS = """
<style>
/* Global Dark Theme */
.stApp {
    background-color: #0B0E14;
    color: #E2E8F0;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
}

/* Header Banner */
.isro-header {
    background: linear-gradient(135deg, #0d1527 0%, #06101e 100%);
    border-bottom: 2px solid #00E5FF;
    padding: 1.2rem 1.8rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0, 229, 255, 0.15);
}

.isro-title {
    color: #00E5FF;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.isro-subtitle {
    color: #94A3B8;
    font-size: 0.95rem;
    margin-top: 4px;
    font-weight: 400;
}

/* Telemetry Card */
.metric-card {
    background: #0E1420;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.4);
    transition: border-color 0.2s;
}

.metric-card:hover {
    border-color: #00E5FF;
}

.metric-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    color: #94A3B8;
    letter-spacing: 1px;
    font-weight: 600;
}

.metric-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #F8FAFC;
    margin: 4px 0;
    font-family: 'Consolas', 'Courier New', monospace;
}

.metric-badge-success {
    color: #1DE9B6;
    font-size: 0.8rem;
    font-weight: 600;
}

.metric-badge-caution {
    color: #FF9100;
    font-size: 0.8rem;
    font-weight: 600;
}

.metric-badge-error {
    color: #FF5252;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Mission Provenance Tag */
.tag-verified {
    display: inline-block;
    background: rgba(29, 233, 182, 0.15);
    color: #1DE9B6;
    border: 1px solid #1DE9B6;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.tag-derived {
    display: inline-block;
    background: rgba(255, 145, 0, 0.15);
    color: #FF9100;
    border: 1px solid #FF9100;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Section Box */
.section-box {
    background: #0E1420;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
}

.section-title {
    color: #00E5FF;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
    border-left: 3px solid #00E5FF;
    padding-left: 8px;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #070A10;
    border-right: 1px solid #1E293B;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #00B4D8 0%, #0077B6 100%);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 0.6rem 1.2rem;
    width: 100%;
    transition: transform 0.1s, box-shadow 0.2s;
}

.stButton>button:hover {
    box-shadow: 0 4px 15px rgba(0, 180, 216, 0.4);
    transform: translateY(-1px);
}
</style>
"""
