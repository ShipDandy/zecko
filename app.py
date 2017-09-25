"""
Zecko: bringing zendesk user metrics into geckoboard
Author: Zeke (Joe) Brower
Version 0.99
2017-09-13
"""
from flask import Flask, jsonify, request
import requests, re, datetime
import zd_creds, agents, tickets, chats

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify("Get Outta Here Would Ya!")

stuff = [
    {
        "title": {"text": "Chats Taken: 8"}
    },
    {
        "title": {"text": "Tickets in OPEN: 2"}
    },
    {
        "title": {"text": "Tickets in SOLVED: 99"}
    }
]

@app.route("/sample")
def sample():
    return jsonify(stuff)

@app.route("/agents")
def list_agents():
    return jsonify(agents.list_agents_in_db())

@app.route("/agents/build_db")
def build_db():
    pass

@app.route("/agents/update_db")
def update_database():
    return jsonify(update_database())

@app.route("/agents/add_agent", methods=["POST"])
def add_agent():
    data = request.get_json()
    agent_spec = (data["zd_id"], data["agentName"])
    return jsonify(agents.add_agent_to_db(agent_spec))

@app.route("/agents/delete_agent", methods=["DELETE"])
def delete_agent(name):
    data = request.get_json()
    return jsonify(agents.delete_agent_from_db(data["zd_id"]))

@app.route("/agents/update_name", methods=["PUT"])
def update_name():
    data = request.get_json()
    return jsonify(agents.update_agent_name(data["newName"], data["zd_id"]))

@app.route("/metrics/<string:name>")
def get_agent_metrics(name):
    siftName = name.replace("_", " ")
    zd_id = agents.get_agent_id(siftName)

    both_tickets = tickets.agent_tickets(zd_id)
    open_tickets = both_tickets[0]
    solved_tickets = both_tickets[1]
    days_chats = chats.chats_taken(siftName)

    current_metrics = [
    {
    "title": {"text": "Chats Taken: " + days_chats}
    },
    {
    "title": {"text": "Tickets in OPEN: " + open_tickets}
    },
    {
    "title": {"text": "Tickets in SOLVED: " + solved_tickets}
    }
    ]

    return jsonify(current_metrics)

### Chat Info ###

@app.route("/chats/active_chats")
def active_chats():
    return jsonify(chats.active_chats_all())

@app.route("/chats/average_wait")
def average_wait_time():
    return jsonify(chats.get_average_wait())

@app.route("/chats/average_chat")
def average_chat_time():
    return jsonify(chats.get_average_chat())

@app.route("/chats/incoming_chats")
def incoming_chats():
    return jsonify(chats.get_incoming_chats())

@app.route("/chats/online_status")
def online_status():
    return jsonify(chats.get_online_status())

if __name__ == "__main__":
    app.run()