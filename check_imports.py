import sys
import os
sys.path.append(os.getcwd())

try:
    from backend.server_receive import save_meeting_data_to_db
    print("Successfully imported save_meeting_data_to_db")
except Exception as e:
    print(f"Failed to import: {e}")
