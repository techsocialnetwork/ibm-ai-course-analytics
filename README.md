# IBM AI Course Library Analytics

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **AI-powered analytics dashboard for IBM AI/ML course library**

This project analyzes 28 IBM AI/ML courses using generative AI to extract insights, visualize learning progress, and demonstrate data + AI capabilities.

## 🎯 Project Goals

- **Extract key skills** from course content using LLMs
- **Visualize learning progress** across categories
- **Generate personalized recommendations** using AI reasoning
- **Demonstrate AI + Data Analysis** capabilities for job applications

## 📊 Features

| Feature | Description | Skills Demonstrated |
|---------|-------------|---------------------|
| **Course Categorization** | Interactive charts of courses by type | Data visualization, pandas |
| **AI-Generated Summaries** | LLM-powered course summaries | Prompt engineering, API integration |
| **Skills Extraction** | NLP analysis of course content | Text analysis, NLP |
| **Learning Path Builder** | AI-driven course recommendations | AI reasoning, data-driven suggestions |
| **Progress Tracker** | Personal learning dashboard | UI design, data processing |

## 🛠️ Tech Stack

- **Data Processing:** Python, Pandas, NumPy
- **AI/LLM:** OpenAI API / IBM Watsonx
- **Visualization:** Streamlit, Plotly
- **Testing:** Pytest
- **Deployment:** Streamlit Cloud / GitHub Pages

## 📁 Project Structure

```
ibm-ai-course-analytics/
├── data/                   # Course data and processed outputs
│   ├── raw/               # Raw course data
│   └── processed/         # AI-enhanced course data
├── src/                   # Source code
│   ├── data_loader.py     # Data loading and cleaning
│   ├── ai_analyzer.py     # LLM integration for analysis
│   ├── visualizations.py  # Chart generation
│   └── dashboard.py       # Streamlit app
├── notebooks/             # Jupyter notebooks for exploration
├── assets/                # Images, logos, static files
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key (or IBM Watsonx credentials)

### Installation

```bash
# Clone the repository
git clone https://github.com/techsocialnetwork/ibm-ai-course-analytics.git
cd ibm-ai-course-analytics

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Running the Dashboard

```bash
# Launch Streamlit app
streamlit run src/dashboard.py
```

The dashboard will be available at `http://localhost:8501`

## 📚 Course Library

This project analyzes courses from:

- **IBM AI Foundations for Business** (27 courses completed)
- **Generative AI Fundamentals Specialization** (in progress)

### Course Categories

- Core Technical (Machine Learning, Deep Learning, NLP, Computer Vision)
- Advanced AI (AI Agents, Multi-Agent Systems)
- Applications (Self-Driving Cars, Robotics)
- Business Strategy (AI Adoption, Frameworks)
- Ethics & Governance (AI Ethics, Governance, Hallucinations)
- Practical/Lab (Hands-on implementations)

## 💡 Key Insights Generated

The dashboard provides:

1. **Skills Coverage Analysis** — What skills you've gained
2. **Learning Gaps** — Areas for further study
3. **Career Alignment** — Which roles match your skill profile
4. **Recommended Next Steps** — AI-generated learning path

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📝 About the Author

**Background:** Data professional with IBM AI Foundations certification

**Specializations:**
- AI Ethics & Governance (6 courses)
- Generative AI Fundamentals (in progress)
- Machine Learning & Deep Learning
- NLP, Computer Vision, AI Agents

**Connect:** [LinkedIn](your-linkedin-url) | [GitHub](https://github.com/techsocialnetwork)

## 📄 License

MIT License - feel free to use this project as a template for your own course analytics!

## 🙏 Acknowledgments

- IBM for the comprehensive AI curriculum
- OpenAI / IBM Watsonx for LLM capabilities
- Streamlit for the amazing dashboard framework

---

**Status:** 🚧 Work in Progress - Building in public

*Last updated: April 2026*
