import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import json

# Load the JSON data from the file
with open('/home/khaleel/Ansible/VMWare/output/power_status_output.json', 'r') as json_file:
    data = json.load(json_file)

# Extract power status for each virtual machine
vm_power_statuses = {}
for vm in data['virtual_machines']:
    vm_name = vm['guest_name']
    power_state = vm['power_state']
    vm_power_statuses[vm_name] = power_state

# Create an HTML table with a stylish design
html_table = '''
<style>
    table {
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
    }

    th, td {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
    }

    th {
        background-color: #4CAF50;
        color: white;
    }

    tr:nth-child(even) {
        background-color: #ffffff;
    }

    tr:nth-child(odd) {
        background-color: #f2f2f2;
    }
</style>
<table>
    <tr>
        <th>VM Name</th>
        <th>Status</th>
    </tr>
'''

for vm_name, power_state in vm_power_statuses.items():
    status_color = 'green' if power_state == 'poweredOn' else 'red'
    html_table += f'''
    <tr>
        <td>{vm_name}</td>
        <td style="color: {status_color}; font-weight: bold;">{power_state}</td>
    </tr>
    '''

html_table += '</table>'

# Define your Gmail and SMTP server settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'khaleel.org@gmail.com'  # Your Gmail email address
smtp_password = 'Gmail_Application_Password'  # Your Gmail password

# Create a connection to the SMTP server
smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
smtp_connection.starttls()  # Use TLS encryption

# Log in to your Gmail account
smtp_connection.login(smtp_username, smtp_password)

# Create the email message
subject = 'Ansible Ubuntu-OS'
from_email = 'khaleel.org@gmail.com'
to_email = ['khaleel.org@gmail.com', 'tmail.khalil@gmail.com']

# Create a MIME message
message = MIMEMultipart()
message['From'] = from_email
message['To'] = ', '.join(to_email)
message['Subject'] = subject

# Add HTML body to the email
HTMLBody = f"VMWare Power Status | {datetime.datetime.now()}<br><br>{html_table}"
message.attach(MIMEText(HTMLBody, 'html'))

# Attach the JSON file
json_attachment = '/home/khaleel/Ansible/VMWare/output/power_status_output.json' 
with open(json_attachment, 'rb') as json_file:
    json_data = MIMEApplication(json_file.read(), Name='power_status_output.json')

json_data['Content-Disposition'] = f'attachment; filename="{json_attachment}"'
message.attach(json_data)

# Send the email
smtp_connection.sendmail(from_email, to_email, message.as_string())

# Close the SMTP connection
smtp_connection.quit()

print("Email Sent Successfully!")

