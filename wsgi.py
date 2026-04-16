from app import app, init_db
import time

# Retry init_db a few times in case DB isn't ready yet
for attempt in range(5):
    try:
        init_db()
        break
    except Exception as e:
        print(f"DB not ready (attempt {attempt+1}/5): {e}")
        time.sleep(2)

