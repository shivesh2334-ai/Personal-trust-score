import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Physician Self-Assessment Tool",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .category-header {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .score-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3498db;
        margin: 1rem 0;
    }
    .recommendation {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Assessment questions
QUESTIONS = {
    "Personal Connect (Do You Care About Me?)": [
        {
            "question": "How often do you call patients by name and make personal contact?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "question": "Do you sit down with patients (not standing) during consultations?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "question": "How frequently do you telephone patients to check on them after procedures or missed appointments?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "question": "Do you show empathy and listen actively to patients' stories?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "question": "How often do you discuss patients' personal life, hobbies, likes, and dislikes?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        }
    ],
    "Trust of Your Trade (Are You the Best?)": [
        {
            "question": "How regularly do you attend lectures and national meetings?",
            "options": ["Never", "Once a year", "2-3 times/year", "Quarterly", "Monthly or more"]
        },
        {
            "question": "How often do you read the latest research in your area of practice?",
            "options": ["Never", "Rarely", "Monthly", "Weekly", "Daily"]
        },
        {
            "question": "Do you pursue continuing medical education and skill development?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Consistently"]
        },
        {
            "question": "How confident are you in acknowledging when you need refreshers in certain areas?",
            "options": ["Not confident", "Slightly confident", "Moderately confident", "Very confident", "Extremely confident"]
        },
        {
            "question": "Do you strive for excellence beyond just avoiding malpractice?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        }
    ],
    "Social Trust (Can I Trust You?)": [
        {
            "question": "How much time do you invest in building trust with patients from different backgrounds?",
            "options": ["No effort", "Minimal effort", "Moderate effort", "Significant effort", "Maximum effort"]
        },
        {
            "question": "Do you create a safe environment for patients to share sensitive issues (substance use, mental health)?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "question": "How reliable are you in following up on patient concerns?",
            "options": ["Unreliable", "Somewhat reliable", "Moderately reliable", "Very reliable", "Completely reliable"]
        },
        {
            "question": "Do you demonstrate care about patients' wellbeing in your actions?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        },
        {
            "question": "How well do you encourage patients to share when they're feeling sad, depressed, or lonely?",
            "options": ["Not at all", "Poorly", "Adequately", "Well", "Excellently"]
        }
    ],
    "Treating Style (Are You Treating Me Differently?)": [
        {
            "question": "How conscious are you of health disparities affecting different populations?",
            "options": ["Not conscious", "Slightly conscious", "Moderately conscious", "Very conscious", "Extremely conscious"]
        },
        {
            "question": "Do you examine your own biases regarding race, ethnicity, sex, or socioeconomic status?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Regularly"]
        },
        {
            "question": "How carefully do you ensure equitable treatment across all patient demographics?",
            "options": ["Not carefully", "Somewhat carefully", "Moderately carefully", "Very carefully", "Extremely carefully"]
        },
        {
            "question": "Do you stay informed about social determinants of health?",
            "options": ["Not informed", "Slightly informed", "Moderately informed", "Well informed", "Expert level"]
        },
        {
            "question": "How often do you reflect on whether you might be perceived as judging patients?",
            "options": ["Never", "Rarely", "Sometimes", "Often", "Always"]
        }
    ]
}

# Scoring and recommendations
def calculate_scores(responses):
    category_scores = {}
    for category, answers in responses.items():
        # Each answer is 0-4, convert to 0-5 scale
        total = sum(answers)
        max_possible = len(answers) * 4
        category_scores[category] = (total / max_possible) * 5 if max_possible > 0 else 0
    
    overall_score = sum(category_scores.values()) / len(category_scores) if category_scores else 0
    return category_scores, overall_score

def get_recommendations(category_scores, overall_score):
    recommendations = []
    
    # Overall assessment
    if overall_score >= 4.5:
        recommendations.append({
            "level": "Excellent",
            "message": "You demonstrate exceptional patient-centered care across all dimensions. Continue your excellent work!"
        })
    elif overall_score >= 3.5:
        recommendations.append({
            "level": "Good",
            "message": "You show strong patient care skills. Focus on the areas below to reach excellence."
        })
    elif overall_score >= 2.5:
        recommendations.append({
            "level": "Fair",
            "message": "You have a foundation to build on. Significant improvement needed in several areas."
        })
    else:
        recommendations.append({
            "level": "Needs Improvement",
            "message": "Your patient care approach needs substantial development. Prioritize the recommendations below."
        })
    
    # Category-specific recommendations
    for category, score in category_scores.items():
        if score < 4.0:
            if "Personal Connect" in category:
                recommendations.append({
                    "category": category,
                    "score": score,
                    "actions": [
                        "Make it a habit to sit down during patient consultations",
                        "Call patients by name and ask about their personal interests",
                        "Set reminders to follow up with patients after procedures",
                        "Practice active listening - let patients finish their stories",
                        "Schedule slightly longer appointments to allow for personal connection"
                    ]
                })
            elif "Trust of Your Trade" in category:
                recommendations.append({
                    "category": category,
                    "score": score,
                    "actions": [
                        "Subscribe to key journals in your specialty",
                        "Register for at least 2-3 conferences per year",
                        "Join a journal club or peer learning group",
                        "Set aside 30 minutes weekly for reading latest research",
                        "Pursue additional certifications or CME credits"
                    ]
                })
            elif "Social Trust" in category:
                recommendations.append({
                    "category": category,
                    "score": score,
                    "actions": [
                        "Create protocols for discussing sensitive topics (substance use, mental health)",
                        "Use open-ended questions to encourage patient sharing",
                        "Demonstrate reliability by following up on every concern",
                        "Build rapport before diving into medical history",
                        "Show genuine concern through both words and actions"
                    ]
                })
            elif "Treating Style" in category:
                recommendations.append({
                    "category": category,
                    "score": score,
                    "actions": [
                        "Take implicit bias training",
                        "Study health disparities in your patient population",
                        "Regularly self-reflect on your treatment decisions across demographics",
                        "Learn about social determinants of health",
                        "Develop cultural competence through education and exposure"
                    ]
                })
    
    return recommendations

def create_score_chart(category_scores):
    categories = list(category_scores.keys())
    scores = list(category_scores.values())
    
    # Shorten category names for display
    short_categories = [
        "Personal\nConnect",
        "Trust of\nTrade",
        "Social\nTrust",
        "Treating\nStyle"
    ]
    
    fig = go.Figure()
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=short_categories,
        y=scores,
        marker_color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],
        text=[f'{score:.2f}' for score in scores],
        textposition='outside'
    ))
    
    # Add reference line at 4.0
    fig.add_hline(y=4.0, line_dash="dash", line_color="green", 
                  annotation_text="Excellence Threshold (4.0)")
    
    fig.update_layout(
        title="Your Professional Score by Category",
        yaxis_title="Score (0-5)",
        yaxis_range=[0, 5.5],
        height=400,
        showlegend=False
    )
    
    return fig

def create_radar_chart(category_scores):
    categories = ["Personal\nConnect", "Trust of\nTrade", "Social\nTrust", "Treating\nStyle"]
    scores = list(category_scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],  # Close the polygon
        theta=categories + [categories[0]],
        fill='toself',
        name='Your Scores',
        line_color='#3498db'
    ))
    
    # Add ideal score reference
    fig.add_trace(go.Scatterpolar(
        r=[5, 5, 5, 5, 5],
        theta=categories + [categories[0]],
        fill='toself',
        name='Ideal Score',
        line_color='#2ecc71',
        opacity=0.3
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=True,
        height=400,
        title="Professional Profile Radar"
    )
    
    return fig

# Main app
def main():
    st.markdown('<h1 class="main-header">🏥 Physician Professional Self-Assessment</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### About This Assessment
    Based on the article **"5 Questions Patients Have but Never Ask"** (JAMA Neurology, 2018), 
    this tool helps physicians evaluate their patient-centered care across four critical dimensions.
    
    **Instructions:** Rate yourself honestly on each question using the scale provided (0-5 points per question).
    """)
    
    # Initialize session state
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    
    # Assessment form
    if not st.session_state.submitted:
        with st.form("assessment_form"):
            st.markdown("---")
            
            for category, questions in QUESTIONS.items():
                st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
                
                category_responses = []
                for i, q in enumerate(questions):
                    response = st.radio(
                        q["question"],
                        options=range(len(q["options"])),
                        format_func=lambda x, opts=q["options"]: opts[x],
                        key=f"{category}_{i}",
                        horizontal=False
                    )
                    category_responses.append(response)
                
                st.session_state.responses[category] = category_responses
                st.markdown("---")
            
            submitted = st.form_submit_button("📊 Calculate My Professional Score", use_container_width=True)
            
            if submitted:
                st.session_state.submitted = True
                st.rerun()
    
    # Results display
    if st.session_state.submitted:
        category_scores, overall_score = calculate_scores(st.session_state.responses)
        recommendations = get_recommendations(category_scores, overall_score)
        
        # Overall Score
        st.markdown("## 🎯 Your Assessment Results")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="score-card" style="text-align: center;">
                <h2>Overall Professional Score</h2>
                <h1 style="color: #3498db; font-size: 4rem; margin: 0;">{overall_score:.2f}</h1>
                <h3 style="color: #7f8c8d;">out of 5.0</h3>
                <p style="font-size: 1.2rem; margin-top: 1rem;">
                    <strong>Level: {recommendations[0]['level']}</strong>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(create_score_chart(category_scores), use_container_width=True)
        
        with col2:
            st.plotly_chart(create_radar_chart(category_scores), use_container_width=True)
        
        st.markdown("---")
        
        # Category breakdown
        st.markdown("## 📋 Category Breakdown")
        
        cols = st.columns(4)
        for i, (category, score) in enumerate(category_scores.items()):
            with cols[i]:
                short_name = category.split("(")[0].strip()
                color = "#2ecc71" if score >= 4.0 else "#f39c12" if score >= 3.0 else "#e74c3c"
                st.markdown(f"""
                <div style="background-color: {color}; padding: 1rem; border-radius: 10px; text-align: center; color: white;">
                    <h4 style="margin: 0; color: white;">{short_name}</h4>
                    <h2 style="margin: 0.5rem 0; color: white;">{score:.2f}/5.0</h2>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Recommendations
        st.markdown("## 💡 Personalized Recommendations")
        
        st.markdown(f"""
        <div class="recommendation">
            <h3>Overall Assessment: {recommendations[0]['level']}</h3>
            <p>{recommendations[0]['message']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        for rec in recommendations[1:]:
            with st.expander(f"🎯 {rec['category']} - Score: {rec['score']:.2f}/5.0"):
                st.markdown("### Action Items to Improve:")
                for action in rec['actions']:
                    st.markdown(f"- {action}")
        
        st.markdown("---")
        
        # Export results
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download Results as JSON", use_container_width=True):
                results = {
                    "timestamp": datetime.now().isoformat(),
                    "overall_score": overall_score,
                    "category_scores": category_scores,
                    "responses": st.session_state.responses
                }
                st.download_button(
                    label="Click to Download",
                    data=json.dumps(results, indent=2),
                    file_name=f"physician_assessment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Take Assessment Again", use_container_width=True):
                st.session_state.submitted = False
                st.session_state.responses = {}
                st.rerun()

if __name__ == "__main__":
    main()
