# Architecture & Development Guide

## 🏗 System Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with Streamlit
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Custom with passlib (PBKDF2)
- **ML Classification**: Rule-based ensemble approach
- **PDF Generation**: fpdf2
- **Storage**: Supabase Storage Buckets

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      User Browser                               │
│                   (Streamlit Frontend)                          │
└─────────────┬───────────────────────────────┬───────────────────┘
              │                               │
              ▼                               ▼
        ┌──────────────┐            ┌──────────────────┐
        │  Home Page   │            │  Admin Pages     │
        │ (Register/   │            │  (Portal/Login)  │
        │  Login)      │            └──────────────────┘
        └──────┬───────┘
               │
               ▼
    ┌──────────────────────────┐
    │  Streamlit Session State │
    │  - user_email            │
    │  - is_admin              │
    └──────────────┬───────────┘
                   │
     ┌─────────────┴──────────────┐
     │                            │
     ▼                            ▼
┌────────────────────┐    ┌──────────────────┐
│  Auth (lib/auth)   │    │  ML (lib/ml)     │
│  - register()      │    │  - classify()    │
│  - verify()        │    └──────────────────┘
└────────┬───────────┘
         │
         ▼
┌──────────────────────────┐
│  Database (lib/db)       │
│  - save_analysis()       │
│  - list_*_analyses()     │
│  - get_analysis_by_id()  │
└────────────┬─────────────┘
             │
             ▼
    ┌─────────────────────┐
    │  Supabase           │
    │  ┌───────────────┐  │
    │  │ PostgreSQL    │  │
    │  │ (analyses     │  │
    │  │  table)       │  │
    │  └───────────────┘  │
    │  ┌───────────────┐  │
    │  │ Storage       │  │
    │  │ (users.json)  │  │
    │  └───────────────┘  │
    └─────────────────────┘
```

---

## 📁 Module Documentation

### `lib/auth.py` - Authentication Module
**Purpose**: User registration and credential verification

**Functions**:
- `register(email, password)` - Create new user account
- `verify(email, password)` - Check credentials during login
- `get_user(email)` - Retrieve user by email
- `_ensure_users_json()` - Initialize users.json in storage
- `_load()` - Load users from Supabase
- `_save(data)` - Save users to Supabase

**Security**:
- Passwords hashed with PBKDF2-SHA256
- Hash stored, plaintext never saved
- Case-insensitive email handling

---

### `lib/db.py` - Database Module
**Purpose**: All database operations with Supabase

**Functions**:
- `get_client()` - Initialize Supabase client
- `save_analysis(row)` - Insert new analysis record
- `list_user_analyses(email, limit)` - Get analyses for specific user
- `list_all_analyses(limit)` - Get all analyses (admin)
- `get_analysis_by_id(id)` - Fetch single analysis

**Database Schema**:
```sql
analyses {
  id: UUID (primary key)
  user_email: TEXT
  phone: TEXT
  age: INTEGER
  gender: TEXT
  occupation: TEXT
  stress: INTEGER (0-10)
  blood_pressure: FLOAT (mmHg)
  heart_rate: INTEGER (bpm)
  sleep_duration: FLOAT (hours)
  bmi_category: TEXT (Normal/Overweight/Obese)
  snoring_frequency: INTEGER (per week)
  working_hours: INTEGER (per day)
  diagnosis: TEXT (ML result)
  severity: INTEGER (0-3)
  created_at: TIMESTAMP (auto)
}
```

---

### `lib/ml.py` - Machine Learning Module
**Purpose**: Sleep disorder classification using ensemble rules

**Function**:
- `classify(inputs: Dict) → Tuple[str, int]`
  - Returns: (diagnosis, severity_level)
  - Severity: 0=Normal, 1=Review, 2=Moderate, 3=High

**Classification Rules**:

| Condition | Score | Diagnosis |
|-----------|-------|-----------|
| OSA Score ≥ 5 | 3 | High Risk: OSA |
| Insomnia Score ≥ 4 | 3 | High Risk: Insomnia |
| Deprivation Score ≥ 3 | 2 | Moderate: Deprivation |
| Ideal Metrics | 0 | Normal |
| Deprivation Score 2 | 2 | Moderate: Deprivation |
| Other | 1 | Needs Review |

---

### `lib/pdf.py` - PDF Generation Module
**Purpose**: Generate downloadable medical reports

**Function**:
- `build_report(data: Dict) → bytes`
  - Creates formatted PDF with:
    - Patient information
    - Vital signs
    - Diagnosis
    - Medical disclaimer
    - Timestamp

---

### `streamlit_app.py` - Main Application Entry Point
**Purpose**: Landing page with registration and login

**Features**:
- Welcome/hero section
- Registration form
- Login form
- Admin access button
- Feature highlights
- Links to other pages

**Page Navigation**:
```
streamlit_app.py (HOME)
├─ pages/Sleep Analysis Dashboard.py (USER DASHBOARD)
├─ pages/Admin Login.py (ADMIN AUTH)
├─ pages/Admin Portal.py (ADMIN PANEL)
└─ pages/Report View.py (REPORT DETAILS)
```

---

### `pages/Sleep Analysis Dashboard.py` - User Dashboard
**Purpose**: Sleep analysis input and history

**Features**:
- 12-field health assessment form
- Real-time ML prediction
- Analysis history table
- Report viewing links
- Responsive UI

**Form Inputs**:
- Phone, Age, Gender, Occupation
- Stress level (1-10 slider)
- Vitals: BP, HR
- Sleep Duration (hours)
- BMI Category
- Snoring Frequency
- Working Hours

---

### `pages/Admin Login.py` - Admin Authentication
**Purpose**: Admin access control

**Features**:
- Password field
- Environment-based password
- Session state management
- Error handling

---

### `pages/Admin Portal.py` - Hospital Action Panel
**Purpose**: Centralized patient management

**Features**:
- Display all patient analyses
- Urgency highlighting (🔴🟡🟢)
- Quick actions: VIEW, CALL
- Sortable/filterable table

---

### `pages/Report View.py` - Detailed Report Display
**Purpose**: View and download medical reports

**Features**:
- Patient demographics
- Vital signs display
- Diagnosis with severity
- Medical disclaimer
- PDF download button

---

## 🔄 Data Processing Pipeline

### User Registration Flow
```python
Input: email, password
  ↓
Validation: email format, password strength
  ↓
Check: email not in users.json
  ↓
Hash: password with PBKDF2
  ↓
Store: {email: hashed_password} in users.json
  ↓
Output: True (success) or False (exists)
```

### Analysis Submission Flow
```python
Input: 12 health parameters
  ↓
Validation: all fields filled, correct types
  ↓
ML Classification: lib/ml.classify()
  ↓
Outputs: diagnosis (str), severity (int 0-3)
  ↓
Database Save: lib/db.save_analysis()
  ↓
User Sees: result + history update + PDF option
```

---

## 🧪 Testing Checklist

### Registration Tests
- [ ] Register with valid email and password
- [ ] Reject duplicate email
- [ ] Validate password strength
- [ ] Confirm user stored in Supabase

### Login Tests
- [ ] Login with correct credentials
- [ ] Reject wrong password
- [ ] Reject non-existent user
- [ ] Verify session state set

### Analysis Tests
- [ ] Submit complete form
- [ ] Classify correctly (test all severities)
- [ ] Save to database
- [ ] Verify history table updates

### Report Tests
- [ ] View report details
- [ ] Download PDF successfully
- [ ] PDF contains all info
- [ ] Timestamp correct

### Admin Tests
- [ ] Admin login with correct password
- [ ] Reject wrong password
- [ ] View all reports
- [ ] Quick actions work

---

## 🚀 Development Tips

### Add New Health Parameter
1. Add field to form in `Sleep Analysis Dashboard.py`
2. Add parameter to analysis record
3. Update ML rules in `ml.py`
4. Update PDF template in `pdf.py`
5. Update Supabase schema

### Change Severity Thresholds
Edit `lib/ml.py` - change score thresholds:
```python
if osa_score >= 5:  # Change this threshold
    return "High Risk: Obstructive Sleep Apnea", 3
```

### Add Admin Features
1. Create new page in `pages/` folder
2. Check `is_admin` session state
3. Call `db.list_all_analyses()` for data
4. Add link in `Admin Portal.py`

---

## 🔐 Security Considerations

1. **Passwords**: Never log or display
2. **Tokens**: Use environment variables
3. **SQL**: Use parameterized queries (Supabase handles)
4. **Session**: Streamlit manages, user controls logout
5. **HTTPS**: Enable in production
6. **Rate Limiting**: Consider for production

---

## 📊 Performance Optimization

- User queries limited to 50 results (paginate if needed)
- Admin queries limited to 200 results
- Cache user analyses in session state
- Lazy load PDF generation
- Consider indexing on `user_email` in Supabase

---

## 🐛 Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Import Error | Missing lib modules | Check `lib/` directory exists |
| Supabase Error | Wrong credentials | Verify `.env` file |
| PDF Generation | Missing fpdf2 | `pip install fpdf2` |
| Session Lost | Browser cache | Clear cache, restart server |
| Email Not Verified | Case sensitive | Convert to lowercase |

---

**Last Updated**: February 13, 2026
