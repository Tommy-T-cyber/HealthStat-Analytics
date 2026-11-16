import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from pathlib import Path

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="HealthStat Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. PROJECT PATHS
# =====================================================

PROJECT_FOLDER = Path(__file__).parent
DATA_PATH = PROJECT_FOLDER / "data" / "health_data_clean.csv"
OUTPUT_PATH = PROJECT_FOLDER / "outputs"

# =====================================================
# 3. THEME AND COLOUR PALETTE
# =====================================================

COLORS = {
    "navy": "#12304A",
    "teal": "#087F8C",
    "aqua": "#27B7A5",
    "light": "#F3F7FA",
    "amber": "#F2A541",
    "purple": "#8064D8",
    "coral": "#E36B7B",
    "muted": "#64748B",
    "grid": "#E7EDF2",
    "white": "#FFFFFF"
}

DIAGNOSIS_COLORS = {
    "Hypertension": COLORS["navy"],
    "Diabetes": COLORS["teal"],
    "Heart Disease": COLORS["amber"],
    "Asthma": COLORS["purple"],
    "Obesity": COLORS["coral"]
}

pio.templates.default = "plotly_white"

# =====================================================
# 4. CUSTOM CSS
# =====================================================

st.markdown("""
<style>
/* ===== GLOBAL LIGHT THEME AND TEXT CONTRAST ===== */
:root {
    color-scheme: light;
}
html, body, [class*="css"], .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background-color: #F2F6FA !important;
    color: #243447 !important;
    font-family: "Segoe UI", Arial, sans-serif;
}
.block-container {
    max-width: 1500px;
    padding: 2rem 2.4rem 3rem 2.4rem;
}

/* Force readable text throughout the app */
.stMarkdown, .stMarkdown p, .stMarkdown span,
.stMarkdown li, .stText, .stCaption, .stAlert,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
label, legend, small {
    color: #334155 !important;
}
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
[data-testid="stHeader"] {
    color: #102A43 !important;
    font-weight: 700 !important;
}
h1 { font-size: 2.25rem !important; letter-spacing: -0.6px; }
h2 { font-size: 1.6rem !important; }
h3, h4 { color: #087F8C !important; }

/* Sidebar */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background: #FFFFFF !important;
}
[data-testid="stSidebar"] {
    border-right: 1px solid #DCE5ED;
}
[data-testid="stSidebar"] * {
    color: #263B50 !important;
}
[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #F2F8FA !important;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE5ED !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    box-shadow: 0 5px 18px rgba(16, 42, 67, 0.07) !important;
}
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #12304A !important;
}
[data-testid="stMetricValue"] {
    font-weight: 750 !important;
}
[data-testid="stMetricLabel"] {
    color: #087F8C !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #40566B !important;
    font-weight: 650 !important;
    background: transparent !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #087F8C !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #087F8C !important;
}

/* Select boxes and other inputs */
div[data-baseweb="select"] > div,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stDateInput"] input {
    background: #FFFFFF !important;
    color: #243447 !important;
    border-color: #C9D5E0 !important;
}
div[data-baseweb="select"] *,
[data-testid="stSelectbox"] *,
[data-testid="stMultiSelect"] * {
    color: #243447 !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background: #087F8C !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 9px !important;
    font-weight: 650 !important;
    padding: 0.55rem 1rem !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #066873 !important;
    color: #FFFFFF !important;
}

/* Tables */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE5ED !important;
    border-radius: 12px !important;
}
[data-testid="stDataFrame"] * {
    color: #243447 !important;
}

/* Alerts, separators, footer */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}
hr {
    border-color: #DCE5ED !important;
    margin: 1.5rem 0 !important;
}
footer, #MainMenu {
    visibility: hidden;
}

/* Smaller screens */
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 2rem 1rem; }
    h1 { font-size: 1.75rem !important; }
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 5. DATA LOADING
# =====================================================

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}\n"
            "Check that health_data_clean.csv is inside the data folder."
        )

    data = pd.read_csv(DATA_PATH)

    if "Last Visit" in data.columns:
        data["Last Visit"] = pd.to_datetime(
            data["Last Visit"],
            dayfirst=True,
            errors="coerce"
        )

    return data


@st.cache_data
def load_table(filename):
    file_path = OUTPUT_PATH / filename
    if file_path.exists():
        return pd.read_csv(file_path, index_col=0)
    return None


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.stop()

descriptive_summary = load_table("descriptive_statistics.csv")
quality_report = load_table("data_quality_report.csv")
correlation_matrix = load_table("correlation_matrix.csv")

# =====================================================
# 6. REUSABLE CHART FORMATTING
# =====================================================

def polish_chart(fig, height=390):
    """Apply consistent styling to Plotly charts."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        font=dict(
            family="Segoe UI, Arial, sans-serif",
            color=COLORS["navy"],
            size=12
        ),
        title=dict(
            font=dict(size=17, color=COLORS["navy"]),
            x=0.02,
            xanchor="left"
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.75)",
            borderwidth=0
        ),
        margin=dict(l=35, r=25, t=65, b=45),
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color=COLORS["navy"]
        )
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"]
    )
    fig.update_yaxes(
        gridcolor=COLORS["grid"],
        linecolor=COLORS["grid"],
        zerolinecolor=COLORS["grid"]
    )
    return fig


def show_chart(fig, height=390):
    fig = polish_chart(fig, height=height)
    st.plotly_chart(fig, use_container_width=True)


# =====================================================
# 7. DASHBOARD HEADER
# =====================================================

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        "<div style='color:#087F8C; font-size:0.78rem; "
        "font-weight:700; letter-spacing:2px; text-transform:uppercase;'>"
        "STATISTICAL THINKING IN DATA SCIENCE</div>",
        unsafe_allow_html=True
    )
    st.title("🏥 HealthStat Analytics")
    st.markdown(
        "<p style='font-size:1.02rem; color:#64748B; margin-top:-10px;'>"
        "Interactive health data analysis and statistical exploration"
        "</p>",
        unsafe_allow_html=True
    )

with header_right:
    st.markdown(
        "<div style='background:#E2F3F1; color:#087F8C; "
        "padding:10px 14px; border-radius:10px; text-align:center; "
        "font-size:0.82rem; font-weight:700; margin-top:20px;'>"
        "● DEMO DATA</div>",
        unsafe_allow_html=True
    )

st.divider()

# =====================================================
# 8. SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown(
    "<div style='font-size:0.75rem; color:#087F8C; "
    "font-weight:700; letter-spacing:1.5px;'>HEALTHSTAT ANALYTICS</div>",
    unsafe_allow_html=True
)
st.sidebar.markdown("## Explore the data")
st.sidebar.caption("Use the filters below to focus the dashboard.")

gender_options = ["All"] + sorted(df["Gender"].dropna().unique().tolist())
diagnosis_options = ["All"] + sorted(df["Diagnosis"].dropna().unique().tolist())
smoking_options = ["All"] + sorted(df["Smoking Status"].dropna().unique().tolist())

def reset_filters():
    st.session_state["gender_filter"] = "All"
    st.session_state["diagnosis_filter"] = "All"
    st.session_state["smoking_filter"] = "All"


gender_filter = st.sidebar.selectbox(
    "Gender", gender_options, key="gender_filter"
)
diagnosis_filter = st.sidebar.selectbox(
    "Diagnosis", diagnosis_options, key="diagnosis_filter"
)
smoking_filter = st.sidebar.selectbox(
    "Smoking status", smoking_options, key="smoking_filter"
)

st.sidebar.button(
    "Reset all filters",
    use_container_width=True,
    on_click=reset_filters
)

filtered_df = df.copy()

if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]
if diagnosis_filter != "All":
    filtered_df = filtered_df[filtered_df["Diagnosis"] == diagnosis_filter]
if smoking_filter != "All":
    filtered_df = filtered_df[filtered_df["Smoking Status"] == smoking_filter]

st.sidebar.divider()
st.sidebar.markdown("**Current selection**")
st.sidebar.metric("Records in view", len(filtered_df))
st.sidebar.caption(f"Total dataset records: {len(df)}")

if filtered_df.empty:
    st.warning("No records match the selected filters. Please change your selections.")
    st.stop()

# =====================================================
# 9. HORIZONTAL NAVIGATION
# =====================================================

pages = st.tabs([
    "Overview",
    "Demographics",
    "Health Indicators",
    "Lifestyle & Adherence",
    "Relationships",
    "Data & Statistics"
])

# =====================================================
# PAGE 1: OVERVIEW
# =====================================================

with pages[0]:
    st.subheader("Health Overview")
    st.caption("A high-level view of the records currently selected.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
    with col2:
        st.metric("Average Age", f"{filtered_df['Age'].mean():.1f} years")
    with col3:
        st.metric("Average BMI", f"{filtered_df['BMI'].mean():.1f}")
    with col4:
        st.metric(
            "Average Cholesterol",
            f"{filtered_df['Cholesterol (mg/dL)'].mean():.1f} mg/dL"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        diagnosis_counts = (
            filtered_df["Diagnosis"].value_counts()
            .rename_axis("Diagnosis").reset_index(name="Count")
        )
        fig = px.bar(
            diagnosis_counts,
            x="Diagnosis",
            y="Count",
            color="Diagnosis",
            color_discrete_map=DIAGNOSIS_COLORS,
            title="Distribution of Diagnoses",
            text="Count"
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        show_chart(fig)

    with col2:
        gender_counts = (
            filtered_df["Gender"].value_counts()
            .rename_axis("Gender").reset_index(name="Count")
        )
        fig = px.pie(
            gender_counts,
            names="Gender",
            values="Count",
            hole=0.58,
            title="Gender Distribution",
            color="Gender",
            color_discrete_map={"Male": COLORS["navy"], "Female": COLORS["teal"]}
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent",
            marker=dict(line=dict(color="#FFFFFF", width=3))
        )
        show_chart(fig)

    st.info(
        "This dashboard uses a simulated dataset for educational analysis. "
        "It does not represent actual patient records or provide clinical advice."
    )

# =====================================================
# PAGE 2: DEMOGRAPHICS
# =====================================================

with pages[1]:
    st.subheader("Demographic Analysis")
    st.caption("Explore the age profile and diagnosis distribution across gender.")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(
            filtered_df,
            x="Age",
            nbins=10,
            title="Age Distribution",
            color_discrete_sequence=[COLORS["teal"]]
        )
        fig.update_traces(marker_line_color="#FFFFFF", marker_line_width=1)
        show_chart(fig)

    with col2:
        diagnosis_gender = pd.crosstab(
            filtered_df["Diagnosis"], filtered_df["Gender"]
        ).reset_index()
        gender_columns = [c for c in diagnosis_gender.columns if c != "Diagnosis"]

        fig = px.bar(
            diagnosis_gender,
            x="Diagnosis",
            y=gender_columns,
            barmode="group",
            title="Diagnosis by Gender",
            color_discrete_map={"Male": COLORS["navy"], "Female": COLORS["teal"]}
        )
        show_chart(fig)

    st.markdown("#### Demographic Summary")
    demographic_summary = filtered_df[["Age"]].describe().round(2)
    st.dataframe(demographic_summary, use_container_width=True)

# =====================================================
# PAGE 3: HEALTH INDICATORS
# =====================================================

with pages[2]:
    st.subheader("Health Indicators Analysis")
    st.caption("Select an indicator to inspect its distribution and variation by diagnosis.")

    health_variables = [
        "BMI",
        "Cholesterol (mg/dL)",
        "Glucose Level (mg/dL)",
        "Heart Rate (bpm)",
        "Systolic BP",
        "Diastolic BP"
    ]
    available_variables = [
        col for col in health_variables if col in filtered_df.columns
    ]

    if available_variables:
        selected_variable = st.selectbox(
            "Select health indicator",
            available_variables
        )

        col1, col2 = st.columns(2)

        with col1:
            fig = px.histogram(
                filtered_df,
                x=selected_variable,
                nbins=10,
                title=f"Distribution of {selected_variable}",
                color_discrete_sequence=[COLORS["teal"]]
            )
            show_chart(fig)

        with col2:
            fig = px.box(
                filtered_df,
                x="Diagnosis",
                y=selected_variable,
                color="Diagnosis",
                color_discrete_map=DIAGNOSIS_COLORS,
                title=f"{selected_variable} by Diagnosis"
            )
            show_chart(fig)

        st.markdown("#### Health Indicator Summary")
        st.dataframe(
            filtered_df[available_variables].describe().round(2),
            use_container_width=True
        )
    else:
        st.warning("No health indicator columns were found in the dataset.")

# =====================================================
# PAGE 4: LIFESTYLE & ADHERENCE
# =====================================================

with pages[3]:
    st.subheader("Lifestyle and Medication Adherence")
    st.caption("Explore smoking status, physical activity and medication adherence.")

    col1, col2 = st.columns(2)

    with col1:
        smoking_counts = (
            filtered_df["Smoking Status"].value_counts()
            .rename_axis("Smoking Status").reset_index(name="Count")
        )
        fig = px.bar(
            smoking_counts,
            x="Smoking Status",
            y="Count",
            color="Smoking Status",
            title="Smoking Status Distribution",
            color_discrete_map={
                "Smoker": COLORS["coral"],
                "Non-Smoker": COLORS["teal"]
            },
            text="Count"
        )
        fig.update_traces(textposition="outside")
        show_chart(fig)

    with col2:
        activity_counts = (
            filtered_df["Physical Activity"].value_counts()
            .rename_axis("Physical Activity").reset_index(name="Count")
        )
        fig = px.pie(
            activity_counts,
            names="Physical Activity",
            values="Count",
            hole=0.55,
            title="Physical Activity Distribution",
            color="Physical Activity",
            color_discrete_map={
                "Low": COLORS["coral"],
                "Moderate": COLORS["amber"],
                "High": COLORS["teal"]
            }
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#FFFFFF", width=3))
        )
        show_chart(fig)

    st.markdown("#### Lifestyle Indicators")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Average Medication Adherence",
            f"{filtered_df['Medication Adherence (%)'].mean():.1f}%"
        )
    with col2:
        st.metric(
            "Average Cholesterol",
            f"{filtered_df['Cholesterol (mg/dL)'].mean():.1f} mg/dL"
        )

    fig = px.box(
        filtered_df,
        x="Smoking Status",
        y="Cholesterol (mg/dL)",
        color="Smoking Status",
        title="Cholesterol by Smoking Status",
        color_discrete_map={
            "Smoker": COLORS["coral"],
            "Non-Smoker": COLORS["teal"]
        }
    )
    show_chart(fig)

# =====================================================
# PAGE 5: RELATIONSHIPS
# =====================================================

with pages[4]:
    st.subheader("Statistical Relationships")
    st.caption("Explore patterns and associations among selected numerical variables.")

    if correlation_matrix is not None:
        numeric_correlation = correlation_matrix.select_dtypes(include="number")
        fig = px.imshow(
            numeric_correlation,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1,
            zmax=1,
            aspect="auto",
            title="Correlation Heatmap"
        )
        fig.update_layout(height=570)
        show_chart(fig, height=570)
    else:
        st.warning("The saved correlation matrix was not found in the outputs folder.")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            filtered_df,
            x="BMI",
            y="Cholesterol (mg/dL)",
            color="Diagnosis",
            color_discrete_map=DIAGNOSIS_COLORS,
            title="BMI vs Cholesterol",
            trendline="ols",
            hover_data=["Age", "Gender"]
        )
        show_chart(fig)

    with col2:
        if "Systolic BP" in filtered_df.columns:
            fig = px.scatter(
                filtered_df,
                x="Age",
                y="Systolic BP",
                color="Diagnosis",
                color_discrete_map=DIAGNOSIS_COLORS,
                title="Age vs Systolic Blood Pressure",
                trendline="ols",
                hover_data=["Gender"]
            )
            show_chart(fig)

    st.info(
        "Correlation describes statistical association, not causation. "
        "The dataset is simulated, so patterns should not be interpreted as clinical evidence."
    )

# =====================================================
# PAGE 6: DATA & STATISTICS
# =====================================================

with pages[5]:
    st.subheader("Data and Statistical Summary")
    st.caption("Review the exported statistical tables and the records currently in view.")

    st.markdown("#### Descriptive Statistics")
    if descriptive_summary is not None:
        st.dataframe(
            descriptive_summary.round(3),
            use_container_width=True
        )
    else:
        st.warning("Descriptive statistics file not found in the outputs folder.")

    st.divider()
    st.markdown("#### Data Quality Report")
    if quality_report is not None:
        st.dataframe(quality_report, use_container_width=True)
    else:
        st.warning("Data quality report not found in the outputs folder.")

    st.divider()
    st.markdown("#### Filtered Dataset")
    st.write(f"**Records currently displayed:** {len(filtered_df)}")

    display_df = filtered_df.drop(columns=["Patient ID"], errors="ignore")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_data,
        file_name="healthstat_filtered_data.csv",
        mime="text/csv"
    )

# =====================================================
# 10. FOOTER
# =====================================================

st.divider()
st.markdown(
    "<div style='text-align:center; color:#8292A3; font-size:0.82rem; "
    "padding:8px 0 2px 0;'>"
    "<strong style='color:#087F8C;'>HealthStat Analytics</strong>"
    " &nbsp;|&nbsp; Statistical Thinking in Data Science"
    " &nbsp;|&nbsp; Simulated Dataset · Educational Use Only"
    "</div>",
    unsafe_allow_html=True
)
