import requests, re, sqlite3

import zd_creds

def get_zdc_departments():
    get_agent_list = requests.get("https://www.zopim.com/api/v2/departments", headers=zd_creds.zdc_headers)

    member_grab = re.compile(r'members.\:\s\[(.+?)\]')
    step1 = member_grab.findall(str(get_agent_list.text))
    
    just_numbers = re.compile(r'(\d+)')
    step2 = just_numbers.findall(str(step1))

    return step2

zdc_numbers = get_zdc_departments()

def get_ids(each):
    zdc_agent_info = requests.get("https://www.zopim.com/api/v2/agents/" + each, headers=zd_creds.zdc_headers)
    agent_info_dic = zdc_agent_info.text
    get_agent_name = re.compile(r'first_name.+?\"(.+?)\"')
    agent_name = get_agent_name.search(agent_info_dic).group(1)

    return (each, agent_name)


def build_agent_db(zdc_numbers):
    runninglist = []
    connection = sqlite3.connect("zdAgents.db")
    cursor = connection.cursor()

    create_table = "CREATE TABLE agents (id text, agentName text)"
    cursor.execute(create_table)

    for each in zdc_numbers:
        if each in runninglist:
            print(each + " is a duplicate, pass-a-roo!")
        else:
            runninglist.append(each)
            print(str(get_ids(each)) + " added.")
            agent_spec = get_ids(each)
            insert_query = "INSERT INTO agents VALUES (?, ?)"
            cursor.execute(insert_query, agent_spec)

    connection.commit()
    connection.close()

    print("donezo")

#build_agent_db(zdc_numbers)

def update_database():
    fresh_list = get_zdc_departments()
    update_count = 0

    for each in fresh_list:
        connection = sqlite3.connect("zdAgents.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM agents WHERE id={}".format(each)
        result = cursor.execute(select_query)
        result2 = result.fetchone()

        if result2 != None:
            pass
        else:
            update_count += 1
            agent_spec = get_ids(each)
            insert_query = "INSERT INTO agents VALUES (?, ?)"
            cursor.execute(insert_query, agent_spec)

        connection.commit()
        connection.close()
    return "{} agents added to database".format(update_count)

def list_agents_in_db():
    agent_list = []
    connection = sqlite3.connect("zdAgents.db")
    cursor = connection.cursor()

    select_query = "SELECT * FROM agents"
    result = cursor.execute(select_query)
    result2 = result.fetchall()

    for each in result2:
        agent_list.append({each[1]: {"id":each[0]}})

    connection.commit()
    connection.close()

    return agent_list

def delete_agent_from_db(agent_id):
    connection = sqlite3.connect("zdAgents.db")
    cursor = connection.cursor()

    delete_entry = "DELETE FROM agents WHERE id={}".format(agent_id)
    cursor.execute(delete_entry)

    connection.commit()
    connection.close()

    return "Agent {} removed from database.".format(agent_id)

def add_agent_to_db(agent_spec):
    connection = sqlite3.connect("zdAgents.db")
    cursor = connection.cursor()

    select_query = "SELECT * FROM agents WHERE id={}".format(agent_spec[0])
    result = cursor.execute(select_query)
    result2 = result.fetchone()

    message = "default"

    if result2 != None:
        message = "Agent ID {} already present in database.".format(agent_spec[0])
    else:
        insert_query = "INSERT INTO agents VALUES (?, ?)"
        cursor.execute(insert_query, agent_spec)
        message = "Agent {}, Zendesk ID {} added to database.".format(agent_spec[1], agent_spec[0])

    connection.commit()
    connection.close()

    return message

def update_agent_name(newName, agent_id):
    connection = sqlite3.connect("zdAgents.db")
    cursor = connection.cursor()

    update_name = "UPDATE agents SET agentName=\'{}\' WHERE id={}".format(newName, agent_id)
    cursor.execute(update_name)

    connection.commit()
    connection.close()

    return "Agent name changed to {}.".format(newName)

def get_agent_id(agentName):
    connection = sqlite3.connect("zdAgents.db")
    cursor = connection.cursor()

    select_query = "SELECT id FROM agents WHERE agentName=\'{}\'".format(agentName)
    result = cursor.execute(select_query)
    result_id = result.fetchone()

    return result_id[0]

    connection.commit()
    connection.close()