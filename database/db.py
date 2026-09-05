"""
Run this on YOUR OWN COMPUTER (not on Streamlit Cloud) to test whether
your Turso database is reachable and your credentials are valid.

How to use:
1. pip install libsql
2. Fill in TURSO_DATABASE_URL and TURSO_AUTH_TOKEN below (copy the exact
   values from Streamlit Cloud > Settings > Secrets, or from your local
   .streamlit/secrets.toml).
3. Run:  python test_turso_connection.py
4. Watch what happens:
   - Prints "SUCCESS" quickly (a few seconds)  -> Turso itself is fine,
     the problem is specific to Streamlit Cloud's network/environment.
   - Hangs forever with no output               -> Turso URL/token/db is
     the real problem (wrong region, expired token, paused/deleted db).
   - Prints an error message quickly            -> read the error, it
     usually says exactly what's wrong (auth failed, host not found, etc).
   If it hangs, press Ctrl+C to stop it, then report back what you saw.
"""
import time

TURSO_DATABASE_URL = "PASTE_YOUR_URL_HERE"   # e.g. libsql://abhishek-singh-abhibhdauriya.aws-ap-south-1.turso.io
TURSO_AUTH_TOKEN = "PASTE_YOUR_TOKEN_HERE"

print("Starting connection attempt...")
start = time.time()

try:
    import libsql
    conn = libsql.connect("test_local_replica.db", sync_url=TURSO_DATABASE_URL, auth_token=TURSO_AUTH_TOKEN)
    print(f"connect() returned after {time.time() - start:.2f}s, now syncing...")

    conn.sync()
    print(f"sync() SUCCESS after {time.time() - start:.2f}s total")

    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    print("Tables found:", tables)

except Exception as e:
    print(f"FAILED after {time.time() - start:.2f}s with error:")
    print(repr(e))
