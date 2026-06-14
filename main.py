import csv
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from template_parser import parse_template

# ── Read contacts from CSV ───────────────────────────────────────────
def read_contacts(filepath):
    contacts = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            contacts.append({
                "name"  : row["name"],
                "email" : row["email"],
                "status": row["status"]
            })
    return contacts

# ── Mark contact as Sent in CSV ─────────────────────────────────────
def mark_as_sent(filepath, sent_email):
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["email"] == sent_email:
                row["status"] = "Sent"
            rows.append(row)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# ── Build personalised HTML email ────────────────────────────────────
def build_email(to_name, to_email):
    subject, plain_text, html_email = parse_template(
        config.TEMPLATE_FILE, to_name
    )
    msg = MIMEMultipart("alternative")
    msg["From"]    = config.SENDER_EMAIL
    msg["To"]      = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_email, "html"))
    return msg

# ── Send one email ───────────────────────────────────────────────────
def send_email(smtp, to_name, to_email):
    msg = build_email(to_name, to_email)
    smtp.sendmail(config.SENDER_EMAIL, to_email, msg.as_string())

# ── Main workflow ────────────────────────────────────────────────────
def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("--- DRY RUN MODE --- (no emails will be sent)")

    contacts = read_contacts(config.CSV_FILE)
    print(f"Found {len(contacts)} contacts")

    sent_count    = 0
    skipped_count = 0
    failed_count  = 0

    if not dry_run:
        smtp_connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_connection.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        print("Logged in to Gmail successfully")

    for contact in contacts:
        name   = contact["name"]
        email  = contact["email"]
        status = contact["status"]

        # Skip already sent contacts
        if status == "Sent":
            print(f"Skipping {name} — already sent")
            skipped_count += 1
            continue

        try:
            if dry_run:
                subject, plain_text, _ = parse_template(
                    config.TEMPLATE_FILE, name
                )
                print(f"\n--- Email preview for {name} ---")
                print(f"To      : {email}")
                print(f"Subject : {subject}")
                print(f"Body    :\n{plain_text}")
                sent_count += 1
            else:
                send_email(smtp_connection, name, email)
                mark_as_sent(config.CSV_FILE, email)
                print(f"Sent to {name} ({email})")
                sent_count += 1

        except Exception as e:
            print(f"Failed for {name} --- {e}")
            failed_count += 1

    if not dry_run:
        smtp_connection.quit()

    print(f"\n--- Summary ---")
    print(f"Sent    : {sent_count}")
    print(f"Skipped : {skipped_count}")
    print(f"Failed  : {failed_count}")
    print(f"Total   : {len(contacts)}")

if __name__ == "__main__":
    main()
    