import requests
import csv
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import boto.s3
import sys


###########DEFINE METHODS###########

def send_email(email):


    email = str(email)

    requests.post(
        "https://api.mailgun.net/v3/sandboxa73d43ac6038480e9088319df0574fc6.mailgun.org/messages",
        auth=("api", "key-"),
        data={"from": "Excited User <postmaster@sandboxa73d43ac6038480e9088319df0574fc6.mailgun.org>",
              "to": [email],
              "subject": "Hello",
              "text": "Please add a name to your GitHub account, visit https://github.com/settings/profile to add your name"})


def send_s3(login):
    print('sending S3')

    import boto
    from boto.s3.key import Key

    #setup the bucket
    c = boto.connect_s3('', '')
    b = c.get_bucket('bhmc12345', validate=False)

    k=Key(b)
    k.key = "Nameless GitHub User {}".format(login)
    k.set_contents_from_string('Here is the login name of the nameless GitHub users {}'.format(login))


payload = {'access_token': '19b60ee773c227399a8daee641fe13e25701fc3d'}
team_members = requests.get('https://api.github.com/orgs/myOrgBYU/members', params=payload)


my_json_team = team_members.json()

no_name = []
    #print all team member's information
for item in my_json_team:

    user = requests.get('https://api.github.com/users/{}'.format(item['login']))
    my_member = user.json()
    
    if my_member['name'] == None:
        no_name.append(my_member)

for item in no_name:
    print(item)
    send_email(item['email'])

    send_s3(item['login'])



