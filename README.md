cd /home/claude && cat > README.md << 'EOF'
# 🏥 Physician Professional Self-Assessment Tool

A comprehensive self-assessment application for physicians to evaluate their patient-centered care skills based on the JAMA Neurology article "5 Questions Patients Have but Never Ask" (2018).

## 📋 Overview

This tool helps physicians assess themselves across four critical dimensions of patient care:

1. **Personal Connect** - Do You Care About Me?
2. **Trust of Your Trade** - Are You the Best?
3. **Social Trust** - Can I Trust You?
4. **Treating Style** - Are You Treating Me Differently?

## 🌟 Features

- **Interactive Assessment**: 20 carefully crafted questions across 4 categories
- **Scoring System**: 0-5 scale for each category and overall performance
- **Visual Analytics**: 
  - Bar charts showing category scores
  - Radar charts for professional profile visualization
- **Personalized Recommendations**: Actionable steps to improve in each area
- **Progress Tracking**: Download results in JSON format
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Local Deployment

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/physician-assessment-tool.git
cd physician-assessment-tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser**
Navigate to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Deploy your app**:
   - Click "New app"
   - Select your forked repository
   - Set main file path: `app.py`
   - Click "Deploy"

4. **Your app will be live** at `https://[your-app-name].streamlit.app`

## 📊 How It Works

### Assessment Process

1. **Answer 20 Questions**: Rate yourself on each question using a 0-4 scale
2. **Calculate Scores**: Each category receives a score out of 5.0
3. **Review Results**: See your overall score and category breakdowns
4. **Get Recommendations**: Receive personalized action items for improvement

### Scoring Scale

- **4.5 - 5.0**: Excellent - Exceptional patient-centered care
- **3.5 - 4.4**: Good - Strong skills with room for improvement
- **2.5 - 3.4**: Fair - Foundation to build on
- **0.0 - 2.4**: Needs Improvement - Substantial development needed

### Categories Explained

#### 1. Personal Connect (Do You Care About Me?)
Evaluates how well you demonstrate personal care and empathy for patients as individuals.

**Key Areas**:
- Calling patients by name
- Sitting down during consultations
- Following up with patients
- Active listening
- Discussing personal interests

#### 2. Trust of Your Trade (Are You the Best?)
Assesses your commitment to professional excellence and continuing education.

**Key Areas**:
- Attending conferences and lectures
- Reading latest research
- Pursuing CME
- Acknowledging learning needs
- Striving for excellence

#### 3. Social Trust (Can I Trust You?)
Measures your ability to build trust, especially across different backgrounds.

**Key Areas**:
- Building cross-cultural trust
- Creating safe spaces for sensitive topics
- Reliability in follow-up
- Demonstrating genuine care
- Encouraging emotional sharing

#### 4. Treating Style (Are You Treating Me Differently?)
Evaluates your awareness of and response to health disparities and biases.

**Key Areas**:
- Awareness of health disparities
- Examining personal biases
- Ensuring equitable treatment
- Understanding social determinants
- Self-reflection on judgment

## 📈 Sample Recommendations

Based on your scores, you'll receive specific action items such as:

**For Personal Connect**:
- Make it a habit to sit down during patient consultations
- Call patients by name and ask about their personal interests
- Set reminders to follow up with patients after procedures

**For Trust of Your Trade**:
- Subscribe to key journals in your specialty
- Register for at least 2-3 conferences per year
- Join a journal club or peer learning group

**For Social Trust**:
- Create protocols for discussing sensitive topics
- Use open-ended questions to encourage patient sharing
- Demonstrate reliability by following up on every concern

**For Treating Style**:
- Take implicit bias training
- Study health disparities in your patient population
- Regularly self-reflect on treatment decisions

## 🛠️ Technical Details

### Built With

- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation
- **Python 3.8+** - Programming language

### File Structure

```
physician-assessment-tool/
│
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore            # Git ignore rules
```

## 📝 Based on Research

This tool is based on the article:

**"5 Questions Patients Have but Never Ask"**
- Published in: JAMA Neurology
- Date: July 9, 2018
- Key Insight: Patients have fundamental questions about their physicians that impact care quality but rarely ask directly

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Created as a tool to help physicians improve patient-centered care.

## 🙏 Acknowledgments

- Based on research published in JAMA Neurology
- Inspired by the goal of improving physician-patient relationships
- Built to support healthcare professionals in self-improvement

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Note**: This tool is for self-assessment and professional development purposes. It is not a substitute for formal performance evaluation or peer review.
EOF
