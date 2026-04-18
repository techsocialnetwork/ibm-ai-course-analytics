"""
Visualizations Module

Creates interactive charts and visualizations for the course dashboard.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CourseVisualizer:
    """Create visualizations for course analytics."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize visualizer with course data.
        
        Args:
            df: DataFrame with course information
        """
        self.df = df
        self.color_palette = px.colors.qualitative.Set3
    
    def create_category_chart(self) -> go.Figure:
        """
        Create bar chart of courses by category.
        
        Returns:
            Plotly figure
        """
        category_counts = self.df['category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        
        fig = px.bar(
            category_counts,
            x='Category',
            y='Count',
            title='Courses by Category',
            color='Category',
            color_discrete_sequence=self.color_palette
        )
        
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Number of Courses",
            showlegend=False,
            height=400
        )
        
        return fig
    
    def create_completion_pie_chart(self) -> go.Figure:
        """
        Create pie chart of completion status.
        
        Returns:
            Plotly figure
        """
        status_counts = self.df['status'].value_counts()
        
        colors = {'Complete': '#2ecc71', 'In Progress': '#f39c12'}
        
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.4,
            marker_colors=[colors.get(s, '#95a5a6') for s in status_counts.index]
        )])
        
        fig.update_layout(
            title='Course Completion Status',
            annotations=[dict(text=f'{len(self.df)}<br>Courses', x=0.5, y=0.5, font_size=20, showarrow=False)],
            height=400
        )
        
        return fig
    
    def create_duration_chart(self) -> go.Figure:
        """
        Create histogram of course durations.
        
        Returns:
            Plotly figure
        """
        fig = px.histogram(
            self.df,
            x='duration_hours',
            nbins=10,
            title='Distribution of Course Durations',
            color='status',
            color_discrete_map={'Complete': '#2ecc71', 'In Progress': '#f39c12'}
        )
        
        fig.update_layout(
            xaxis_title="Duration (hours)",
            yaxis_title="Number of Courses",
            height=400
        )
        
        return fig
    
    def create_skills_wordcloud_data(self) -> pd.DataFrame:
        """
        Process skills data for visualization.
        
        Returns:
            DataFrame with skill frequencies
        """
        all_skills = []
        for skills_str in self.df['skills_covered'].dropna():
            skills = [s.strip() for s in skills_str.split(',')]
            all_skills.extend(skills)
        
        skill_counts = pd.Series(all_skills).value_counts().reset_index()
        skill_counts.columns = ['Skill', 'Count']
        
        return skill_counts.head(20)  # Top 20 skills
    
    def create_skills_bar_chart(self) -> go.Figure:
        """
        Create horizontal bar chart of top skills.
        
        Returns:
            Plotly figure
        """
        skill_counts = self.create_skills_wordcloud_data()
        
        fig = px.bar(
            skill_counts,
            y='Skill',
            x='Count',
            orientation='h',
            title='Top 20 Skills in Course Library',
            color='Count',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            xaxis_title="Number of Courses",
            yaxis_title="",
            height=600,
            yaxis=dict(autorange="reversed")
        )
        
        return fig
    
    def create_category_completion_heatmap(self) -> go.Figure:
        """
        Create heatmap of completion by category.
        
        Returns:
            Plotly figure
        """
        # Create completion matrix
        completion_data = []
        categories = self.df['category'].unique()
        
        for category in categories:
            cat_df = self.df[self.df['category'] == category]
            total = len(cat_df)
            completed = len(cat_df[cat_df['status'] == 'Complete'])
            in_progress = len(cat_df[cat_df['status'] == 'In Progress'])
            
            completion_data.append({
                'Category': category,
                'Complete': completed,
                'In Progress': in_progress,
                'Not Started': total - completed - in_progress,
                'Completion %': (completed / total * 100) if total > 0 else 0
            })
        
        completion_df = pd.DataFrame(completion_data)
        
        fig = px.imshow(
            completion_df[['Complete', 'In Progress']].T,
            x=completion_df['Category'],
            y=['Complete', 'In Progress'],
            title='Course Status by Category',
            color_continuous_scale='Greens',
            aspect='auto'
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_progress_gauge(self) -> go.Figure:
        """
        Create gauge chart showing overall progress.
        
        Returns:
            Plotly figure
        """
        completed = len(self.df[self.df['status'] == 'Complete'])
        total = len(self.df)
        percentage = (completed / total * 100) if total > 0 else 0
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Completion"},
            delta={'reference': 100, 'relative': False},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#2ecc71"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 25], 'color': '#ffcccc'},
                    {'range': [25, 50], 'color': '#ffffcc'},
                    {'range': [50, 75], 'color': '#ccffcc'},
                    {'range': [75, 100], 'color': '#99ff99'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_timeline_chart(self) -> go.Figure:
        """
        Create timeline of course completion (simulated).
        
        Returns:
            Plotly figure
        """
        completed_courses = self.df[self.df['status'] == 'Complete'].copy()
        
        if len(completed_courses) == 0:
            fig = go.Figure()
            fig.update_layout(title="No completed courses yet")
            return fig
        
        # Create simulated timeline
        completed_courses = completed_courses.sort_values('course_id')
        completed_courses['cumulative_hours'] = completed_courses['duration_hours'].cumsum()
        
        fig = px.area(
            completed_courses,
            x='course_id',
            y='cumulative_hours',
            title='Learning Journey: Cumulative Hours Completed',
            color_discrete_sequence=['#3498db']
        )
        
        fig.update_layout(
            xaxis_title="Courses Completed",
            yaxis_title="Cumulative Hours",
            height=400
        )
        
        return fig
    
    def create_dashboard_summary(self) -> Dict:
        """
        Create summary statistics for dashboard.
        
        Returns:
            Dictionary with key metrics
        """
        completed = len(self.df[self.df['status'] == 'Complete'])
        in_progress = len(self.df[self.df['status'] == 'In Progress'])
        total_hours = self.df['duration_hours'].sum()
        completed_hours = self.df[self.df['status'] == 'Complete']['duration_hours'].sum()
        
        # Get top skills
        all_skills = []
        for skills_str in self.df['skills_covered'].dropna():
            skills = [s.strip() for s in skills_str.split(',')]
            all_skills.extend(skills)
        top_skills = pd.Series(all_skills).value_counts().head(5).to_dict()
        
        return {
            'total_courses': len(self.df),
            'completed_courses': completed,
            'in_progress_courses': in_progress,
            'completion_rate': round(completed / len(self.df) * 100, 1),
            'total_hours': round(total_hours, 1),
            'completed_hours': round(completed_hours, 1),
            'hours_remaining': round(total_hours - completed_hours, 1),
            'categories': self.df['category'].nunique(),
            'top_skills': top_skills
        }


def main():
    """Example usage of CourseVisualizer."""
    from data_loader import CourseDataLoader
    
    # Load data
    loader = CourseDataLoader("data/raw/ibm_courses.csv")
    df = loader.load_data()
    
    # Create visualizer
    viz = CourseVisualizer(df)
    
    # Generate all charts
    print("Creating visualizations...")
    
    # Summary
    summary = viz.create_dashboard_summary()
    print("\n=== Dashboard Summary ===")
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    # Charts
    category_chart = viz.create_category_chart()
    completion_chart = viz.create_completion_pie_chart()
    duration_chart = viz.create_duration_chart()
    skills_chart = viz.create_skills_bar_chart()
    progress_gauge = viz.create_progress_gauge()
    
    print("\nVisualizations created successfully!")
    print("Run the Streamlit dashboard to view them interactively.")


if __name__ == "__main__":
    main()
