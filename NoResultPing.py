import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
# This Script pings a list of IP addresses and sends an email if something doesn't ping properly.
# Dictionary mapping IP addresses to their descriptions
ip_addresses = {
    "208.223.214.34": "Printfly Primary Internet",
    "50.206.246.28": "Printfly Backup Internet",
    "187.249.0.114": "Mach6 Primary Internet",
    "201.163.134.170": "Mach6 Backup Internet",
    "63.127.184.46": "Caroline Rd Internet",
    "10.1.113.111": "Printfly Ripping ESXi",
    "10.1.113.215": "Printfly Backup Ripping ESXi",
    "10.2.96.16": "Mach6 Ripping ESXi",
    "10.2.96.17": "Mach6 Ripping ESXI 2",
    "10.1.113.211": "Printfly Truenas HQ",
    "10.2.96.99": "mach6 Truenas",
    "10.1.113.20": "Printfly DC01",
    "10.1.113.21": "Printfly DC02",
    "10.1.113.110": "Unifi Camera UNVR",
    "10.1.113.1": "Print fly Cisco Switch",
    "10.1.103.240":"PRINTFLY-RIP-51",
    "10.1.103.241":"PRINTFLY-RIP-52",
    "10.1.103.242":"PRINTFLY-RIP-53",
    "10.1.103.243":"PRINTFLY-RIP-54",
    "10.1.103.244":"PRINTFLY-RIP-55",
    "10.1.103.245":"PRINTFLY-RIP-56",
    "10.1.113.50":"PRINTFLY-RIPPER-57",
    "10.1.113.51":"PRINTFLY-RIPPER-58",
    "10.1.113.52":"PRINTFLY-RIPPER-59",
    "10.1.113.53":"PRINTFLY-RIPPER-60",
    "10.1.113.54":"PRINTFLY-RIPPER-61",
    "10.1.113.55":"PRINTFLY-RIPPER-62",
    "10.2.96.81":"Mach6-Ripper-101",
    "10.2.96.82":"Mach6-Ripper-102",
    "10.2.96.83":"Mach6-Ripper-103",
    "10.2.96.84":"Mach6-Ripper-104",
    "10.2.96.85":"Mach6-Ripper-105",
    "10.2.96.86":"Mach6-Ripper-106",
    "10.2.96.87":"Mach6-Ripper-107",
    "10.2.96.88":"Mach6-Ripper-108",
    "10.2.96.89":"Mach6-Ripper-109",
    "10.2.96.90":"Mach6-Ripper-110",
    "10.2.96.91":"Mach6-Ripper-111",
    "10.2.96.92":"Mach6-Ripper-112"
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

