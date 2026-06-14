# Gmail Automation Bot

A Python script and Streamlit web app that reads contacts from a CSV file and sends personalised styled emails via Gmail automatically. No coding knowledge required to operate.

## Demo
Watch 90 second demo — coming soon

## Actual Streamlit URL:
Live app: https://pythoneo6-cmyk-sheets-email-bot.streamlit.app

## What it does
- Reads names and emails from a CSV file
- Sends personalised HTML styled emails to each contact
- Supports bold, italic and colour formatting in emails
- Marks each contact as Sent to prevent duplicate emails
- Supports dry run mode for safe preview before sending
- Shows summary report after every run
- Full Streamlit web UI for non technical users

## Tech stack
- Python 3
- Streamlit — web interface
- smtplib — Gmail sending
- csv — contact management
- Gmail App Password — secure authentication

## Project structure
- app.py — Streamlit web UI for non technical users
- main.py — terminal version for technical users
- template_parser.py — converts formatting tags to HTML
- config.py — one time setup only
- contacts.csv — add your contacts here
- email_template.txt — write your email draft here

## How to use

### One time setup
1. Open config.py
2. Add your Gmail address
3. Add your Gmail App Password
4. Save — never touch config.py again

### Non technical users
python -m streamlit run app.py
Then open http://localhost:8501 in your browser

### Technical users
python main.py --dry-run
python main.py

## Email formatting guide
- **your text** becomes Bold
- *your text* becomes Italic
- ~~your text~~ becomes Highlighted
- {name} becomes the contact name automatically

## Author
Neo — Python developer
GitHub https://github.com/pythoneo6-cmyk
