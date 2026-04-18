"""
Streamlit Dashboard

Interactive dashboard for IBM AI Course Library Analytics.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from data_loader import CourseDataLoader
from visualizations import CourseVisualizer

# Page configuration
st.set_page_config(
    page_title="IBM AI Course Analytics",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        color: #000000;
    }
    .skill-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #1f77b4;
        text-align: center;
        color: #000000;
    }
    .skill-tag {
        background-color: #e1e8ed;
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem;
        display: inline-block;
        font-size: 0.875rem;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache course data."""
    loader = CourseDataLoader("data/raw/ibm_courses.csv")
    return loader.load_data()


def main():
    """Main dashboard application."""
    
    # Header
    st.markdown('<p class="main-header">📚 IBM AI Course Library Analytics</p>', unsafe_allow_html=True)
    st.markdown("AI-powered analysis of IBM AI/ML certification journey")
    
    # Load data
    try:
        df = load_data()
        viz = CourseVisualizer(df)
        summary = viz.create_dashboard_summary()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure data/raw/ibm_courses.csv exists")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Select View",
            ["Overview", "Courses", "Skills", "Progress", "AI Insights"]
        )
        
        st.header("Filters")
        selected_category = st.multiselect(
            "Category",
            options=df['category'].unique(),
            default=[]
        )
        
        selected_status = st.multiselect(
            "Status",
            options=df['status'].unique(),
            default=[]
        )
        
        # Filter data
        filtered_df = df.copy()
        if selected_category:
            filtered_df = filtered_df[filtered_df['category'].isin(selected_category)]
        if selected_status:
            filtered_df = filtered_df[filtered_df['status'].isin(selected_status)]
    
    # Main content based on page selection
    if page == "Overview":
        show_overview(viz, summary, filtered_df)
    elif page == "Courses":
        show_courses(filtered_df)
    elif page == "Skills":
        show_skills(viz, filtered_df)
    elif page == "Progress":
        show_progress(viz, filtered_df)
    elif page == "AI Insights":
        show_ai_insights(filtered_df)


def show_overview(viz, summary, df):
    """Display overview dashboard."""
    
    st.subheader("📊 At a Glance")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Courses", summary['total_courses'])
    with col2:
        st.metric("Completed", f"{summary['completed_courses']} ({summary['completion_rate']}%)")
    with col3:
        st.metric("Hours Completed", f"{summary['completed_hours']}h")
    with col4:
        st.metric("Hours Remaining", f"{summary['hours_remaining']}h")
    
    st.divider()
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(viz.create_category_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(viz.create_completion_pie_chart(), use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(viz.create_progress_gauge(), use_container_width=True)
    
    with col2:
        st.plotly_chart(viz.create_duration_chart(), use_container_width=True)
    
    # Top skills
    st.subheader("🔥 Top Skills Covered")
    skills_cols = st.columns(5)
    for i, (skill, count) in enumerate(list(summary['top_skills'].items())[:5]):
        with skills_cols[i]:
            st.markdown(f"<div class='skill-card'><strong>{skill}</strong><br>{count} courses</div>", 
                       unsafe_allow_html=True)


def show_courses(df):
    """Display courses table and details."""
    
    st.subheader("📖 Course Library")
    
    # Search
    search = st.text_input("Search courses", "")
    if search:
        df = df[df['course_title'].str.contains(search, case=False) | 
                df['description'].str.contains(search, case=False)]
    
    # Display table
    st.dataframe(
        df[['course_title', 'category', 'type', 'status', 'duration_hours', 'skills_covered']],
        use_container_width=True,
        hide_index=True
    )
    
    # Course details expander
    st.subheader("Course Details")
    selected_course = st.selectbox("Select a course", df['course_title'])
    
    if selected_course:
        course = df[df['course_title'] == selected_course].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Category:** {course['category']}")
            st.markdown(f"**Type:** {course['type']}")
            st.markdown(f"**Status:** {course['status']}")
            st.markdown(f"**Duration:** {course['duration_hours']} hours")
        with col2:
            st.markdown("**Skills:**")
            for skill in course['skills_covered'].split(','):
                st.markdown(f"<span class='skill-tag'>{skill.strip()}</span>", 
                           unsafe_allow_html=True)
        
        st.markdown("**Description:**")
        st.info(course['description'])


def show_skills(viz, df):
    """Display skills analysis."""
    
    st.subheader("🎯 Skills Analysis")
    
    # Skills chart
    st.plotly_chart(viz.create_skills_bar_chart(), use_container_width=True)
    
    # All skills
    st.subheader("All Skills by Category")
    
    skills_by_category = {}
    for _, row in df.iterrows():
        category = row['category']
        skills = [s.strip() for s in row['skills_covered'].split(',')]
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].extend(skills)
    
    for category, skills in skills_by_category.items():
        with st.expander(f"{category} ({len(set(skills))} unique skills)"):
            unique_skills = sorted(set(skills))
            cols = st.columns(4)
            for i, skill in enumerate(unique_skills):
                cols[i % 4].markdown(f"• {skill}")


def show_progress(viz, df):
    """Display progress tracking."""
    
    st.subheader("📈 Learning Progress")
    
    # Progress charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(viz.create_category_completion_heatmap(), use_container_width=True)
    
    with col2:
        st.plotly_chart(viz.create_timeline_chart(), use_container_width=True)
    
    # Category progress
    st.subheader("Progress by Category")
    
    for category in df['category'].unique():
        cat_df = df[df['category'] == category]
        completed = len(cat_df[cat_df['status'] == 'Complete'])
        total = len(cat_df)
        percentage = (completed / total * 100) if total > 0 else 0
        
        st.progress(percentage / 100, text=f"{category}: {completed}/{total} ({percentage:.0f}%)")


def show_ai_insights(df):
    """Display AI-generated insights."""
    
    st.subheader("🤖 AI-Powered Insights")
    
    st.info("AI analysis features require OpenAI API key configuration")
    
    # Placeholder for AI features
    st.markdown("""
    ### Coming Soon:
    
    1. **AI-Generated Course Summaries** — LLM-powered key takeaways for each course
    2. **Personalized Learning Paths** — AI-recommended course sequences based on career goals
    3. **Skills Gap Analysis** — Identify missing skills for target roles
    4. **Career Alignment** — Match your profile to AI job descriptions
    
    ### To Enable:
    
    1. Set your `OPENAI_API_KEY` in `.env`
    2. Run: `python src/ai_analyzer.py`
    3. Refresh this dashboard
    """)
    
    # Demo section
    st.subheader("Sample AI Analysis")
    
    sample_course = df.iloc[0]
    st.markdown(f"**Course:** {sample_course['course_title']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**AI-Generated Key Takeaways:**")
        st.markdown("• Understanding of core concepts")
        st.markdown("• Practical application skills")
        st.markdown("• Industry best practices")
    with col2:
        st.markdown("**Career Relevance:**")
        st.markdown("Foundation for AI/ML roles requiring this expertise")


if __name__ == "__main__":
    main()
