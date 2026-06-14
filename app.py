import streamlit as st
import csv
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from template_parser import parse_template_from_text

# ── Page configuration ───────────────────────────────────────────────
st.set_page_config(
    page_title = "Gmail Automation Bot",
    page_icon  = "✉️",
    layout     = "centered"
)

# ── App title ────────────────────────────────────────────────────────
st.title("✉️ Gmail Automation Bot")
st.markdown("Upload your contacts, write your email, preview and send.")
st.divider()

# ── Step 0: Gmail credentials ────────────────────────────────────────
st.subheader("Step 0 — Enter your Gmail credentials")
st.markdown("Your credentials are never saved — entered fresh each session.")

sender_email    = st.text_input("Your Gmail address", 
                                placeholder="yourname@gmail.com")
sender_password = st.text_input("Your Gmail App Password", 
                                type="password",
                                placeholder="xxxx xxxx xxxx xxxx")

if not sender_email or not sender_password:
    st.warning("Please enter your Gmail credentials to continue")
    st.stop()

st.success("Credentials entered — ready to continue")
st.divider()

# ── Step 1: Upload CSV ───────────────────────────────────────────────
st.subheader("Step 1 — Upload your contacts CSV")
st.markdown("Your CSV must have these columns: `name`, `email`")

uploaded_file = st.file_uploader("Choose your contacts CSV", type="csv")

contacts = []

if uploaded_file:
    # Read uploaded CSV into memory
    content = uploaded_file.read().decode("utf-8")
    reader  = csv.DictReader(io.StringIO(content))
    
    for row in reader:
        contacts.append({
            "name" : row["name"].strip(),
            "email": row["email"].strip()
        })

    # Show contacts in a table
    st.success(f"Found {len(contacts)} contacts")
    st.dataframe({
        "Name" : [c["name"]  for c in contacts],
        "Email": [c["email"] for c in contacts]
    })

st.divider()


# ── Step 2: Write email template ─────────────────────────────────────
st.subheader("Step 2 — Write your email")

st.markdown("""
**Formatting guide:**
| What you type | What client sees |
|---------------|-----------------|
| `**text**`    | **Bold**        |
| `*text*`      | *Italic*        |
| `~~text~~`    | Highlighted     |
| `{name}`      | Contact's name  |
""")

# Subject input
subject_input = st.text_input(
    "Email Subject",
    placeholder="e.g. Welcome from our team"
)

# Body input
body_input = st.text_area(
    "Email Body",
    height=250,
    placeholder="""Hi {name},

**Thank you** for joining us.
*We are happy* to have you on board.

~~This offer is valid for limited time only~~

Regards,
Your Company Name"""
)

st.divider()


# ── Step 3: Preview emails ───────────────────────────────────────────
st.subheader("Step 3 — Preview before sending")

if st.button("👁️ Preview Emails", use_container_width=True):
    
    # Check if everything is filled in
    if not contacts:
        st.error("Please upload your contacts CSV first")
    elif not subject_input.strip():
        st.error("Please write an email subject")
    elif not body_input.strip():
        st.error("Please write an email body")
    else:
        st.success(f"Previewing {len(contacts)} emails")
        
        for contact in contacts:
            name  = contact["name"]
            email = contact["email"]

            # Parse formatting tags to HTML
            subject, plain_text, html_preview = parse_template_from_text(
                subject_input, body_input, name
            )

            # Show each email preview in an expander
            with st.expander(f"📧 {name} — {email}"):
                st.markdown(f"**Subject:** {subject}")
                st.markdown("**Body preview:**")
                st.markdown(plain_text)

st.divider()


# ── Step 4: Send emails ──────────────────────────────────────────────
st.subheader("Step 4 — Send emails")

if st.button("🚀 Send Emails", use_container_width=True, type="primary"):

    # Check if everything is filled in
    if not contacts:
        st.error("Please upload your contacts CSV first")
    elif not subject_input.strip():
        st.error("Please write an email subject")
    elif not body_input.strip():
        st.error("Please write an email body")
    else:
        # Connect to Gmail
        try:
            smtp_connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            smtp_connection.login(sender_email, sender_password)
            st.success("Logged in to Gmail successfully")
        except Exception as e:
            st.error(f"Gmail login failed --- {e}")
            st.stop()

        # Send to each contact
        sent_count   = 0
        failed_count = 0

        progress_bar = st.progress(0)
        status_box   = st.empty()

        for i, contact in enumerate(contacts):
            name  = contact["name"]
            email = contact["email"]

            try:
                # Build email from template
                subject, plain_text, html_email = parse_template_from_text(
                    subject_input, body_input, name
                )

                # Build MIME message
                msg = MIMEMultipart("alternative")
                msg["From"]    = sender_email
                msg["To"]      = email
                msg["Subject"] = subject
                msg.attach(MIMEText(plain_text, "plain"))
                msg.attach(MIMEText(html_email, "html"))

                # Send
                smtp_connection.sendmail(sender_email, email, msg.as_string())

                sent_count += 1
                status_box.success(f"Sent to {name} ({email})")

            except Exception as e:
                failed_count += 1
                status_box.error(f"Failed for {name} --- {e}")

            # Update progress bar
            progress_bar.progress((i + 1) / len(contacts))

        smtp_connection.quit()

        # Final summary
        st.divider()
        st.subheader("📊 Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Sent",   sent_count)
        col2.metric("Failed", failed_count)
        col3.metric("Total",  len(contacts))