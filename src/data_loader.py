"""
Data Loader Module

Handles loading, cleaning, and preprocessing of IBM course data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CourseDataLoader:
    """Load and preprocess IBM AI course data."""
    
    def __init__(self, data_path: str = "data/raw/ibm_courses.csv"):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the CSV file containing course data
        """
        self.data_path = Path(data_path)
        self.df: Optional[pd.DataFrame] = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load course data from CSV file.
        
        Returns:
            DataFrame containing course information
        """
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Loaded {len(self.df)} courses from {self.data_path}")
            return self.df
        except FileNotFoundError:
            logger.error(f"File not found: {self.data_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def get_course_stats(self) -> Dict:
        """
        Calculate basic statistics about the course library.
        
        Returns:
            Dictionary containing course statistics
        """
        if self.df is None:
            self.load_data()
            
        stats = {
            'total_courses': len(self.df),
            'completed_courses': len(self.df[self.df['status'] == 'Complete']),
            'in_progress_courses': len(self.df[self.df['status'] == 'In Progress']),
            'total_hours': self.df['duration_hours'].sum(),
            'avg_duration': self.df['duration_hours'].mean(),
            'categories': self.df['category'].nunique(),
            'types': self.df['type'].nunique()
        }
        
        return stats
    
    def get_courses_by_category(self) -> pd.DataFrame:
        """
        Group courses by category with counts and total hours.
        
        Returns:
            DataFrame with category statistics
        """
        if self.df is None:
            self.load_data()
            
        category_stats = self.df.groupby('category').agg({
            'course_id': 'count',
            'duration_hours': 'sum',
            'status': lambda x: (x == 'Complete').sum()
        }).rename(columns={
            'course_id': 'course_count',
            'duration_hours': 'total_hours',
            'status': 'completed'
        })
        
        return category_stats.sort_values('course_count', ascending=False)
    
    def get_skills_list(self) -> List[str]:
        """
        Extract all unique skills from the course library.
        
        Returns:
            List of unique skills
        """
        if self.df is None:
            self.load_data()
            
        all_skills = []
        for skills_str in self.df['skills_covered'].dropna():
            skills = [s.strip() for s in skills_str.split(',')]
            all_skills.extend(skills)
            
        return sorted(list(set(all_skills)))
    
    def get_courses_by_skill(self, skill: str) -> pd.DataFrame:
        """
        Find courses that cover a specific skill.
        
        Args:
            skill: Skill to search for
            
        Returns:
            DataFrame of courses covering the skill
        """
        if self.df is None:
            self.load_data()
            
        mask = self.df['skills_covered'].str.contains(skill, case=False, na=False)
        return self.df[mask][['course_title', 'category', 'status', 'duration_hours']]
    
    def get_completion_progress(self) -> Dict:
        """
        Calculate completion progress by category.
        
        Returns:
            Dictionary with completion statistics
        """
        if self.df is None:
            self.load_data()
            
        progress = {}
        for category in self.df['category'].unique():
            cat_df = self.df[self.df['category'] == category]
            total = len(cat_df)
            completed = len(cat_df[cat_df['status'] == 'Complete'])
            progress[category] = {
                'total': total,
                'completed': completed,
                'percentage': (completed / total * 100) if total > 0 else 0
            }
            
        return progress
    
    def export_for_analysis(self, output_path: str = "data/processed/courses_processed.csv"):
        """
        Export processed data for AI analysis.
        
        Args:
            output_path: Path to save processed data
        """
        if self.df is None:
            self.load_data()
            
        # Add derived columns
        df_export = self.df.copy()
        df_export['skills_list'] = df_export['skills_covered'].apply(
            lambda x: [s.strip() for s in str(x).split(',')] if pd.notna(x) else []
        )
        df_export['is_complete'] = df_export['status'] == 'Complete'
        df_export['is_in_progress'] = df_export['status'] == 'In Progress'
        
        # Save
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df_export.to_csv(output_path, index=False)
        logger.info(f"Exported processed data to {output_path}")
        
        return df_export


def main():
    """Example usage of CourseDataLoader."""
    loader = CourseDataLoader()
    
    # Load data
    df = loader.load_data()
    print(f"\nLoaded {len(df)} courses")
    print(f"\nColumns: {list(df.columns)}")
    
    # Get stats
    stats = loader.get_course_stats()
    print(f"\n=== Course Statistics ===")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Get category breakdown
    print(f"\n=== Courses by Category ===")
    cat_stats = loader.get_courses_by_category()
    print(cat_stats)
    
    # Get skills
    skills = loader.get_skills_list()
    print(f"\n=== Total Unique Skills: {len(skills)} ===")
    print(f"Sample skills: {skills[:10]}")
    
    # Export for analysis
    loader.export_for_analysis()


if __name__ == "__main__":
    main()
