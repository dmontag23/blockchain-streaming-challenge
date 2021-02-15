"""
The reporting.py class provides helper functions to generate email reports.
"""

import logging
import smtplib
import ssl
from utilities.database_utilities import execute_sql_statement

def report_null_users():
    """
    Reports the total number of users with null in both the "state" and "postcode" field

    :returns: The number of users with null in both the "state" and "postcode" field
    :rtype: str
    """

    null_users = ""
    null_user_count = execute_sql_statement("SELECT COUNT(*) FROM location WHERE state IS NULL AND postcode IS NULL;")[0][0]
    null_users += str(null_user_count)
    return null_users

def report_total_number_of_users():
    """
    Reports the total number of users in the database as a string

    :returns: The total number of users in the database
    :rtype: str
    """

    users = ""
    user_count = execute_sql_statement("SELECT COUNT(*) FROM location;")[0][0]
    users += str(user_count)
    return users

def report_users_by_state():
    """
    Reports the total number of users in each state in the database as a string

    :returns: The total number of users in each state in the database
    :rtype: str
    """

    users_by_state = ""
    for row in execute_sql_statement("SELECT state, COUNT(*) AS count FROM location GROUP BY state ORDER BY count DESC;"):
        if row[0]:
            users_by_state += row[0] + ": " + str(row[1]) + "\n"
        else:
            users_by_state += "Unknown: " + str(row[1]) + "\n"
    return users_by_state

def report_users_by_city():
    """
    Reports the total number of users by city in the database as a string

    :returns: The 10 states with the highest user activity in the database
    :rtype: str
    """

    users_by_state = ""
    for row in execute_sql_statement("SELECT city, COUNT(*) AS count FROM location GROUP BY city ORDER BY count DESC LIMIT 10;"):
        users_by_state += row[0].title() + ": " + str(row[1]) + "\n"
    return users_by_state

def send_email_report(email_list, message):
    """
    Sends an email with the message text to everyone in the email list

    :param email_list: The list of emails to send the report to
    :type email_list: list
    :param message: The message to send in the email
    :type message: str

    :returns: None
    :rtype: None
    """

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
    """
    Generates an email report on the current user base

    :returns: None
    :rtype: None
    """

    receiver_emails = ["dillondatapipeline@gmail.com"]
    subject = "Your User Report!"
    text = "Hi there!\n\nThis is your friendly Python Robot with you new user report.\n\n"
    text += "The total number of users is now: " + report_total_number_of_users() + ". However, " + report_null_users() + \
            " users do not have a valid state or postcode, and so these records are unlikely to be helpful. \n\n"
    text += "Here are the cities with the most user activity : \n\n" + report_users_by_city() + "\n"
    text += "The number of users by state is: \n\n" + report_users_by_state() + "\n"
    text += "That's all for now! Have a fantastic day :-)"
    message = 'Subject: {}\n\n{}'.format(subject, text)
    send_email_report(receiver_emails, message)
