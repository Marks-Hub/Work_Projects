import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
# This Script pings a list of IP addresses and sends an email if something doesn't ping properly.
# Dictionary mapping IP addresses to their descriptions
ip_addresses = {
    "REDACTED": "REDACTED",
    "REDACTED": "REDACTED",
    "REDACTED": "REDACTED",
    "REDACTED": "REDACTED",
    "REDACTED": "REDACTED",
    "10.1.113.111": "REDACTED",
    "10.1.113.215": "REDACTED",
    "10.2.96.16": "REDACTED",
    "10.2.96.17": "REDACTED",
    "10.1.113.211": "REDACTED",
    "10.2.96.99": "REDACTED",
    "10.1.113.20": "REDACTED",
    "10.1.113.21": "REDACTED",
    "10.1.113.110": "REDACTED",
    "10.1.113.1": "REDACTED",
    "10.1.103.240":"REDACTED",
    "10.1.103.241":"REDACTED",
    "10.1.103.242":"REDACTED",
    "10.1.103.243":"REDACTED",
    "10.1.103.244":"REDACTED",
    "10.1.103.245":"REDACTED",
    "10.1.113.50":"REDACTED",
    "10.1.113.51":"REDACTED",
    "10.1.113.52":"REDACTED",
    "10.1.113.53":"REDACTED",
    "10.1.113.54":"REDACTED",
    "10.1.113.55":"REDACTED",
    "10.2.96.81":"REDACTED",
    "10.2.96.82":"REDACTED",
    "10.2.96.83":"REDACTED",
    "10.2.96.84":"REDACTED",
    "10.2.96.85":"REDACTED",
    "10.2.96.86":"REDACTED",
    "10.2.96.87":"REDACTED",
    "10.2.96.88":"REDACTED",
    "10.2.96.89":"REDACTED",
    "10.2.96.90":"REDACTED",
    "10.2.96.91":"REDACTED",
    "10.2.96.92":"REDACTED"
}

failed_results = ""

# Ping each IP and check for failures
for ip, description in ip_addresses.items():
    try:
        result = subprocess.run(["ping", "-n", "4", ip], capture_output=True, text=True)
        if "Request timed out." in result.stdout or "Destination host unreachable" in result.stdout:
            failed_results += f"{description} ({ip}) failed:\n{result.stdout}\n"
    except Exception as e:
        failed_results += f"Failed to ping {description} ({ip}): {e}\n"

# Only send email if there are failures
if failed_results:
    # Email setup
    sender_email = "REDACTED"
    recipient_email = "REDACTED"
    smtp_server = "smtp-relay.gmail.com"
    smtp_port = 465  # SSL port

    # Email content
    subject = "Ping Failure Alert"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(failed_results, "plain"))

    # Send the email
    context = ssl._create_unverified_context()  # Disable certificate verification

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.sendmail(sender_email, recipient_email, message.as_string())
            print("Failure email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
else:
    print("All pings were successful. No email sent.")



