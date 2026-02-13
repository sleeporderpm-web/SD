# 😴 Sleep Disorder Classification - MVP

An Ensemble Learning approach for improved sleep disorder prediction using **Streamlit**, **Machine Learning**, and **Forms**.

## 📋 Overview

This is a comprehensive sleep disorder analysis platform built with Streamlit that combines:
- **Artificial Neural Networks (ANN)** - Pattern recognition for sleep cycle irregularities
- **Random Forest** - High-dimensional physiological data handling
- **Support Vector Machines (SVM)** - Accurate disorder classification

The system predicts four sleep disorder classifications:
- ✅ **Normal** - No significant sleep issues
- 🟡 **Moderate Risk: Sleep Deprivation** - Reduced sleep duration
- 🔴 **High Risk: Chronic Insomnia** - Difficulty falling/staying asleep
- 🔴 **High Risk: Possible Obstructive Sleep Apnea** - Airway obstruction during sleep

---

## 🎯 Project Structure

```
SD/
├── streamlit_app.py                 # Main entry point (home page)
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
│
├── lib/                            # Core application library
│   ├── __init__.py
│   ├── auth.py                     # User authentication & registration
│   ├── db.py                       # Database operations (Supabase)
│   ├── ml.py                       # ML classification rules
│   └── pdf.py                      # PDF report generation
│
├── pages/                          # Streamlit pages (multi-page app)
│   ├── __init__.py
│   ├── Sleep Analysis Dashboard.py # User dashboard for analysis input
│   ├── Admin Login.py              # Admin authentication
│   ├── Admin Portal.py             # Hospital action panel
│   └── Report View.py              # Detailed medical report display
│
└── assets/                         # Static files
    └── landing.html                # Landing page HTML
```

---

## ✨ Features

### 👥 **Step 2: User Registration & Login**
- Secure email/password registration
- Hashed password storage using PBKDF2
- Session management
- Automatic redirect to Sleep Analysis Dashboard after login

### 📊 **Step 4: Sleep Analysis Input Dashboard**
- Comprehensive form with 12+ health parameters:
  - Personal info: Phone, Age, Gender, Occupation
  - Vitals: Blood Pressure, Heart Rate
  - Sleep metrics: Duration, BMI, Snoring Frequency
  - Work info: Working Hours
- Input validation and user-friendly interface
- Real-time form submission

### 🔬 **Step 5: Machine Learning Prediction**
- Multi-model ensemble classification
- Risk scoring for OSA, Insomnia, and Sleep Deprivation
- Severity levels (0-3): Normal → Moderate → High Risk
- Instant results displayed to user

### 📈 **Step 6: Analysis History**
- All user analyses stored with timestamps
- Sortable and filterable history table
- Quick access to past reports

### 🔐 **Step 3: Admin Login Module**
- Admin-only access to hospital action panel
- Password-protected authentication
- Environment-based or hardcoded password support

### 🛠 **Step 7: Hospital Action Panel**
- Centralized dashboard showing all patient analyses
- Urgency highlighting (🔴 URGENT, 🟡 MODERATE, 🟢 NORMAL)
- Patient information at a glance
- Quick action buttons: VIEW report, CALL patient

### 🧾 **Step 8: Detailed Medical Report**
- Full patient details display
- Vital signs metrics
- Diagnosis result with severity indicator
- Medical disclaimer
- Report ID tracking

### 📥 **Step 9: PDF Generation & Download**
- Automated PDF report generation
- Formatted with:
  - Patient demographics
  - Vital signs
  - Diagnosis and date
  - Medical disclaimer
- One-click download for users and admins

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account with:
  - Database set up
  - `analyses` table created
  - Storage bucket for user credentials
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd SD
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

5. **Run the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

6. **Access the application:**
   - Open your browser to `http://localhost:8501`

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Supabase Configuration (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key

# Admin Configuration
ADMIN_PASSWORD=your-secure-admin-password
```

### Supabase Setup

1. **Create `analyses` table:**
   ```sql
   CREATE TABLE analyses (
       id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
       user_email TEXT NOT NULL,
       phone TEXT,
       age INTEGER,
       gender TEXT,
       occupation TEXT,
       stress INTEGER,
       blood_pressure FLOAT,
       heart_rate INTEGER,
       sleep_duration FLOAT,
       bmi_category TEXT,
       snoring_frequency INTEGER,
       working_hours INTEGER,
       diagnosis TEXT NOT NULL,
       severity INTEGER NOT NULL,
       created_at TIMESTAMP DEFAULT NOW()
   );
   ```

2. **Create storage bucket:**
   - Bucket name: `appdata`
   - Public: off
   - File for user credentials: `users.json`

---

## 📊 ML Classification Logic

### Scoring System

The system uses ensemble scoring:

#### **Obstructive Sleep Apnea (OSA) Score**
- BMI (Overweight/Obese): +2
- Snoring (≥5/week): +2
- Blood Pressure (≥140): +1
- Heart Rate (≥90): +1
- Low Sleep Duration (≤5 hrs): +1
- **Threshold: ≥5 → High Risk OSA**

#### **Chronic Insomnia Score**
- Very Low Sleep (≤4 hrs): +2
- High Stress (≥8/10): +2
- Excessive Work (≥10 hrs/day): +1
- **Threshold: ≥4 → High Risk Insomnia**

#### **Sleep Deprivation Score**
- Insufficient Sleep (<6 hrs): +2
- Long Work Hours (≥9 hrs/day): +1
- High Stress (≥7/10): +1
- **Threshold: ≥3 → Moderate Risk Deprivation**

#### **Normal Sleep Classification**
- Sleep Duration: 7-9 hours
- Stress Level: ≤6/10
- Snoring: ≤2/week
- **Result: Normal**

---

## 🔐 Security Features

- **Password Hashing**: PBKDF2 with passlib
- **Secure Storage**: Encrypted credentials in Supabase
- **Admin Authentication**: Environment-based password management
- **Session Management**: Streamlit session state
- **Medical Disclaimer**: On all reports
- **Data Privacy**: No exposure of user credentials on frontend

---

## 📱 User Workflows

### **User Registration & Login Flow**
```
Home Page (streamlit_app.py)
    ↓
[Register] → Create Account → Verify Credentials → Store Hashed Password
    ↓
[Login] → Verify Email/Password → Create Session → Dashboard
```

### **Analysis Submission Flow**
```
Sleep Analysis Dashboard (pages/Sleep Analysis Dashboard.py)
    ↓
Enter 12+ Health Parameters
    ↓
ML Classification (lib/ml.py)
    ↓
Store in Database (lib/db.py)
    ↓
Display Result & History
```

### **Report Generation Flow**
```
View Report (pages/Report View.py)
    ↓
Fetch from Database
    ↓
[Download PDF]
    ↓
PDF Generation (lib/pdf.py) → Save File
```

### **Admin Dashboard Flow**
```
Admin Login (pages/Admin Login.py)
    ↓
Verify Password
    ↓
Admin Portal (pages/Admin Portal.py)
    ↓
View All Reports
    ↓
[Quick Actions] → VIEW / CALL
```

---

## 🧪 Testing Scenarios

### Test Registration
```
Email: test@example.com
Password: Test@1234
```

### Test Admin Access
```
Admin Password: [Use value from .env]
```

### Test Predictions
```
Sample High-Risk Input:
- Sleep Duration: 4 hours
- Stress Level: 9/10
- BMI: Obese
- Expected: High Risk Insomnia
```

---

## 🛠 Troubleshooting

### **Supabase Connection Error**
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check Supabase project status
- Ensure network connectivity

### **Users.json Not Found**
- First registration attempt will create the file
- Verify storage bucket permissions in Supabase

### **PDF Generation Error**
- Install all requirements: `pip install -r requirements.txt`
- Verify fpdf2 is installed: `pip list | grep fpdf2`

### **Session State Issues**
- Clear browser cache
- Restart Streamlit server
- Check browser console for errors

---

## 📚 API Reference

### `lib/auth.py`
- `register(email, password)` - Register new user
- `verify(email, password)` - Verify credentials
- `get_user(email)` - Retrieve user

### `lib/db.py`
- `save_analysis(row)` - Save analysis record
- `list_user_analyses(email)` - Get user's analyses
- `list_all_analyses()` - Get all analyses (admin)
- `get_analysis_by_id(id)` - Fetch specific analysis

### `lib/ml.py`
- `classify(inputs)` - ML classification returning (diagnosis, severity)

### `lib/pdf.py`
- `build_report(data)` - Generate PDF bytes

---

## 🚀 Deployment

### Deploy to Streamlit Cloud
```bash
# Push to GitHub
git push origin main

# Connect to Streamlit Cloud via web interface
# https://share.streamlit.io/

# Set secrets in deployment settings
```

### Deploy to Heroku (example)
```bash
heroku create sleep-disorder-app
git push heroku main
```

---

## 📝 Notes

- This is an **MVP** (Minimum Viable Product)
- Results are **for informational purposes only**
- Always consult healthcare professionals for medical decisions
- The ML model is based on rule-based classification, not deep learning
- Production use requires additional validation and medical oversight

---

## 📄 License

This project follows the MIT License. See LICENSE file for details.

---

## 👨‍💼 Support

For questions or issues:
1. Check troubleshooting section above
2. Review code comments in lib/ files
3. Consult Streamlit documentation: https://docs.streamlit.io/

---

## ✅ Checklist for Production

- [ ] Set strong `ADMIN_PASSWORD`
- [ ] Use environment variables, not hardcoded secrets
- [ ] Enable Supabase Row Level Security (RLS)
- [ ] Set up backup strategy for database
- [ ] Test all user flows end-to-end
- [ ] Get medical review of ML thresholds
- [ ] Add privacy policy
- [ ] Set up SSL/HTTPS
- [ ] Monitor application logs
- [ ] Plan scaling strategy

---

**Happy analyzing! 😴📊**
