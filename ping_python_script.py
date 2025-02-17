import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# Dictionary mapping IP addresses to their descriptions
ip_addresses = {
    "208.223.214.34": "Printfly Primary",
    "50.206.246.28": "Printfly Backup",
    "187.249.0.114": "Mach6 Primary",
    "201.163.134.170": "Mach6 Backup",
    "63.127.184.46": "Caroline Rd"
}

results = ""

# Ping each IP and store the results with descriptions
for ip, description in ip_addresses.items():
    try:
        result = subprocess.run(["ping", "-n", "4", ip], capture_output=True, text=True)
        results += f"{description} ({ip}):\n{result.stdout}\n"
    except Exception as e:
        results += f"Failed to ping {description} ({ip}): {e}\n"

# Email setup
sender_email = "it@rushordertees.com"
recipient_email = "it@rushordertees.com"
smtp_server = "smtp-relay.gmail.com"
smtp_port = 465  # SSL port

# Email content
subject = "Ping Results"
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = subject
message.attach(MIMEText(results, "plain"))

# Send the email
context = ssl._create_unverified_context()  # Disable certificate verification

try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.sendmail(sender_email, recipient_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
