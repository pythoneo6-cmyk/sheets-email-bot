import re

# ── Read and parse email_template.txt ───────────────────────────────
def parse_template(filepath, name):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # ── Extract subject ──────────────────────────────────────────────
    subject = ""
    body_raw = ""

    for line in content.splitlines():
        if line.startswith("SUBJECT:"):
            subject = line.replace("SUBJECT:", "").strip()
        
    # ── Extract body (everything after BODY:) ────────────────────────
    if "BODY:" in content:
        body_raw = content.split("BODY:", 1)[1].strip()

    # ── Replace {name} placeholder ───────────────────────────────────
    body_raw = body_raw.replace("{name}", name)
    subject  = subject.replace("{name}", name)

    # ── Convert formatting tags to HTML ─────────────────────────────
    # Convert each line to HTML paragraph
    html_lines = []
    for line in body_raw.splitlines():
        if line.strip() == "":
            html_lines.append("<br>")
            continue

        # **text** → bold
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)

        # *text* → italic
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)

        # ~~text~~ → coloured highlight
        line = re.sub(r'~~(.+?)~~', r'<span style="color:#E8593C">\1</span>', line)

        html_lines.append(f"<p style='margin:6px 0'>{line}</p>")

    html_body = "\n".join(html_lines)

    # ── Wrap in professional HTML email layout ───────────────────────
    html_email = f"""
    <html>
      <body style="font-family: Arial, sans-serif; 
                   background-color: #f4f4f4; padding: 30px;">
        <div style="max-width: 600px; margin: auto; 
                    background: #ffffff; border-radius: 8px; 
                    padding: 40px; border: 1px solid #eee;">
          
          <div style="border-bottom: 2px solid #4A90D9; 
                      padding-bottom: 10px; margin-bottom: 20px;">
            <h2 style="color: #4A90D9; margin: 0;">
                Message for {name}
            </h2>
          </div>

          <div style="color: #333333; font-size: 15px; line-height: 1.7;">
            {html_body}
          </div>

          <div style="margin-top: 30px; padding-top: 15px; 
                      border-top: 1px solid #eee; 
                      color: #999; font-size: 12px;">
            This email was sent automatically. Please do not reply.
          </div>

        </div>
      </body>
    </html>
    """

    # ── Plain text version (fallback) ────────────────────────────────
    plain_text = re.sub(r'\*\*(.+?)\*\*', r'\1', body_raw)
    plain_text = re.sub(r'\*(.+?)\*',     r'\1', plain_text)
    plain_text = re.sub(r'~~(.+?)~~',     r'\1', plain_text)

    return subject, plain_text, html_email


# ── Parse template from text directly (used by Streamlit app) ────────
def parse_template_from_text(subject, body_raw, name):
    
    # Replace {name} placeholder
    body_raw = body_raw.replace("{name}", name)
    subject  = subject.replace("{name}", name)

    # Convert formatting tags to HTML
    html_lines = []
    for line in body_raw.splitlines():
        if line.strip() == "":
            html_lines.append("<br>")
            continue

        # **text** → bold
        line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)

        # *text* → italic
        line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)

        # ~~text~~ → coloured highlight
        line = re.sub(r'~~(.+?)~~', 
                      r'<span style="color:#E8593C">\1</span>', line)

        html_lines.append(f"<p style='margin:6px 0'>{line}</p>")

    html_body = "\n".join(html_lines)

    # Wrap in professional HTML email layout
    html_email = f"""
    <html>
      <body style="font-family: Arial, sans-serif;
                   background-color: #f4f4f4; padding: 30px;">
        <div style="max-width: 600px; margin: auto;
                    background: #ffffff; border-radius: 8px;
                    padding: 40px; border: 1px solid #eee;">

          <div style="border-bottom: 2px solid #4A90D9;
                      padding-bottom: 10px; margin-bottom: 20px;">
            <h2 style="color: #4A90D9; margin: 0;">
                Message for {name}
            </h2>
          </div>

          <div style="color: #333333; font-size: 15px; line-height: 1.7;">
            {html_body}
          </div>

          <div style="margin-top: 30px; padding-top: 15px;
                      border-top: 1px solid #eee;
                      color: #999; font-size: 12px;">
            This email was sent automatically. Please do not reply.
          </div>

        </div>
      </body>
    </html>
    """

    # Plain text fallback
    plain_text = re.sub(r'\*\*(.+?)\*\*', r'\1', body_raw)
    plain_text = re.sub(r'\*(.+?)\*',     r'\1', plain_text)
    plain_text = re.sub(r'~~(.+?)~~',     r'\1', plain_text)

    return subject, plain_text, html_email