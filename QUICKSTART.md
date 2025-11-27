# Quick Start Guide

Get the Job Market Trends Analytics project running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- pip (Python package manager)

## Step-by-Step Setup

### 1. Navigate to Project Directory
```bash
cd "job trend"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Setup Script (Optional)
```bash
python setup.py
```

This creates necessary directories and checks dependencies.

### 6. Start the Application
```bash
python app.py
```

### 7. Open in Browser
Navigate to: **http://localhost:5000**

## Default Credentials

**Admin Login:**
- Username: `admin`
- Password: `admin123`

Access admin panel at: **http://localhost:5000/admin/login**

## Test the ML Models

Run the demo script:
```bash
python ml/model.py
```

This will:
- Create sample predictions
- Show skill gap analysis
- Display job recommendations

## Try These Features

1. **Dashboard**: View analytics and charts
2. **Predictions**: Upload `data/job_postings_sample.csv` and run predictions
3. **Skill Gap**: Select "Data Scientist" and add skills like "Python", "SQL"
4. **Recommendations**: Enter skills to get job recommendations
5. **Trends**: Search for "Data Scientist" to see trends

## Common Issues

### Port Already in Use
If port 5000 is busy, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001
```

### Missing Dependencies
If you get import errors:
```bash
pip install -r requirements.txt
```

### Permission Errors (Linux/macOS)
If you can't create directories:
```bash
chmod +x setup.py
python setup.py
```

## Next Steps

- Read `README.md` for full documentation
- Check `HOW_IT_WORKS.md` to understand the prediction flow
- Review `PROJECT_STRUCTURE.md` for file organization
- Customize templates in `templates/`
- Add real ML models in `ml/model.py`

## Development Tips

1. **Enable Debug Mode**: Already enabled in `app.py` (auto-reloads on changes)
2. **View Logs**: Check terminal output for errors
3. **Test API**: Use browser DevTools Network tab or Postman
4. **Modify Data**: Edit JSON files in `data/` directory

## Production Deployment

See `README.md` for deployment instructions to:
- Render
- Heroku
- Gunicorn + systemd

---

**Need Help?** Check the main `README.md` for detailed documentation.

