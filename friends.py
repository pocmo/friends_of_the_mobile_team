#!/usr/bin/env python2

from datetime import datetime, timedelta
import urllib

URL = 'https://bugzilla.mozilla.org/buglist.cgi'

CONST_PARAMS = [
    'query_format=advanced',
    'list_id=12431522',  # WTF
    'product=Android%20Background%20Services',
    'product=Firefox%20for%20Android',
    'product=Firefox%20for%20iOS',
    'chfield=bug_status',
    'bug_status=RESOLVED',
    'chfieldvalue=RESOLVED',
    'chfieldto=Now',
]
DATE_PARAM = 'chfieldfrom={}'  # YYYY-MM-DD

EMAIL_LINE = 'email{}={}'
EMAIL_NUM_PARAM_LINES = [
    'emailtype{}=notequals',
    'emailassigned_to{}=1',
]

def generate_email_params(address, count):
    out = []
    for line in EMAIL_NUM_PARAM_LINES:
        out.append(line.format(count))
    out.append(EMAIL_LINE.format(count, urllib.quote(address)))
    return out

def generate_date_param():
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    return DATE_PARAM.format(seven_days_ago)

date_param = generate_date_param()
email_params = []
with open('emails.txt', 'r') as f:
    for i, email in enumerate(f, start=1):
        email_params.extend(generate_email_params(email, i))

params = '&'.join(CONST_PARAMS + [date_param] + email_params)
out = URL + '?' + params
print(out)
