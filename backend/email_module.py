import smtplib
import os

def send_activation_link(to_email=1, token=1):
    gmail_user = os.environ['PE_BUNE_EMAIL']
    gmail_password = os.environ['PE_BUNE_PASSWORD']

    sent_from = os.environ['PE_BUNE_EMAIL']

    to = [to_email]
    subject = 'Pe bune?! Activation link'
    body = """\
    Hello and thanks for registration!\n\n
    Here is your activation link:\n
    %s\n\n
    David
    """ % ('https://www.pebune.davidrosu.tech/api/confirm/' + token)

    email_text = '\r\n'.join(['To: %s' % ','.join(to),
                    'From: %s' % sent_from,
                    'Subject: %s' % subject,
                    '', body])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        
        return True
    except:
        return False
