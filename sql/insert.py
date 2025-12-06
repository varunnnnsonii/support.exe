import psycopg2

# DB connection parameters
DB_USER = "vxrun"
DB_PASS = "vxrun"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "CustomerSupport"

def connect_postgres_db(dbname=DB_NAME):
    conn = psycopg2.connect(
        dbname=dbname,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    return conn

def insert_user():
    conn = connect_postgres_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO users DEFAULT VALUES RETURNING uid;")
    uid = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"Inserted user with uid={uid}")
    return uid

def insert_chat_history(uid, chat_json, date, time):
    conn = connect_postgres_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO chat_history (uid, chat, date, time)
        VALUES (%s, %s, %s, %s)
        RETURNING chatid;
    """, (uid, chat_json, date, time))
    chatid = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(f"Inserted chat_history with chatid={chatid}")
    return chatid

def insert_or_update_sentiment(chatid, sentiment):
    conn = connect_postgres_db()
    cur = conn.cursor()
    
    # Upsert sentiment (insert or update if exists)
    cur.execute("""
        INSERT INTO sentiments (chatid, sentiment)
        VALUES (%s, %s)
        ON CONFLICT (chatid) DO UPDATE SET sentiment = EXCLUDED.sentiment;
    """, (chatid, sentiment))

    # Update sentimentStatus in chat_history to 'not pending'
    cur.execute("""
        UPDATE chat_history
        SET sentimentStatus = 'not pending'
        WHERE chatid = %s;
    """, (chatid,))
    
    cur.close()
    conn.close()
    print(f"Inserted/Updated sentiment for chatid={chatid}")

def insert_escalation(chatid, status, remarks, dept):
    conn = connect_postgres_db()
    cur = conn.cursor()
    # Insert escalation and get eid
    cur.execute("""
        INSERT INTO escalation (chatid, status, remarks, dept)
        VALUES (%s, %s, %s, %s)
        RETURNING eid;
    """, (chatid, status, remarks, dept))
    eid = cur.fetchone()[0]
    
    # Update eid in chat_history for this chatid
    cur.execute("""
        UPDATE chat_history
        SET eid = %s
        WHERE chatid = %s;
    """, (eid, chatid))
    
    cur.close()
    conn.close()
    print(f"Inserted escalation eid={eid} for chatid={chatid}")
    return eid

# Example usage
if __name__ == "__main__":
    import datetime
    import json
    
    # 1. Insert user
    uid = insert_user()
    
    # 2. Insert chat_history
    chat_example = [{"sender":"user","message":"Hello"},{"sender":"agent","message":"Hi, how can I help?"}]
    chat_json = json.dumps(chat_example)  # Must be JSON string for JSONB
    
    today = datetime.date.today()
    now = datetime.datetime.now().time()
    
    chatid = insert_chat_history(uid, chat_json, today, now)
    
    # 3. Insert/update sentiment (initially pending, later update)
    insert_or_update_sentiment(chatid, "positive")

    # 4. Insert escalation
    eid = insert_escalation(chatid, "open", "Customer requested escalation", "support")