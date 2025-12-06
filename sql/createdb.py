import psycopg2
from psycopg2 import sql

# DB connection parameters
DB_USER = "vxrun"
DB_PASS = "vxrun"
DB_HOST = "localhost"
DB_PORT = 5432
# DB connection function
def connect_postgres_db(dbname="postgres"):
    """Connect to a PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=dbname,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
    )
    conn.autocommit = True
    return conn

def create_database(dbname):
    """Create the database if it doesn't exist."""
    conn = connect_postgres_db()
    cur = conn.cursor()

    # Check if DB exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (dbname,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(dbname)))
        print(f"Database '{dbname}' created.")
    else:
        print(f"Database '{dbname}' already exists.")

    cur.close()
    conn.close()

def create_tables(dbname):
    """Create the required tables inside the given database."""
    conn = connect_postgres_db(dbname=dbname)
    cur = conn.cursor()

    # Create users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            uid SERIAL PRIMARY KEY
        );
    """)

    # # Create chat_history table
    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS chat_history (
    #         chatid SERIAL PRIMARY KEY,
    #         uid INTEGER REFERENCES users(uid),
    #         chat JSONB,  -- storing chat as JSON for flexibility
    #         date DATE,
    #         time TIME,
    #         eid INTEGER NULL
    #     );
    # """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            chatid SERIAL PRIMARY KEY,
            uid INTEGER REFERENCES users(uid),
            chat JSONB,  -- storing chat as JSON for flexibility
            date DATE,
            time TIME,
            eid INTEGER NULL,
            sentimentStatus VARCHAR(20) DEFAULT 'pending'  -- new column added
        );
    """)

    # Create sentiments table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sentiments (
            chatid INTEGER REFERENCES chat_history(chatid),
            sentiment VARCHAR(50),
            PRIMARY KEY (chatid)
        );
    """)

    # Create escalation table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS escalation (
            eid SERIAL PRIMARY KEY,
            chatid INTEGER REFERENCES chat_history(chatid),
            status VARCHAR(50),
            remarks TEXT,
            dept VARCHAR(100)
        );
    """)

    print("Tables created successfully in database:", dbname)

    cur.close()
    conn.close()




if __name__ == "__main__":
    dbname = "CustomerSupport"
    create_database(dbname)
    create_tables(dbname)
