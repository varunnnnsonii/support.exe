import psycopg2
# Function to list all databases in PostgreSQL
def list_databases():
    try:
        # Connect to the default 'postgres' database
        conn = psycopg2.connect(
            dbname="postgres",
            user="vxrun",
            password="vxrun",
            host="localhost"
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Query to list all databases
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cur.fetchall()

        print("Available Databases:")
        for db in databases:
            print(f"- {db[0]}")

        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)
# List tables and their columns in a PostgreSQL database
def list_tables_with_columns(dbname):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user="vxrun",
            password="vxrun",
            host="localhost"
        )
        cur = conn.cursor()

        # Fetch table names
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """)
        tables = cur.fetchall()

        print(f"\nTables in database '{dbname}':\n")

        for table in tables:
            table_name = table[0]
            print(f"🔹 {table_name}")

            # Fetch columns for each table
            cur.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = %s;
            """, (table_name,))
            columns = cur.fetchall()

            for col_name, data_type in columns:
                print(f"   - {col_name}: {data_type}")
            print()  # Newline for separation

        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

# Call the function
if __name__ == "__main__":
    list_databases()
    list_tables_with_columns("CustomerSupport")