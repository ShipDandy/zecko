import requests, re, datetime

import zd_creds

def agent_tickets(zd_id):
    query_date = str(datetime.date.today())
    open_ticket_raw = requests.get("https://shipstation.zendesk.com/api/v2/search.json?query=type:ticket status:open assignee:" + zd_id, headers=zd_creds.zd_headers)

    solved_ticket_raw = requests.get("https://shipstation.zendesk.com/api/v2/search.json?query=type:ticket status:solved assignee:" + zd_id + " solved:" + query_date, headers=zd_creds.zd_headers)

    payload_open = str(open_ticket_raw.json()["count"])
    payload_solved = str(solved_ticket_raw.json()["count"])

    return payload_open, payload_solved

