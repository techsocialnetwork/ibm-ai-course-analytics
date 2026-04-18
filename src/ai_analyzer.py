"""
AI Analyzer Module

Uses LLMs (OpenAI or IBM Watsonx) to analyze course content and extract insights.
"""

import os
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
import pandas as pd

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI package not installed. OpenAI features will be disabled.")

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CourseAnalysis:
    """Structure for AI-analyzed course data."""
    course_id: int
    key_takeaways: List[str]
    practical_applications: List[str]
    career_relevance: str
    skill_level: str  # Beginner, Intermediate, Advanced
    recommended_prerequisites: List[str]
    related_courses: List[str]


class AICourseAnalyzer:
    """Analyze courses using LLM APIs."""
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize the AI analyzer.
        
        Args:
            provider: 'openai' or 'watsonx'
        """
        self.provider = provider
        self.client = None
        
        if provider == "openai":
            self._init_openai()
        elif provider == "watsonx":
            self._init_watsonx()
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def _init_openai(self):
        """Initialize OpenAI client."""
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        logger.info(f"Initialized OpenAI client with model: {self.model}")
    
    def _init_watsonx(self):
        """Initialize IBM Watsonx client."""
        # Placeholder for Watsonx implementation
        logger.warning("Watsonx implementation is a placeholder")
        raise NotImplementedError("Watsonx support coming soon")
    
    def analyze_course(self, course_title: str, description: str, 
                       skills: str, category: str) -> CourseAnalysis:
        """
        Analyze a single course using LLM.
        
        Args:
            course_title: Name of the course
            description: Course description
            skills: Skills covered (comma-separated)
            category: Course category
            
        Returns:
            CourseAnalysis object with AI-generated insights
        """
        prompt = f"""
        Analyze this IBM AI course and provide structured insights:
        
        Course Title: {course_title}
        Category: {category}
        Skills Covered: {skills}
        Description: {description}
        
        Provide a JSON response with the following structure:
        {{
            "key_takeaways": ["3-5 bullet points of main learning outcomes"],
            "practical_applications": ["2-3 real-world use cases"],
            "career_relevance": "How this course helps career (1-2 sentences)",
            "skill_level": "Beginner/Intermediate/Advanced",
            "recommended_prerequisites": ["Any recommended prior knowledge"],
            "related_courses": ["Names of related courses"]
        }}
        
        Be concise and specific. Focus on actionable insights.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI curriculum analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON response
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # Try to extract JSON if wrapped in markdown
                import re
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(1))
                else:
                    raise
            
            return CourseAnalysis(
                course_id=0,  # Will be set by caller
                key_takeaways=data.get("key_takeaways", []),
                practical_applications=data.get("practical_applications", []),
                career_relevance=data.get("career_relevance", ""),
                skill_level=data.get("skill_level", "Intermediate"),
                recommended_prerequisites=data.get("recommended_prerequisites", []),
                related_courses=data.get("related_courses", [])
            )
            
        except Exception as e:
            logger.error(f"Error analyzing course '{course_title}': {e}")
            # Return default analysis on error
            return CourseAnalysis(
                course_id=0,
                key_takeaways=["Analysis failed"],
                practical_applications=["N/A"],
                career_relevance="N/A",
                skill_level="Intermediate",
                recommended_prerequisites=[],
                related_courses=[]
            )
    
    def analyze_all_courses(self, df: pd.DataFrame, 
                           output_path: str = "data/processed/courses_ai_analyzed.json") -> pd.DataFrame:
        """
        Analyze all courses and save results.
        
        Args:
            df: DataFrame with course data
            output_path: Path to save analysis results
            
        Returns:
            DataFrame with added AI analysis columns
        """
        logger.info(f"Analyzing {len(df)} courses...")
        
        analyses = []
        for idx, row in df.iterrows():
            logger.info(f"Analyzing: {row['course_title']}")
            
            analysis = self.analyze_course(
                course_title=row['course_title'],
                description=row['description'],
                skills=row['skills_covered'],
                category=row['category']
            )
            analysis.course_id = row['course_id']
            analyses.append(analysis)
        
        # Convert to DataFrame columns
        df['ai_key_takeaways'] = [a.key_takeaways for a in analyses]
        df['ai_practical_applications'] = [a.practical_applications for a in analyses]
        df['ai_career_relevance'] = [a.career_relevance for a in analyses]
        df['ai_skill_level'] = [a.skill_level for a in analyses]
        df['ai_prerequisites'] = [a.recommended_prerequisites for a in analyses]
        df['ai_related_courses'] = [a.related_courses for a in analyses]
        
        # Save as JSON
        import json
        output_data = []
        for a in analyses:
            output_data.append({
                'course_id': a.course_id,
                'key_takeaways': a.key_takeaways,
                'practical_applications': a.practical_applications,
                'career_relevance': a.career_relevance,
                'skill_level': a.skill_level,
                'prerequisites': a.recommended_prerequisites,
                'related_courses': a.related_courses
            })
        
        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        logger.info(f"Saved AI analysis to {output_path}")
        return df
    
    def generate_learning_path(self, career_goal: str, 
                               current_skills: List[str]) -> Dict:
        """
        Generate a personalized learning path based on career goals.
        
        Args:
            career_goal: Target role (e.g., "AI Product Manager")
            current_skills: List of skills already possessed
            
        Returns:
            Dictionary with recommended courses and rationale
        """
        prompt = f"""
        Based on the IBM AI course library, create a personalized learning path.
        
        Career Goal: {career_goal}
        Current Skills: {', '.join(current_skills)}
        
        Available course categories:
        - Core Technical (ML, DL, NLP, Computer Vision)
        - Advanced AI (AI Agents, Multi-Agent Systems)
        - Applications (Self-Driving Cars, Robotics)
        - Business Strategy (AI Adoption, Frameworks)
        - Ethics & Governance (AI Ethics, Governance)
        - Practical/Lab (Hands-on implementations)
        
        Provide a JSON response:
        {{
            "recommended_path": [
                {{
                    "phase": "Phase 1: Foundation",
                    "courses": ["Course names"],
                    "rationale": "Why these courses"
                }}
            ],
            "estimated_time": "Total hours",
            "key_skills_gained": ["Skills from this path"],
            "career_readiness": "How this prepares for the role"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI career advisor."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Parse JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                else:
                    return {"raw_response": content}
                    
        except Exception as e:
            logger.error(f"Error generating learning path: {e}")
            return {"error": str(e)}
    
    def extract_all_skills(self, df: pd.DataFrame) -> Dict[str, int]:
        """
        Extract and count all skills from course library using AI.
        
        Args:
            df: DataFrame with course data
            
        Returns:
            Dictionary of skills and their frequency
        """
        all_skills_text = "\n".join(df['skills_covered'].dropna())
        
        prompt = f"""
        Extract and categorize all technical skills from this list:
        
        {all_skills_text}
        
        Provide a JSON response:
        {{
            "skills_by_category": {{
                "Machine Learning": ["skill1", "skill2"],
                "Deep Learning": ["skill3"],
                "NLP": ["skill4", "skill5"],
                "Computer Vision": ["skill6"],
                "AI Ethics": ["skill7"],
                "Tools & Platforms": ["skill8"]
            }},
            "top_skills": ["Most important 10 skills overall"],
            "emerging_skills": ["New/trending skills"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical skills analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error extracting skills: {e}")
            return {"error": str(e)}


def main():
    """Example usage of AICourseAnalyzer."""
    from data_loader import CourseDataLoader
    
    # Load data
    loader = CourseDataLoader()
    df = loader.load_data()
    
    # Initialize analyzer
    try:
        analyzer = AICourseAnalyzer(provider="openai")
        
        # Analyze a single course
        print("\n=== Analyzing Single Course ===")
        sample_course = df.iloc[0]
        analysis = analyzer.analyze_course(
            course_title=sample_course['course_title'],
            description=sample_course['description'],
            skills=sample_course['skills_covered'],
            category=sample_course['category']
        )
        print(f"Course: {sample_course['course_title']}")
        print(f"Key Takeaways: {analysis.key_takeaways}")
        print(f"Career Relevance: {analysis.career_relevance}")
        
        # Generate learning path
        print("\n=== Generating Learning Path ===")
        path = analyzer.generate_learning_path(
            career_goal="AI Product Manager",
            current_skills=["Data Analysis", "Python", "SQL"]
        )
        print(json.dumps(path, indent=2))
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print("Make sure OPENAI_API_KEY is set in your .env file")


if __name__ == "__main__":
    main()
