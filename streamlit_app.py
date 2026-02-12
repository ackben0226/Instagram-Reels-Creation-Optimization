
# **🎨 Creating Streamlit Dashboard (app.py)**
"""
Instagram Reels Quick Edit Feature - Interactive Dashboard
Deploy: streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import sys
import os

# Add parent directory to path for imports (works in notebook & script)
try:
    # If running as a script
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
except NameError:
    # If running in notebook, fall back to current working directory
    BASE_DIR = os.path.dirname(os.getcwd())

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

print("Base directory added to path:", BASE_DIR)


# Page configuration
st.set_page_config(
    page_title="Instagram Reels Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 5px solid #1E88E5;
    }
    .positive {
        color: #4CAF50;
        font-weight: 600;
    }
    .negative {
        color: #f44336;
        font-weight: 600;
    }
    .neutral {
        color: #FF9800;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def load_data():
    """Load analysis results"""
    try:
        # Load business impact
        with open('results/business_impact.json', 'r') as f:
            business_impact = json.load(f)
        
        # Load A/B test results
        ab_results = pd.read_csv('results/ab_test_results.csv')
        
        # Load funnel metrics
        funnel_overall = pd.read_csv('results/funnel_metrics_overall.csv')
        funnel_cohort = pd.read_csv('results/funnel_metrics_by_cohort.csv')
        
        return {
            'business_impact': business_impact,
            'ab_results': ab_results,
            'funnel_overall': funnel_overall,
            'funnel_cohort': funnel_cohort
        }
    except FileNotFoundError:
        # Create sample data for demo
        return create_sample_data()

def create_sample_data():
    """Create sample data for dashboard demo"""
    # Business impact
    business_impact = {
        'daily': {
            'additional_creators': 6085535,
            'additional_reels': 6694089,
            'additional_watch_time_hours': 46486.7,
            'additional_revenue': 70288
        },
        'monthly': {
            'additional_reels': 200822672,
            'additional_watch_time_hours': 1394601,
            'additional_revenue': 2108638
        }
    }
    
    # A/B test results
    ab_results = pd.DataFrame({
        'segment': ['overall', 'casual_creator', 'power_creator', 'Android', 'iPhone'],
        'control_mean': [0.23, 0.153, 0.348, 0.255, 0.315],
        'treatment_mean': [0.26, 0.170, 0.391, 0.279, 0.355],
        'relative_lift': [0.13, 0.106, 0.124, 0.094, 0.127],
        'p_value': [0.0001, 0.0000, 0.0000, 0.0000, 0.0000],
        'significant': [True, True, True, True, True]
    })
    
    # Funnel metrics
    funnel_steps = ['reels_tab_opened', 'create_button_clicked', 'camera_opened', 
                    'clip_recorded', 'audio_selected', 'edit_tool_opened', 'reels_posted']
    
    funnel_overall = pd.DataFrame({
        'funnel_step': funnel_steps,
        'sessions_reached': [100000, 85000, 70000, 60000, 50000, 40000, 30000],
        'conversion_rate': [1.0, 0.85, 0.70, 0.60, 0.50, 0.40, 0.30],
        'dropoff_rate': [0.0, 0.15, 0.18, 0.14, 0.17, 0.20, 0.25]
    })
    
    return {
        'business_impact': business_impact,
        'ab_results': ab_results,
        'funnel_overall': funnel_overall,
        'funnel_cohort': None
    }

def create_kpi_metrics(data):
    """Create KPI metrics at top of dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin:0; color:#666;">🎯 Creation Lift</h3>
            <h2 style="margin:0; color:#1E88E5;">10.6-12.7%</h2>
            <p style="margin:0; color:#666; font-size:0.9rem;">Statistically significant (p < 0.0000)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#666;">💰 Monthly Revenue</h3>
            <h2 style="margin:0; color:#4CAF50;">${data['business_impact']['monthly']['additional_revenue']:,.0f}</h2>
            <p style="margin:0; color:#666; font-size:0.9rem;">Conservative estimate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; color:#666;">📈 Additional Reels</h3>
            <h2 style="margin:0; color:#FF9800;">{data['business_impact']['monthly']['additional_reels']:,.0f}</h2>
            <p style="margin:0; color:#666; font-size:0.9rem;">Per month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin:0; color:#666;">📱 Feature Adoption</h3>
            <h2 style="margin:0; color:#9C27B0;">60%</h2>
            <p style="margin:0; color:#666; font-size:0.9rem;">Of treatment group</p>
        </div>
        """, unsafe_allow_html=True)

def plot_ab_test_results(ab_results):
    """Plot A/B test results with confidence intervals"""
    st.markdown('<div class="sub-header">A/B Test Results by Segment</div>', unsafe_allow_html=True)
    
    # Filter for segments (not overall)
    segment_results = ab_results[ab_results['segment'] != 'overall'].copy()
    
    # Create forest plot
    fig = go.Figure()
    
    # Color by significance
    colors = ['#4CAF50' if x else '#f44336' for x in segment_results['significant']]
    
    fig.add_trace(go.Scatter(
        x=segment_results['relative_lift'] * 100,  # Convert to percentage
        y=segment_results['segment'],
        mode='markers',
        marker=dict(
            size=20,
            color=colors,
            line=dict(width=2, color='DarkSlateGrey')
        ),
        error_x=dict(
            type='data',
            array=[5, 4, 3, 4, 3],  # Simulated confidence intervals
            arrayminus=[5, 4, 3, 4, 3],
            thickness=1.5,
            width=5,
            color='gray'
        ),
        hovertemplate="<b>%{y}</b><br>Lift: %{x:.1f}%<br>p-value: <0.0001<extra></extra>"
    ))
    
    # Add vertical lines
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="gray")
    fig.add_vline(x=10, line_width=1, line_dash="dot", line_color="green", 
                  annotation_text="10% Target", annotation_position="top right")
    
    fig.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Relative Lift (%)",
        yaxis_title="Segment",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    
    fig.update_xaxes(
        gridcolor='lightgray',
        zerolinecolor='gray'
    )
    
    fig.update_yaxes(
        gridcolor='lightgray'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add metrics table
    st.markdown("#### Detailed Results")
    display_df = segment_results[['segment', 'control_mean', 'treatment_mean', 'relative_lift', 'p_value']].copy()
    display_df['control_mean'] = display_df['control_mean'].apply(lambda x: f"{x:.1%}")
    display_df['treatment_mean'] = display_df['treatment_mean'].apply(lambda x: f"{x:.1%}")
    display_df['relative_lift'] = display_df['relative_lift'].apply(lambda x: f"{x:.1%}")
    display_df['p_value'] = display_df['p_value'].apply(lambda x: f"{x:.4f}")
    display_df.columns = ['Segment', 'Control Rate', 'Treatment Rate', 'Lift', 'p-value']
    
    st.dataframe(display_df, use_container_width=True)

def plot_funnel_analysis(funnel_data):
    """Plot creation funnel analysis"""
    st.markdown('<div class="sub-header">Creation Funnel Analysis</div>', unsafe_allow_html=True)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Funnel Conversion Rates', 'Drop-off Analysis'),
        specs=[[{'type': 'funnel'}, {'type': 'bar'}]]
    )
    
    # Funnel plot
    fig.add_trace(
        go.Funnel(
            name='Creation Flow',
            y=funnel_data['funnel_step'],
            x=funnel_data['sessions_reached'],
            textinfo="value+percent initial",
            opacity=0.7,
            connector=dict(line=dict(color='royalblue', width=3)),
            marker=dict(
                color=['#1E88E5', '#2196F3', '#42A5F5', '#64B5F6', 
                       '#90CAF9', '#BBDEFB', '#E3F2FD']
            )
        ),
        row=1, col=1
    )
    
    # Drop-off bar chart
    fig.add_trace(
        go.Bar(
            x=funnel_data['funnel_step'],
            y=funnel_data['dropoff_rate'] * 100,
            marker_color='#f44336',
            text=funnel_data['dropoff_rate'].apply(lambda x: f"{x:.1%}"),
            textposition='auto'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    fig.update_xaxes(title_text="Sessions", row=1, col=1)
    fig.update_xaxes(title_text="Funnel Step", row=1, col=2)
    fig.update_yaxes(title_text="Drop-off Rate (%)", row=1, col=2)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key insight
    st.info("""
    **Key Insight**: 42% of creators drop off at the editing stage. 
    This represents the biggest opportunity for improvement in the creation funnel.
    """)

def plot_business_impact(business_impact):
    """Plot business impact metrics"""
    st.markdown('<div class="sub-header">Business Impact Projection</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue projection
        fig1 = go.Figure()
        
        fig1.add_trace(go.Indicator(
            mode="number+delta",
            value=business_impact['monthly']['additional_revenue'],
            number={'prefix': "$", 'valueformat': ",.0f"},
            delta={'reference': 1500000, 'relative': True, 'valueformat': '.1%'},
            title={"text": "Monthly Revenue Impact"},
            domain={'row': 0, 'column': 0}
        ))
        
        fig1.update_layout(
            height=200,
            paper_bgcolor='pink',
            font=dict(size=18)
        )
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Reels projection
        fig2 = go.Figure()
        
        fig2.add_trace(go.Indicator(
            mode="number+delta",
            value=business_impact['monthly']['additional_reels'] / 1000000,
            number={'suffix': "M", 'valueformat': ".1f"},
            delta={'reference': 150, 'relative': True, 'valueformat': '.1%'},
            title={"text": "Monthly Additional Reels"},
            domain={'row': 0, 'column': 0}
        ))
        
        fig2.update_layout(
            height=200,
            paper_bgcolor='pink',
            font=dict(size=18)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Assumptions table
    st.markdown("#### Conservative Assumptions")
    
    assumptions = pd.DataFrame({
        'Parameter': ['Feature Adoption', 'Reels Monetized', 'Avg CPM', 'Creator Distribution', 'Watch Time per Reel'],
        'Value': ['60%', '35%', '$20', '15% casual, 10% power', '30 seconds'],
        'Industry Benchmark': ['50-70%', '30-40%', '$15-50', 'Varies by platform', '25-35 seconds'],
        'Rationale': ['From experiment data', 'Conservative estimate', 'Lower bound for modeling', 'Based on Meta reports', 'Average from analysis']
    })
    
    st.dataframe(assumptions, use_container_width=True)

def plot_launch_strategy():
    """Plot launch strategy timeline"""
    st.markdown('<div class="sub-header">Phased Launch Strategy</div>', unsafe_allow_html=True)
    
    # Create Gantt chart
    phases = pd.DataFrame([
        dict(Task="Phase 1", Start='2024-03-01', Finish='2024-03-14', 
             Description="10% rollout to iPhone casual creators", Lift="12.7%", Audience="10M users"),
        dict(Task="Phase 2", Start='2024-03-15', Finish='2024-03-28', 
             Description="50% rollout to iPhone users", Lift="≥8% maintained", Audience="50M users"),
        dict(Task="Phase 3", Start='2024-04-01', Finish='2024-04-30', 
             Description="100% rollout to casual creators", Lift="≥8% maintained", Audience="225M users"),
        dict(Task="Phase 4", Start='2024-05-01', Finish='2024-05-31', 
             Description="Optimize & expand to Android", Lift="≥8% target", Audience="Full Android")
    ])
    
    fig = px.timeline(
        phases, 
        x_start="Start", 
        x_end="Finish", 
        y="Task",
        color="Task",
        color_discrete_sequence=['#1E88E5', '#2196F3', '#42A5F5', '#64B5F6'],
        hover_data=["Description", "Lift", "Audience"]
    )
    
    fig.update_layout(
        height=300,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis_title="Timeline",
        yaxis_title="",
        font=dict(size=12)
    )
    
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
    
    # Success metrics
    st.markdown("#### Success Metrics by Phase")
    
    success_metrics = pd.DataFrame({
        'Phase': ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4'],
        'Primary Metric': ['Lift ≥12%', 'Lift ≥8%', 'Lift ≥8%', 'Lift ≥8%'],
        'Adoption': ['≥40%', '≥50%', '≥50%', '≥50%'],
        'Watch Time': ['≥28s', '≥28s', '≥28s', '≥28s'],
        'Crashes': ['<0.1%', '<0.1%', '<0.1%', '<0.1%']
    })
    
    st.dataframe(success_metrics, use_container_width=True)

def main():
    """Main dashboard function"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/124/124010.png", width=100)
        st.title("Instagram Reels Analytics")
        
        st.markdown("---")
        
        st.markdown("### 📊 Dashboard Sections")
        section = st.radio(
            "Navigate to:",
            ["Executive Summary", "A/B Test Results", "Funnel Analysis", 
             "Business Impact", "Launch Strategy", "Methodology"]
        )
        
        st.markdown("---")
        
        st.markdown("### ⚙️ Assumptions")
        
        # Interactive sliders for business assumptions
        adoption_rate = st.slider(
            "Feature Adoption Rate", 
            min_value=0.0, max_value=1.0, value=0.6, step=0.05,
            help="Percentage of users who will use Quick Edit feature"
        )
        
        monetization_rate = st.slider(
            "Monetization Rate", 
            min_value=0.0, max_value=1.0, value=0.35, step=0.05,
            help="Percentage of Reels that show ads"
        )
        
        cpm = st.slider(
            "Average CPM ($)", 
            min_value=5, max_value=50, value=20, step=5,
            help="Cost per 1000 ad impressions"
        )
        
        st.markdown("---")
        
        st.markdown("### 📈 Last Updated")
        st.caption("February 15, 2026")
        
        st.markdown("### 👤 Analyst")
        st.caption("Your Name - Senior Data Scientist")
    
    # Load data
    data = load_data()
    
    # Main content based on section
    if section == "Executive Summary":
        st.markdown('<div class="main-header">Instagram Reels Quick Edit Feature Analysis</div>', unsafe_allow_html=True)
        
        # Problem statement
        st.markdown("""
        ### 🎯 Problem Statement
        Instagram Reels creation suffers from a **42% drop-off rate** at the editing stage. 
        Casual creators find existing editing tools too complex, leading to abandoned content creation.
        
        ### 🚀 Solution Tested
        **Quick Edit Feature**: AI-powered one-tap editing that automatically syncs clips to audio and applies professional edits.
        
        ### 📊 Key Results
        """)
        
        create_kpi_metrics(data)
        
        # Recommendation
        st.markdown("""
        ### ✅ Recommendation
        **LAUNCH WITH PHASED ROLLOUT**
        
        1. **Week 1-2**: 10% rollout to iPhone casual creators (12.7% lift observed)
        2. **Week 3-4**: 50% rollout to iPhone users if metrics stable
        3. **Month 2**: 100% rollout to all casual creators
        4. **Month 3**: Optimize for Android (9.4% lift), then expand
        
        **Success Criteria**: 
        - Maintain ≥8% lift in creation success (vs 10.6% observed)
        - Quick Edit adoption ≥50% (vs 60% observed)
        - No negative impact on watch time or app crashes
        """)
        
    elif section == "A/B Test Results":
        st.markdown('<div class="main-header">A/B Test Statistical Analysis</div>', unsafe_allow_html=True)
        plot_ab_test_results(data['ab_results'])
        
        # Statistical significance
        st.markdown("""
        ### 📈 Statistical Significance Interpretation
        
        | Metric | Change | p-value | Interpretation |
        |--------|--------|---------|----------------|
        | Edit Tools Used | -0.6% | 0.0003 | ✅ **Positive** - Quick Edit is replacing manual editing |
        | Quick Edit Used | +60% | <0.0001 | ✅ **Excellent** - Strong feature appeal |
        | Session Duration | +0.1% | 0.5702 | ✅ **Neutral** - No negative UX impact |
        
        **Note**: All p-values < 0.05 indicate statistically significant results.
        """)
        
    elif section == "Funnel Analysis":
        st.markdown('<div class="main-header">Creation Funnel Analysis</div>', unsafe_allow_html=True)
        plot_funnel_analysis(data['funnel_overall'])
        
    elif section == "Business Impact":
        st.markdown('<div class="main-header">Business Impact Analysis</div>', unsafe_allow_html=True)
        plot_business_impact(data['business_impact'])
        
        # ROI calculation
        st.markdown("""
        ### 💰 ROI Calculation
        
        | Metric | Value |
        |--------|-------|
        | Monthly Revenue Impact | ${:,.0f} |
        | Engineering Cost | $500,000 |
        | Payback Period | **<1 month** |
        | Annualized ROI | **>2400%** |
        
        **Note**: Engineering cost includes development, testing, and deployment.
        """.format(data['business_impact']['monthly']['additional_revenue']))
        
    elif section == "Launch Strategy":
        st.markdown('<div class="main-header">Phased Launch Strategy</div>', unsafe_allow_html=True)
        plot_launch_strategy()
        
        # Risks and mitigations
        st.markdown("""
        ### ⚠️ Risks & Mitigations
        
        | Risk | Probability | Impact | Mitigation |
        |------|------------|--------|------------|
        | Lower Android adoption | Medium | Medium | Android-specific UX optimization |
        | Content quality decline | Low | High | Monitor watch time & negative feedback |
        | Feature fatigue | Low | Medium | Track 7-day, 30-day retention |
        | Infrastructure scaling | Low | Medium | Gradual rollout with monitoring |
        """)
        
    elif section == "Methodology":
        st.markdown('<div class="main-header">Methodology & Technical Details</div>', unsafe_allow_html=True)
        
        st.markdown("""
        ### 🧪 Experiment Design
        
        | Parameter | Value |
        |-----------|-------|
        | Experiment Type | A/B Test |
        | Population | 5% of Instagram users |
        | Duration | 14 days |
        | Sample Size | 500,000 user sessions |
        | Randomization | User-level |
        | Primary Metric | Creation success rate |
        
        ### 📊 Statistical Methods
        
        1. **Hypothesis Testing**: Two-sample t-test with Welch's correction
        2. **Confidence Intervals**: 95% using normal approximation
        3. **Power Analysis**: 80% power to detect 10% lift
        4. **Multiple Testing**: No correction needed (single primary metric)
        
        ### 💻 Technical Implementation
        
        ```python
        # Key analysis functions
        def analyze_ab_test(df, metric='successful_post'):
            control = df[df['variant'] == 'control'][metric]
            treatment = df[df['variant'] == 'treatment'][metric]
            
            # Calculate means and confidence intervals
            control_mean = control.mean()
            treatment_mean = treatment.mean()
            lift = (treatment_mean - control_mean) / control_mean
            
            # T-test for statistical significance
            t_stat, p_value = stats.ttest_ind(treatment, control, equal_var=False)
            
            return {
                'lift': lift,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        ```
        
        ### 📈 Data Sources
        
        - **Event Logs**: User interactions with Reels creation flow
        - **User Data**: Demographics, device type, creator cohort
        - **Performance Data**: Reels watch time, engagement metrics
        - **Experiment Data**: A/B test assignments and outcomes
        
        ### 🔗 Repository Structure
        
        ```
        instagram-reels-analysis/
        ├── data/           # Synthetic datasets
        ├── src/            # Analysis functions
        ├── notebooks/      # Jupyter analysis
        ├── dashboard/      # This Streamlit app
        └── results/        # Analysis outputs
        ```
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>📊 <strong>Instagram Reels Quick Edit Analysis</strong> | Meta-Style Product Analytics Portfolio Project</p>
    <p>📅 Last Updated: February 2026 | 👤 Analyst: Benjamin Ackah | 📧 Contact: ack.ben0226@gmail.com</p>
    <p><em>Note: This is a portfolio project with synthetic data for demonstration purposes.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
