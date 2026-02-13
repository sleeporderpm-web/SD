# 📊 Data Storage Quick Reference

## Where Everything Lives 📁

| What | Where | How to Access |
|------|-------|---------------|
| **User Registrations** | `.data/users.json` | Data Tracker → 👥 Registrations |
| **Sleep Analyses** | `.data/analyses.json` | Data Tracker → 📋 Analyses |
| **Medical Reports** | `.data/analyses.json` | Data Tracker → 📄 Reports |
| **Admin Password** | Environment variable | `.env` file or `ADMIN_PASSWORD` env var |

---

## Real Example From Your System 🔍

### Current Registered Users
```json
{
  "test@gmail.com": "$pbkdf2-sha256$..." ← Password hashed (secure)
}
```

### Current Sleep Analysis (= Report)
```json
{
  "id": "58eae5d8-4380-46c5-9d89-c1458035895d",  ← Report ID
  "user_email": "test@gmail.com",
  "phone": "1234567890",
  "age": 30,
  "sleep_duration": 7.0,
  "diagnosis": "Normal",
  "severity": 0,
  "created_at": "2026-02-13T09:15:43.254926"
}
```

---

## Track Your Data in 3 Commands 🚀

### 1️⃣ View All Users
```
http://localhost:8501/Data%20Tracker → 👥 Registrations tab
```

### 2️⃣ View All Analyses
```
http://localhost:8501/Data%20Tracker → 📋 Analyses tab
```

### 3️⃣ View Raw JSON Files
```bash
# In terminal
cat /workspaces/SD/.data/users.json
cat /workspaces/SD/.data/analyses.json
```

---

## Data Flow Summary 🔄

```
REGISTER
Email + Password → PBKDF2 Hash → .data/users.json ✅

LOGIN  
Email + Password → Match Hash in .data/users.json → Session ✅

SUBMIT ANALYSIS
Form Fields → ML Classification → .data/analyses.json ✅

VIEW REPORT
Click "View Report" → Get from .data/analyses.json → PDF Download ✅

ADMIN VIEW
Login as Admin → See all in .data/analyses.json → Color coded by severity ✅

TRACK EVERYTHING
Data Tracker page → See both files visually organized ✅
```

---

## Stats From Your System 📈

- **Total Users**: 1 (test@gmail.com)
- **Total Analyses**: 1
- **Diagnoses**: Normal (Severity 0 = 🟢 No Risk)
- **File Size**: Both files ~1KB each

---

## Real File Locations 📍

```
/workspaces/SD/
├── .data/
│   ├── users.json          ← All registered users with hashed passwords
│   └── analyses.json       ← All analyses & auto-generated reports
```

---

## Pages for Tracking 📱

| Page | Purpose | Access |
|------|---------|--------|
| **Data Tracker** | View ALL data visually | Sidebar → 📊 Data Tracker |
| **Sleep Dashboard** | View YOUR analyses | Login → Dashboard → History tab |
| **Report View** | See/download specific report | Dashboard → Click report |
| **Admin Portal** | View all with color-coded severity | Sidebar → Admin → Portal |

---

## Test It Out! 🧪

### See Current Data
1. Go to http://localhost:8501/Data%20Tracker
2. Click **👥 Registrations** → See test@gmail.com registered
3. Click **📋 Analyses** → See the sleep analysis submitted
4. Click **📄 Reports** → See report ready to download

### Or Check Directly
```bash
cd /workspaces/SD
cat .data/users.json          # See all user emails (hashed passwords)
cat .data/analyses.json       # See all sleep data & diagnoses
```

---

## Admin Credentials 🔐

**Default Password**: `admin123`

**To Change**:
1. Set environment variable:
   ```bash
   export ADMIN_PASSWORD="my-secure-password"
   ```
2. Restart Streamlit
3. Use new password to login

---

## Production Setup 🚀

When deploying to production, switch from local files to Supabase:

1. **Get Supabase credentials**: 
   - Go to https://supabase.com
   - Create project
   - Copy URL & Key

2. **Create `.env` file**:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-api-key
   ADMIN_PASSWORD=your-secure-password
   ```

3. **Restart app** → Automatically uses Supabase!

---

## Key Security Features 🔒

✅ **Passwords**: PBKDF2-SHA256 hashed (29,000 iterations)
✅ **Reports**: Unique UUID (cannot be guessed)
✅ **Local Files**: Git-ignored (`.gitignore` excludes `.data/`)
✅ **No Plaintext**: Never stores raw passwords
✅ **Admin Protected**: Password-protected admin panel

---

## Common Questions ❓

**Q: Where are my analyses?**
A: `.data/analyses.json` - View in Data Tracker page

**Q: How are passwords stored?**
A: PBKDF2-SHA256 hashed (one-way encryption, cannot be reversed)

**Q: Can I download reports?**
A: Yes! View Report → PDF Download button

**Q: How many analyses stored?**
A: Check Data Tracker → 📋 Analyses → see count at top

**Q: Can I export all data?**
A: Yes! Data Tracker → 🗄️ Raw Data → "Export All Data as JSON"

**Q: Using Supabase soon?**
A: Add `.env` with credentials and restart - automatic switch!

---

## Files Changed/Added 📝

- ✅ `lib/auth.py` - Now uses local `.data/users.json`
- ✅ `lib/db.py` - Now uses local `.data/analyses.json` with Supabase fallback
- ✅ `pages/Data Tracker.py` - NEW! Full data management dashboard
- ✅ `DATA_STORAGE_GUIDE.md` - Comprehensive documentation
- ✅ `DATA_STORAGE_QUICK_REFERENCE.md` - This file!
- ✅ `.data/` folder - Auto-created with JSON files

---

## Next Steps 🎯

1. **Test the system**
   - Register multiple users
   - Submit multiple analyses
   - Check Data Tracker page
   - Download a PDF report

2. **Monitor data**
   - Open Data Tracker daily
   - Export data for backup
   - Check for new analyses

3. **For production**
   - Set up Supabase account
   - Add `.env` credentials
   - Deploy to cloud

---

**Last Updated**: February 13, 2026
**Version**: 1.0
**Status**: ✅ Working
