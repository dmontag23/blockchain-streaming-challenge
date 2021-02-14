import logging
import smtplib
import ssl
from utilities.database_utilities import execute_sql_statement

def report_total_number_of_users():
    users = ""
    user_count = execute_sql_statement("SELECT COUNT(*) FROM location;")[0][0]
    users += str(user_count)
    return users

def report_users_by_state():
    users_by_state = ""
    for row in execute_sql_statement("SELECT state, COUNT(*) AS count FROM location GROUP BY state ORDER BY count DESC;"):
        if row[0]:
            users_by_state += row[0] + ": " + str(row[1]) + "\n"
        else:
            users_by_state += "Unknown: " + str(row[1]) + "\n"
    return users_by_state

def report_users_by_city():
    users_by_state = ""
    for row in execute_sql_statement("SELECT city, COUNT(*) AS count FROM location GROUP BY city ORDER BY count DESC LIMIT 10;"):
        users_by_state += row[0].title() + ": " + str(row[1]) + "\n"
    return users_by_state

def send_report(email_list, message):
    port = 465
    sender_email = "dillondatapipeline@gmail.com"
    password = "Blockchain"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Send emails
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        logging.info("Logging into " + sender_email)
        server.login(sender_email, password)
        logging.info("Sending emails...")
        for receiver_email in email_list:
            server.sendmail(sender_email, receiver_email, message)
    logging.info("Emails sent!")

def generate_email_report():
    receiver_emails = ["dillondatapipeline@gmail.com"]
    subject = "Your User Report!"
    text = "Hi there!\n\nThis is your friendly Python Robot with you new user report.\n\n"
    text += "The total number of users is now: " + report_total_number_of_users() + "\n\n"
    text += "Here are the cities with the most user activity : \n\n" + report_users_by_city() + "\n"
    text += "The number of users by state is: \n\n" + report_users_by_state() + "\n"
    text += "That's all for now! Have a fantastic day :-)"
    message = 'Subject: {}\n\n{}'.format(subject, text)
    send_report(receiver_emails, message)
