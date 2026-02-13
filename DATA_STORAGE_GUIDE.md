# 📊 Sleep Disorder Data Storage & Tracking Guide

## Quick Overview

All your data is stored locally in the `.data/` folder during development. Here's where everything goes:

| Data Type | Storage Location | Format | Purpose |
|-----------|------------------|--------|---------|
| **User Registrations** | `.data/users.json` | JSON | Email + hashed password |
| **Sleep Analyses** | `.data/analyses.json` | JSON | Analysis results & predictions |
| **Reports** | `.data/analyses.json` | JSON (exportable to PDF) | Generated medical reports |
| **Admin Credentials** | Environment variable or code | String | Admin login password |

---

## 📝 User Registrations Storage

### Location
```
.data/users.json
```

### File Structure
```json
{
  "users": {
    "email@example.com": "$pbkdf2-sha256$29000$[salt]$[hash]",
    "another@email.com": "$pbkdf2-sha256$29000$[salt]$[hash]"
  }
}
```

### Security Details
- **Algorithm**: PBKDF2-SHA256 (industry standard)
- **Iterations**: 29,000 rounds
- **Format**: Passwords are one-way hashed (cannot be decrypted)
- **Storage**: Never stores plaintext passwords

### How to Track Registrations
1. Open **Data Tracker** page from sidebar
2. Click on **"👥 Registrations"** tab
3. View all registered emails and status

---

## 🏥 Sleep Analysis Data Storage

### Location
```
.data/analyses.json
```

### File Structure
```json
{
  "analyses": [
    {
      "id": "58eae5d8-4380-46c5-9d89-c1458035895d",
      "user_email": "test@gmail.com",
      "phone": "1234567890",
      "age": 30,
      "gender": "Male",
      "occupation": "Engineer",
      "stress": 5,
      "blood_pressure": 120.0,
      "heart_rate": 72,
      "sleep_duration": 7.0,
      "bmi_category": "Underweight",
      "snoring_frequency": 1,
      "working_hours": 8,
      "diagnosis": "Normal",
      "severity": 0,
      "created_at": "2026-02-13T09:15:43.254926"
    }
  ]
}
```

### Field Descriptions
| Field | Type | Example | Purpose |
|-------|------|---------|---------|
| `id` | UUID | 58eae5d8... | Unique report identifier |
| `user_email` | String | test@gmail.com | Patient email |
| `phone` | String | 1234567890 | Contact number |
| `age` | Integer | 30 | Patient age |
| `gender` | String | Male/Female/Other | Patient gender |
| `occupation` | String | Engineer | Job description |
| `stress` | Integer | 0-10 | Stress level (0=low, 10=high) |
| `blood_pressure` | Float | 120.0 | Systolic BP (mmHg) |
| `heart_rate` | Integer | 72 | BPM at rest |
| `sleep_duration` | Float | 7.0 | Hours of sleep |
| `bmi_category` | String | Underweight | BMI classification |
| `snoring_frequency` | Integer | 1 | Snores per week |
| `working_hours` | Integer | 8 | Hours worked daily |
| `diagnosis` | String | Normal | ML prediction result |
| `severity` | Integer | 0-3 | Risk level (0=none, 3=critical) |
| `created_at` | String | ISO datetime | Timestamp of analysis |

### Diagnosis & Severity Levels

**Severity Scale:**
- `0` = 🟢 Normal (No risks)
- `1` = 🟡 Low Risk (Needs review)
- `2` = 🟡 Moderate Risk (Monitor closely)
- `3` = 🔴 High Risk (Urgent action needed)

**Possible Diagnoses:**
- `Normal` - Healthy sleep pattern
- `High Risk: Obstructive Sleep Apnea (OSA)` - Breathing interruptions during sleep
- `High Risk: Chronic Insomnia` - Difficulty falling/staying asleep
- `Moderate Risk: Sleep Deprivation` - Insufficient sleep duration
- `Needs Review` - Borderline cases requiring assessment

### How to Track Analyses
1. Open **Data Tracker** page from sidebar
2. Click on **"📋 Analyses"** tab
3. Features available:
   - View total count
   - See all analyses with details
   - Search by patient email
   - Filter by diagnosis
   - Filter by severity level

---

## 📄 Medical Reports Storage & Tracking

### Where Reports Are Stored
**Since we don't have a separate reports table yet**, each analysis automatically becomes a report:
- Every analysis record in `.data/analyses.json` is a report
- **Report ID** = `id` field in the analysis object
- **Report Content** = All the analysis data

### How to Access Reports

#### Method 1: Data Tracker Page
1. Go to **Data Tracker** → **"📄 Reports"** tab
2. See all generated reports
3. View report details
4. Export JSON data

#### Method 2: Sleep Analysis Dashboard
1. Login to your account
2. Go to **Sleep Analysis Dashboard**
3. Click **"📋 History"** tab
4. Click **"View Report"** button for any analysis
5. See the full report with PDF download option

#### Method 3: Admin Portal
1. Login as admin
2. Go to **Admin Portal**
3. Find patient by urgency color:
   - 🔴 RED = Urgent (Severity 3)
   - 🟡 YELLOW = Moderate (Severity 2)
   - 🟢 GREEN = Normal (Severity 0-1)
4. Click "VIEW Report" with report ID
5. Full report opens with PDF download

### Report Download (PDF)
1. Open any report (via Dashboard or Admin Portal)
2. Includes:
   - Patient demographics
   - Vital signs
   - ML classification result
   - Severity indicator
   - Medical disclaimer
3. Click **"📥 Download PDF"** button to save

---

## 🔐 Admin Credentials Storage

### Location
**Three possible locations (checked in order):**

1. **Environment Variable** (Production recommended)
   ```bash
   export ADMIN_PASSWORD="your-secure-password"
   ```

2. **Streamlit Secrets** (For Streamlit Cloud)
   File: `.streamlit/secrets.toml`
   ```toml
   ADMIN_PASSWORD = "your-secure-password"
   ```

3. **Hardcoded Default** (Development only)
   ```python
   # In pages/Admin Login.py
   admin_pwd = "admin123"  # Default if no env var
   ```

### How to Change Admin Password
1. Set environment variable:
   ```bash
   export ADMIN_PASSWORD="new_secure_password"
   ```
2. Or create `.streamlit/secrets.toml`:
   ```toml
   ADMIN_PASSWORD = "new_secure_password"
   ```
3. Restart Streamlit app
4. Login with new password

---

## 📊 Data Tracker Dashboard Features

### Available Pages

#### 1. 👥 Registrations Tab
- List all registered users
- Count total registrations
- View email addresses
- See password hash verification (for debugging)

#### 2. 📋 Analyses Tab
- List all sleep analyses
- Metrics: Total, Normal, Risk cases
- Detailed data table with:
  - Date of analysis
  - Patient email
  - Contact phone
  - Health metrics (BP, HR, sleep)
  - Diagnosis result
  - Severity level
  - Report ID
- Advanced filtering:
  - Search by email
  - Filter by diagnosis
  - Filter by severity

#### 3. 📄 Reports Tab
- All auto-generated reports
- Report status (Ready for Download)
- Select report to view
- Preview JSON data
- Get report ID for linking

#### 4. 🗄️ Raw Data Tab
- View complete JSON data
- Users file (hashed passwords)
- Analyses file (all records)
- Useful for debugging or export

---

## 📂 File System Structure

```
/workspaces/SD/
├── .data/                          # ← All data stored here
│   ├── users.json                  # User registrations
│   └── analyses.json               # Sleep analyses & reports
├── pages/
│   ├── Data Tracker.py             # ← NEW: View all data
│   ├── Register.py
│   ├── Login.py
│   ├── Sleep Analysis Dashboard.py
│   ├── Admin Login.py
│   ├── Admin Portal.py
│   └── Report View.py
├── lib/
│   ├── auth.py                     # Handles user registration login
│   ├── db.py                       # Handles analysis storage
│   ├── ml.py                       # ML classification
│   └── pdf.py                      # PDF report generation
├── streamlit_app.py                # Main landing page
└── .gitignore                      # .data/ excluded from git
```

---

## 🔄 Data Flow Diagram

```
USER REGISTRATION
├─ User enters email + password
├─ Password hashed (PBKDF2)
└─ Stored in .data/users.json

USER LOGIN
├─ User enters credentials
├─ Password compared with hash
└─ Session created if match

SLEEP ANALYSIS SUBMISSION
├─ User fills form (12 fields)
├─ ML model classifies
├─ Report ID generated (UUID)
└─ Stored in .data/analyses.json

REPORT GENERATION
├─ User/Admin requests report
├─ Data retrieved from JSON
├─ PDF generated on-the-fly
└─ Available for download
```

---

## 🚀 Production Deployment

### Switch to Supabase (Production)

When deploying to production, use Supabase instead of local files:

1. **Create Supabase project**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Get `SUPABASE_URL` and `SUPABASE_KEY`

2. **Create `.env` file**
   ```
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-key
   ADMIN_PASSWORD=your-admin-password
   ```

3. **Create database tables**
   - `analyses` table (for studies)
   - `appdata` storage bucket (for users.json)

4. **Restart Streamlit**
   - It will automatically use Supabase
   - Fallback to local files if Supabase unavailable

---

## 📋 Data Backup & Export

### Backup Local Data
1. Go to **Data Tracker** → **"🗄️ Raw Data"** tab
2. Click **"📖 Show Analyses (JSON)"**
3. Copy to safe location
4. Or use **"📥 Export All Data as JSON"** for automatic download

### Share Data
- Export as JSON
- Share file securely
- Import later if needed

---

## ✅ Tracking Checklist

- ✅ **Register User**: Check `.data/users.json`
- ✅ **Submit Analysis**: Check `.data/analyses.json`
- ✅ **View All Data**: Use Data Tracker page
- ✅ **Download Reports**: Via Report View page
- ✅ **Admin Actions**: Use Admin Portal
- ✅ **Export Data**: Use Data Tracker export button

---

## 🆘 Troubleshooting

### "Registration error: Missing Supabase credentials"
- **Solution**: App uses local storage fallback automatically. No action needed. (Previously showing error, now fixed)

### Can't find user data
1. Check if user registered successfully (look in Data Tracker)
2. Verify `.data/users.json` exists
3. Try refreshing the page

### Analysis not saving
1. Check `.data/analyses.json` file
2. Verify file permissions
3. Check browser console for errors

### Can't access Data Tracker
- Go to Home page sidebar
- Click "📊 View Data Tracker" button
- No login required to view data

---

## 📞 Support

For questions about data storage:
1. Check this guide
2. View Data Tracker page for live data
3. Export JSON for external analysis
4. Check `.data/` folder directly

