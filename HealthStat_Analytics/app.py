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

# The selected theme is stored in session state so the whole dashboard can
# switch appearance consistently when the user changes the control.
st.session_state.setdefault("dashboard_theme", "Dark")
dashboard_theme = st.session_state["dashboard_theme"]

THEMES = {
    "Dark": {
        "page": "#0B1420", "surface": "#142334", "surface_alt": "#1B3044",
        "text": "#E8F0F7", "muted": "#B8C7D6", "heading": "#FFFFFF",
        "border": "#38516A", "grid": "#30465B", "accent": "#39D0BD",
        "plot": "#142334", "sidebar_start": "#163B50", "sidebar_end": "#116B70",
        "series": ["#45D6C5", "#FFB84D", "#B49AFF", "#FF829A", "#70B7FF", "#C4E879", "#F6A34A", "#45D483"]
    },
    "Light": {
        "page": "#F4F7FB", "surface": "#FFFFFF", "surface_alt": "#EDF3F8",
        "text": "#243447", "muted": "#526579", "heading": "#14283D",
        "border": "#D5E0EA", "grid": "#E3EAF1", "accent": "#087F8C",
        "plot": "#FFFFFF", "sidebar_start": "#E1F2F2", "sidebar_end": "#D5E9F4",
        "series": ["#087F8C", "#D97706", "#7654C8", "#D94868", "#2563A6", "#5D861B", "#B45309", "#16834A"]
    }
}
UI = THEMES[dashboard_theme]
DIAGNOSIS_COLORS = {
    "Hypertension": UI["series"][0], "Diabetes": UI["series"][1],
    "Heart Disease": UI["series"][2], "Asthma": UI["series"][3],
    "Obesity": UI["series"][4]
}
pio.templates.default = "plotly_dark" if dashboard_theme == "Dark" else "plotly_white"

# =====================================================
# 4. CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>
:root {{ color-scheme: {'dark' if dashboard_theme == 'Dark' else 'light'} !important; }}
html, body, .stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"], [data-testid="stMainBlockContainer"] {{
    background: {UI["page"]} !important;
    color: {UI["text"]} !important;
    font-family: "Segoe UI", Arial, sans-serif !important;
}}
header[data-testid="stHeader"] {{ background: {UI["page"]} !important; }}
[data-testid="stToolbar"] {{ background: transparent !important; }}
.block-container {{ max-width: 1500px; padding: 2rem 2.4rem 3rem; }}

.stApp p, .stApp span, .stApp label, .stApp li, .stApp small,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stCaptionContainer"] p,
[data-testid="stWidgetLabel"] p {{
    color: {UI["text"]} !important;
}}
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
    color: {UI["heading"]} !important; font-weight: 700 !important;
}}
h1 {{ font-size: 3.0rem !important; letter-spacing: -1.1px; font-weight: 900 !important; line-height: 1.08 !important; }}
h2 {{ font-size: 1.65rem !important; font-weight: 800 !important; }}
h3, h4 {{ color: {UI["accent"]} !important; }}

/* Sidebar */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div,
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
    background: {UI["surface"]} !important;
}}
[data-testid="stSidebar"] {{ border-right: 1px solid {UI["border"]} !important; }}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {{
    font-size: 1.35rem !important; font-weight: 850 !important;
    letter-spacing: -0.35px !important; color: {UI["heading"]} !important;
}}

[data-testid="stSidebar"] * {{ color: {UI["text"]} !important; }}
[data-testid="stRadio"] label,
[data-testid="stRadio"] p,
[data-testid="stRadio"] span {{
    color: {UI["text"]} !important;
}}
[data-testid="stRadio"] [role="radiogroup"] {{
    gap: 0.35rem !important;
    background: {UI["surface"]} !important;
    border: 1px solid {UI["border"]} !important;
    border-radius: 12px !important;
    padding: 8px 10px !important;
}}
[data-testid="stRadio"] [role="radio"] {{
    color: {UI["text"]} !important;
}}

/* Dropdowns and inputs */
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {{
    background: {UI["surface_alt"]} !important;
    border: 1px solid {UI["border"]} !important;
    border-radius: 9px !important;
    color: {UI["text"]} !important;
}}
[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stMultiSelect"] [data-baseweb="select"] * {{
    color: {UI["text"]} !important;
    background-color: transparent !important;
}}
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {{
    background: {UI["surface_alt"]} !important;
}}
[data-testid="stSelectbox"] [data-baseweb="select"] input,
[data-testid="stMultiSelect"] [data-baseweb="select"] input {{
    color: {UI["text"]} !important;
    -webkit-text-fill-color: {UI["text"]} !important;
}}
[data-baseweb="popover"], [data-baseweb="menu"],
[role="listbox"], [role="option"] {{
    background: {UI["surface"]} !important;
    color: {UI["text"]} !important;
}}

[data-baseweb="popover"], [data-baseweb="menu"],
[role="listbox"], [role="option"] {{
    background: {UI["surface"]} !important; color: {UI["text"]} !important;
}}

/* KPI cards */
[data-testid="stMetric"] {{
    background: {UI["surface"]} !important;
    border: 1px solid {UI["border"]} !important;
    border-radius: 15px !important;
    padding: 20px 22px !important;
    box-shadow: 0 5px 16px rgba(0,0,0,0.12) !important;
}}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {{
    color: {UI["heading"]} !important;
}}
[data-testid="stMetricLabel"] {{ color: {UI["accent"]} !important; }}

/* Tabs */
button[data-baseweb="tab"] {{
    color: {UI["muted"]} !important; font-weight: 650 !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {UI["accent"]} !important; }}
div[data-baseweb="tab-highlight"] {{ background: {UI["accent"]} !important; }}

/* Buttons */
.stButton > button, .stDownloadButton > button {{
    background: {UI["accent"]} !important; color: {"#FFFFFF" if dashboard_theme == "Dark" else "#FFFFFF"} !important;
    border: 0 !important; border-radius: 9px !important; font-weight: 650 !important;
}}
.stButton > button *, .stDownloadButton > button * {{ color: #FFFFFF !important; }}

/* Tables, alerts and separators */
[data-testid="stDataFrame"], [data-testid="stTable"] {{
    background: {UI["surface"]} !important;
    border: 1px solid {UI["border"]} !important;
    border-radius: 11px !important;
}}
[data-testid="stAlert"] {{ border-radius: 11px !important; }}
hr {{ border-color: {UI["border"]} !important; }}
footer, #MainMenu {{ visibility: hidden; }}

@media (max-width: 768px) {{
    .block-container {{ padding: 1rem 1rem 2rem; }}
    h1 {{ font-size: 1.75rem !important; }}
}}


/* Sidebar filter controls: explicit contrast for both themes.
   BaseWeb renders select values, placeholders, icons and option menus
   in separate nested elements, so style each part directly. */
[data-testid="stSidebar"] [data-testid="stSelectbox"] label,
[data-testid="stSidebar"] [data-testid="stSelectbox"] label p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{
    color: {UI["heading"]} !important;
    font-weight: 750 !important;
    font-size: 0.96rem !important;
}}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    background: {UI["heading"]} !important;
    border: 1.5px solid {UI["surface_alt"]} !important;
    border-radius: 10px !important;
    min-height: 44px !important;
    box-shadow: none !important;
}}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] * {{
    color: {UI["border"]} !important;
    -webkit-text-fill-color: {UI["text"]} !important;
}}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] input {{
    color: {UI["text"]} !important;
    -webkit-text-fill-color: {UI["text"]} !important;
    caret-color: {UI["text"]} !important;
}}
[data-testid="stSidebar"] [data-testid="stSelectbox"] svg {{
    fill: {UI["text"]} !important;
    color: {UI["muted"]} !important;
}}
/* Dropdown menus are portalled outside the sidebar in Streamlit. */
[data-baseweb="popover"] [data-baseweb="menu"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"] {{
    background: {UI["muted"]} !important;
    border: 1px solid {UI["surface"]} !important;
}}
[data-baseweb="popover"] [role="option"],
[data-baseweb="menu"] [role="option"] {{
    background: {UI["border"]} !important;
    color: {UI["surface"]} !important;
    -webkit-text-fill-color: {UI["text"]} !important;
    min-height: 38px !important;
}}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [role="option"][aria-selected="true"],
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [role="option"][aria-selected="true"] {{
    background: {UI["text"]} !important;
    color: {UI["surface_alt"]} !important;
    -webkit-text-fill-color: {UI["heading"]} !important;
}}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
    color: {UI["heading"]} !important;
}}
[data-testid="stSidebar"] [data-testid="stButton"] button {{
    min-height: 42px !important;
}}

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
    """Apply chart styling that follows the selected dashboard appearance."""
    dark = dashboard_theme == "Dark"
    plot_bg = UI["plot"]
    text_color = UI["text"]
    heading_color = UI["heading"]
    grid_color = UI["grid"]
    border_color = UI["border"]

    fig.update_layout(
        template="plotly_dark" if dark else "plotly_white",
        height=height,
        paper_bgcolor=plot_bg,
        plot_bgcolor=plot_bg,
        font=dict(family="Segoe UI, Arial, sans-serif", color=text_color, size=13),
        title=dict(font=dict(size=18, color=heading_color), x=0.03, xanchor="left"),
        # High-contrast legend styling: explicit text, title, background and border
        # prevent labels from disappearing against the chart panel.
        legend=dict(
            bgcolor=plot_bg,
            bordercolor=border_color,
            borderwidth=1,
            font=dict(color=text_color, size=13, family="Segoe UI, Arial, sans-serif"),
            title_font=dict(color=heading_color, size=13),
            itemsizing="constant",
            tracegroupgap=8,
            itemclick="toggle",
            itemdoubleclick="toggleothers"
        ),
        # Use a bright, colour-blind-conscious sequence with sufficient contrast
        # against the dark chart background.
        colorway=UI["series"],
        margin=dict(l=55, r=35, t=68, b=60),
        hoverlabel=dict(
            bgcolor=UI["surface"], bordercolor=border_color,
            font=dict(color=text_color, size=12)
        )
    )
    # Keep chart panels, plot areas, legends and hover labels in the selected theme.
    fig.update_traces(
        selector=dict(type="pie"),
        marker_line_color=border_color,
        marker_line_width=2,
        textfont=dict(color=text_color, size=13)
    )
    # Improve labels displayed directly on bars, points and other traces.
    # Explicit font colour avoids relying on Plotly's default template colour.
    fig.update_traces(
        selector=dict(type="bar"),
        textfont=dict(color=text_color, size=12)
    )
    fig.update_xaxes(
        title_font=dict(color=text_color, size=13),
        tickfont=dict(color=UI["muted"], size=11),
        showgrid=False, linecolor=border_color, zerolinecolor=border_color
    )
    fig.update_yaxes(
        title_font=dict(color=text_color, size=13),
        tickfont=dict(color=UI["muted"], size=11),
        gridcolor=grid_color, linecolor=border_color,
        zerolinecolor=border_color
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
        f"<div style='color:{UI['accent']}; font-size:0.78rem; "
        "font-weight:700; letter-spacing:2px; text-transform:uppercase;'>"
        "STATISTICAL THINKING IN DATA SCIENCE</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:2.85rem; line-height:1.08; font-weight:900; "
        f"letter-spacing:-1.2px; color:{UI['heading']}; margin:5px 0 12px;'>"
        "🏥 HealthStat Analytics</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<p style='font-size:1.02rem; color:{UI['muted']}; margin-top:-10px;'>"
        "Interactive health data analysis and statistical exploration"
        "</p>",
        unsafe_allow_html=True
    )

with header_right:
    st.radio(
        "Appearance",
        options=["Dark", "Light"],
        horizontal=True,
        key="dashboard_theme",
        label_visibility="visible"
    )

st.divider()

# =====================================================
# 8. SIDEBAR FILTERS
# =====================================================

st.sidebar.markdown(
    f"<div style='background:linear-gradient(135deg,{UI['sidebar_start']},{UI['sidebar_end']}); "
    f"padding:17px 15px; border:1px solid {UI['border']}; border-radius:14px; "
    "margin:4px 0 20px;'>"
    "<div style='font-size:1.25rem; font-weight:900; letter-spacing:-0.4px; "
    f"color:{UI['heading']};'>🏥 HealthStat Analytics</div>"
    f"<div style='font-size:0.72rem; color:{UI['text']}; margin-top:5px; "
    "letter-spacing:1px; font-weight:700;'>HEALTH DATA EXPLORER</div></div>",
    unsafe_allow_html=True
)
st.sidebar.markdown("## Explore the data")
st.sidebar.caption("Choose filters to explore the patient records.")

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
    "Data & Statistics",
    "Key Findings",
    "AI Explanation"
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
            marker=dict(line=dict(color=UI["border"], width=2))
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
            marker=dict(line=dict(color=UI["border"], width=2))
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
# PAGE 7: KEY FINDINGS
# =====================================================

with pages[6]:
    st.subheader("Complete Statistical Findings")
    st.caption(
        "This section consolidates the findings from the Health Stats and Data "
        "Analysis notebook. It uses the full dataset, independently of sidebar filters."
    )

    findings_df = df.copy()
    if "Systolic BP" not in findings_df.columns or "Diastolic BP" not in findings_df.columns:
        bp_values = findings_df["Blood Pressure"].astype(str).str.extract(
            r"^\s*(\d+)\s*/\s*(\d+)\s*$"
        )
        findings_df["Systolic BP"] = pd.to_numeric(bp_values[0], errors="coerce")
        findings_df["Diastolic BP"] = pd.to_numeric(bp_values[1], errors="coerce")

    if "Last Visit" in findings_df.columns:
        findings_df["Last Visit"] = pd.to_datetime(
            findings_df["Last Visit"], dayfirst=True, errors="coerce"
        )

    finding_numeric = [
        "Age", "Heart Rate (bpm)", "Cholesterol (mg/dL)", "BMI",
        "Systolic BP", "Diastolic BP", "Medication Adherence (%)",
        "Glucose Level (mg/dL)"
    ]
    finding_numeric = [c for c in finding_numeric if c in findings_df.columns]

    st.info(
        f"Analysis population: {len(findings_df)} records. "
        "The sidebar filters do not change the results on this page."
    )

    # 1. Dataset quality
    st.markdown("### 1. Dataset profile and data quality")
    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Records", f"{len(findings_df):,}")
    q2.metric("Original columns", "14")
    q3.metric("Missing cells", f"{int(findings_df.isna().sum().sum())}")
    q4.metric("Duplicate rows", f"{int(findings_df.duplicated().sum())}")

    quality_summary = pd.DataFrame({
        "Data quality check": [
            "Number of records", "Number of original columns",
            "Missing values (all columns)", "Duplicate complete rows",
            "Unique Patient IDs", "Repeated Patient IDs",
            "Unparsed blood-pressure records", "Unparsed visit dates"
        ],
        "Result": [
            len(findings_df), 14, int(findings_df.isna().sum().sum()),
            int(findings_df.duplicated().sum()),
            int(findings_df["Patient ID"].nunique()),
            int(findings_df["Patient ID"].duplicated().sum()),
            int(findings_df[["Systolic BP", "Diastolic BP"]].isna().any(axis=1).sum()),
            int(findings_df["Last Visit"].isna().sum())
        ]
    })
    st.dataframe(quality_summary, use_container_width=True, hide_index=True)

    if findings_df["Last Visit"].notna().any():
        st.write(
            f"**Parsed date range:** {findings_df['Last Visit'].min():%d %B %Y} "
            f"to {findings_df['Last Visit'].max():%d %B %Y}."
        )
    st.caption(
        "The notebook assumes day/month/year for slash-formatted dates. Two early "
        "dates are ambiguous from the text alone. Confirm the date convention before "
        "drawing date-based conclusions."
    )

    # 2. Numerical summaries
    st.markdown("### 2. Numerical variable findings")
    numeric_summary = findings_df[finding_numeric].describe().T
    numeric_summary["median"] = findings_df[finding_numeric].median()
    numeric_summary["IQR"] = (
        findings_df[finding_numeric].quantile(0.75)
        - findings_df[finding_numeric].quantile(0.25)
    )
    st.dataframe(numeric_summary.round(2), use_container_width=True)

    # 3. Categorical distributions
    st.markdown("### 3. Categorical distribution findings")
    categorical_variables = [
        "Gender", "Diagnosis", "Smoking Status", "Physical Activity"
    ]
    category_tabs = st.tabs(categorical_variables)
    for tab, variable in zip(category_tabs, categorical_variables):
        with tab:
            counts = findings_df[variable].value_counts(dropna=False)
            percentages = findings_df[variable].value_counts(
                normalize=True, dropna=False
            ).reindex(counts.index) * 100
            distribution = pd.DataFrame({
                "Category": counts.index.astype(str),
                "Frequency": counts.values,
                "Percentage (%)": percentages.values.round(1)
            })
            st.dataframe(distribution, use_container_width=True, hide_index=True)

    # 4. IQR screening
    st.markdown("### 4. IQR outlier screening")
    outlier_rows = []
    for variable in finding_numeric:
        q1 = findings_df[variable].quantile(0.25)
        q3 = findings_df[variable].quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        flagged = findings_df[
            (findings_df[variable] < lower) | (findings_df[variable] > upper)
        ]
        outlier_rows.append({
            "Variable": variable,
            "Lower fence": round(lower, 2),
            "Upper fence": round(upper, 2),
            "IQR-flagged records": len(flagged)
        })
    st.dataframe(pd.DataFrame(outlier_rows), use_container_width=True, hide_index=True)
    st.caption(
        "No numerical variables had IQR-flagged observations in the supplied file. "
        "IQR flags are screening indicators, not proof of data errors."
    )

    # 5. Pairwise associations and full correlation matrix
    st.markdown("### 5. Pairwise relationship findings")
    pairs = [
        ("BMI", "Cholesterol (mg/dL)"),
        ("Age", "Systolic BP"),
        ("Age", "Glucose Level (mg/dL)")
    ]
    pair_results = []
    for xvar, yvar in pairs:
        pair_results.append({
            "Variable pair": f"{xvar} vs {yvar}",
            "Pearson r": findings_df[xvar].corr(findings_df[yvar], method="pearson"),
            "Spearman rho": findings_df[xvar].corr(findings_df[yvar], method="spearman")
        })
    st.dataframe(pd.DataFrame(pair_results).round(3), use_container_width=True, hide_index=True)

    st.markdown("#### Full Pearson correlation matrix")
    full_corr = findings_df[finding_numeric].corr(method="pearson")
    st.dataframe(full_corr.round(3), use_container_width=True)

    # 6. Numeric group comparisons
    st.markdown("### 6. Group comparison findings")
    st.markdown("#### Cholesterol by smoking status")
    smoking_cholesterol_summary = (
        findings_df.groupby("Smoking Status")["Cholesterol (mg/dL)"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .round(2)
    )
    st.dataframe(smoking_cholesterol_summary, use_container_width=True)

    st.markdown("#### Glucose by diagnosis")
    glucose_by_diagnosis = (
        findings_df.groupby("Diagnosis")["Glucose Level (mg/dL)"]
        .agg(["count", "mean", "median", "std", "min", "max"])
        .round(2)
        .sort_values("mean")
    )
    st.dataframe(glucose_by_diagnosis, use_container_width=True)

    # 7. Categorical associations
    st.markdown("### 7. Categorical relationship findings")
    st.markdown("#### Gender by diagnosis: counts")
    gender_diag = pd.crosstab(findings_df["Gender"], findings_df["Diagnosis"])
    st.dataframe(gender_diag, use_container_width=True)
    st.markdown("#### Gender by diagnosis: row percentages")
    gender_diag_pct = pd.crosstab(
        findings_df["Gender"], findings_df["Diagnosis"], normalize="index"
    ) * 100
    st.dataframe(gender_diag_pct.round(1), use_container_width=True)

    st.markdown("#### Smoking status by diagnosis: counts")
    smoking_diag = pd.crosstab(
        findings_df["Smoking Status"], findings_df["Diagnosis"]
    )
    st.dataframe(smoking_diag, use_container_width=True)
    st.markdown("#### Smoking status by diagnosis: row percentages")
    smoking_diag_pct = pd.crosstab(
        findings_df["Smoking Status"], findings_df["Diagnosis"], normalize="index"
    ) * 100
    st.dataframe(smoking_diag_pct.round(1), use_container_width=True)
    st.caption(
        "These tables describe how categories are distributed within this sample. "
        "Small or zero cells limit interpretation."
    )

    # 8. Monthly record counts
    st.markdown("### 8. Records by parsed visit month")
    monthly = (
        findings_df.dropna(subset=["Last Visit"])
        .assign(Month=lambda x: x["Last Visit"].dt.to_period("M").astype(str))
        .groupby("Month")["Patient ID"].count()
        .rename("Record count").reset_index()
    )
    st.dataframe(monthly, use_container_width=True, hide_index=True)
    st.caption(
        "Monthly counts describe the parsed dates in this simulated file. They are "
        "not evidence of real hospital attendance or disease-incidence trends."
    )

    # 9. Stratified age–blood pressure correlations
    st.markdown("### 9. Age and systolic blood pressure by gender")
    overall_corr = findings_df["Age"].corr(findings_df["Systolic BP"])
    st.metric("Overall Pearson correlation", f"{overall_corr:.3f}")
    stratified_corr = findings_df.groupby("Gender").apply(
        lambda group: group["Age"].corr(group["Systolic BP"])
    ).rename("Pearson correlation").reset_index()
    st.dataframe(stratified_corr.round(3), use_container_width=True, hide_index=True)

    # 10. Overall interpretation and limits
    st.markdown("### 10. Overall interpretation")
    st.markdown(
        """
        - The supplied file has 40 records, no missing values, no duplicate complete
          rows and 40 unique patient identifiers.
        - Gender is evenly split, each diagnosis category has eight records, smoking
          status has 19 smokers and 21 non-smokers, and physical activity has 20 low,
          12 moderate and 8 high activity records.
        - BMI and cholesterol have a very strong positive association. Age also has
          positive associations with systolic blood pressure and glucose.
        - The correlation matrix contains many unusually high positive correlations
          and strong negative correlations with medication adherence.
        - The diagnosis, gender and smoking categories show highly structured patterns.
          This raises the possibility that the simulated values were generated using
          linked rules or a fixed template.
        """
    )
    st.warning(
        "The notebook reports exploratory/descriptive statistics, Pearson and "
        "Spearman correlations, IQR screening, group summaries, cross-tabulations, "
        "monthly record counts and stratified correlations. It does not report "
        "formal hypothesis tests such as t-tests, ANOVA or chi-square tests. "
        "The dataset is simulated and small. Findings are not clinical evidence, "
        "do not establish causation and should not be generalized to real patients."
    )


# =====================================================
# PAGE 8: AUTOMATED AI-STYLE EXPLANATIONS
# =====================================================

with pages[7]:
    st.subheader("Automated Explanation of Findings")
    st.caption(
        "Plain-language explanations generated from the dataset's calculated "
        "statistics. This is a rule-based feature, not a live generative AI service."
    )

    explanation_df = df.copy()
    if "Systolic BP" not in explanation_df.columns or "Diastolic BP" not in explanation_df.columns:
        bp_parts = explanation_df["Blood Pressure"].astype(str).str.extract(
            r"^\s*(\d+)\s*/\s*(\d+)\s*$"
        )
        explanation_df["Systolic BP"] = pd.to_numeric(bp_parts[0], errors="coerce")
        explanation_df["Diastolic BP"] = pd.to_numeric(bp_parts[1], errors="coerce")

    n_records = len(explanation_df)
    bmi_corr = explanation_df["BMI"].corr(explanation_df["Cholesterol (mg/dL)"])
    age_sbp_corr = explanation_df["Age"].corr(explanation_df["Systolic BP"])
    age_glucose_corr = explanation_df["Age"].corr(explanation_df["Glucose Level (mg/dL)"])

    smoker_stats = explanation_df.groupby("Smoking Status")["Cholesterol (mg/dL)"].agg(["count", "mean"])
    glucose_stats = explanation_df.groupby("Diagnosis")["Glucose Level (mg/dL)"].mean().sort_values()

    def describe_strength(value):
        magnitude = abs(value)
        if magnitude >= 0.90:
            strength = "very strong"
        elif magnitude >= 0.70:
            strength = "strong"
        elif magnitude >= 0.40:
            strength = "moderate"
        elif magnitude >= 0.20:
            strength = "weak"
        else:
            strength = "very weak"
        direction = "positive" if value >= 0 else "negative"
        return strength, direction

    st.info(
        f"These explanations are based on all {n_records} records, not the subset "
        "currently selected in the sidebar."
    )

    st.markdown("### 1. Dataset overview")
    gender_counts = explanation_df["Gender"].value_counts()
    diagnosis_counts = explanation_df["Diagnosis"].value_counts()
    smoking_counts = explanation_df["Smoking Status"].value_counts()
    activity_counts = explanation_df["Physical Activity"].value_counts()
    mean_age = explanation_df["Age"].mean()
    mean_bmi = explanation_df["BMI"].mean()
    mean_chol = explanation_df["Cholesterol (mg/dL)"].mean()
    mean_adherence = explanation_df["Medication Adherence (%)"].mean()

    st.write(
        f"The dataset contains **{n_records} records**. The average age is "
        f"**{mean_age:.1f} years**, average BMI is **{mean_bmi:.1f}**, average "
        f"cholesterol is **{mean_chol:.1f} mg/dL**, and average medication "
        f"adherence is **{mean_adherence:.1f}%**."
    )
    st.write(
        f"Gender counts are {', '.join(f'{k}: {v}' for k, v in gender_counts.items())}. "
        f"The diagnosis categories are distributed as "
        f"{', '.join(f'{k}: {v}' for k, v in diagnosis_counts.items())}."
    )
    st.write(
        f"Smoking status counts are {', '.join(f'{k}: {v}' for k, v in smoking_counts.items())}. "
        f"Physical activity counts are "
        f"{', '.join(f'{k}: {v}' for k, v in activity_counts.items())}."
    )

    st.divider()
    st.markdown("### 2. Correlation explanations")

    strength, direction = describe_strength(bmi_corr)
    st.markdown("**BMI and cholesterol**")
    st.write(
        f"The Pearson correlation is **{bmi_corr:.3f}**, indicating a {strength} "
        f"{direction} linear association in this dataset. A positive association "
        "means records with higher BMI values tend also to have higher cholesterol "
        "values. It does not show that BMI causes cholesterol to increase."
    )

    strength, direction = describe_strength(age_sbp_corr)
    st.markdown("**Age and systolic blood pressure**")
    st.write(
        f"The Pearson correlation is **{age_sbp_corr:.3f}**, indicating a {strength} "
        f"{direction} association in these records. This describes how the two "
        "variables move together in this simulated sample; it is not proof of a "
        "causal or clinical relationship."
    )

    strength, direction = describe_strength(age_glucose_corr)
    st.markdown("**Age and glucose level**")
    st.write(
        f"The Pearson correlation is **{age_glucose_corr:.3f}**, indicating a "
        f"{strength} {direction} association in this dataset."
    )

    st.divider()
    st.markdown("### 3. Group comparison explanations")
    st.markdown("**Cholesterol by smoking status**")
    if "Smoker" in smoker_stats.index and "Non-Smoker" in smoker_stats.index:
        smoker_mean = smoker_stats.loc["Smoker", "mean"]
        nonsmoker_mean = smoker_stats.loc["Non-Smoker", "mean"]
        difference = smoker_mean - nonsmoker_mean
        comparison = "higher" if difference > 0 else "lower"
        st.write(
            f"The mean cholesterol among smokers is **{smoker_mean:.2f} mg/dL**, "
            f"compared with **{nonsmoker_mean:.2f} mg/dL** among non-smokers. "
            f"The smoker-group mean is {abs(difference):.2f} mg/dL {comparison}. "
            "This is a descriptive comparison and does not establish that smoking "
            "caused the difference."
        )
    st.dataframe(smoker_stats.round(2), use_container_width=True)

    st.markdown("**Glucose level by diagnosis**")
    lowest_group = glucose_stats.index[0]
    highest_group = glucose_stats.index[-1]
    st.write(
        f"The lowest group mean glucose is observed for **{lowest_group}** "
        f"({glucose_stats.iloc[0]:.2f} mg/dL), while the highest is observed for "
        f"**{highest_group}** ({glucose_stats.iloc[-1]:.2f} mg/dL). These are group "
        "averages; they do not describe every individual record."
    )
    st.dataframe(glucose_stats.rename("Mean glucose (mg/dL)").round(2), use_container_width=True)

    st.divider()
    st.markdown("### 4. Data quality and outlier explanations")
    missing_total = int(explanation_df.isna().sum().sum())
    duplicate_total = int(explanation_df.duplicated().sum())
    unique_ids = int(explanation_df["Patient ID"].nunique())
    st.write(
        f"The loaded dataset contains **{missing_total} missing cells**, "
        f"**{duplicate_total} duplicate complete rows**, and **{unique_ids} unique "
        "patient identifiers**. These checks help describe the completeness and "
        "consistency of the file."
    )

    outlier_count = 0
    outlier_details = []
    for variable in [
        "Age", "Heart Rate (bpm)", "Cholesterol (mg/dL)", "BMI",
        "Systolic BP", "Diastolic BP", "Medication Adherence (%)",
        "Glucose Level (mg/dL)"
    ]:
        if variable not in explanation_df.columns:
            continue
        q1 = explanation_df[variable].quantile(0.25)
        q3 = explanation_df[variable].quantile(0.75)
        iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((explanation_df[variable] < low) | (explanation_df[variable] > high)).sum())
        outlier_count += count
        outlier_details.append({"Variable": variable, "IQR flags": count})
    st.write(
        f"Across the numerical variables checked, **{outlier_count} variable-level "
        "IQR flags** were identified. An IQR flag is a prompt for review, not proof "
        "that a value is wrong. A record can be flagged in more than one variable."
    )
    st.dataframe(pd.DataFrame(outlier_details), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 5. Overall interpretation")
    st.write(
        "The strongest pattern in the analysis is the positive association between "
        "BMI and cholesterol. The dataset also shows differences in average glucose "
        "across diagnosis groups and in average cholesterol between smoking groups. "
        "These patterns can be explored further with plots and additional statistical "
        "tests, but the summaries alone do not establish cause and effect."
    )
    st.warning(
        "Important limitation: this is a small simulated dataset, not real patient "
        "data. The explanations are generated using fixed statistical rules and "
        "templates. They are not medical advice, do not provide diagnosis or "
        "treatment recommendations, and should not be generalized to real populations."
    )

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
