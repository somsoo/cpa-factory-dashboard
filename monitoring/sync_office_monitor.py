import os
import json
import time
import subprocess
from datetime import datetime

LOG_FILE = r"C:\Users\hsm29\.gemini\antigravity\brain\8e80c36e-a05d-43f7-8910-a92553980485\.system_generated\logs\transcript.jsonl"
STATUS_FILE = r"C:\Users\hsm29\Documents\total-system-dashboard\monitoring\onepage_status.json"
REPO_DIR = r"C:\Users\hsm29\Documents\total-system-dashboard"

def parse_logs():
    agents = {}
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    step_type = data.get('type')
                    
                    if step_type == 'SYSTEM_MESSAGE':
                        content = data.get('content', '')
                        if '[Message]' in content and 'sender=' in content:
                            parts = content.split('sender=')
                            if len(parts) > 1:
                                sender_id = parts[1].split(' ')[0]
                                if sender_id.startswith('8e80c36e'):
                                    continue
                                msg_content = content.split('content=')[-1].strip()
                                
                                if sender_id not in agents:
                                    agents[sender_id] = {
                                        "id": sender_id,
                                        "name": f"에이전트 [{sender_id[:6]}]",
                                        "status": "RUNNING",
                                        "last_message": msg_content
                                    }
                                else:
                                    agents[sender_id]["last_message"] = msg_content
                                    if 'finished with result' in msg_content or '완료' in msg_content or '저장' in msg_content:
                                        agents[sender_id]["status"] = "IDLE/FINISHED"
                except:
                    continue
    except Exception as e:
        print("Error:", e)
        
    return list(agents.values())

def main():
    print("Starting Enhanced Virtual Office Sync Daemon...")
    while True:
        agents_list = parse_logs()
        all_idle = True
        
        for a in agents_list:
            if a["status"] == "RUNNING":
                all_idle = False
                
        output = {
            "last_updated": datetime.now().isoformat(),
            "agents": agents_list
        }
        
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        subprocess.run(["git", "add", "monitoring/onepage_status.json"], cwd=REPO_DIR, stdout=subprocess.DEVNULL)
        res = subprocess.run(["git", "commit", "-m", "Auto-sync: Subagents Detail Update"], cwd=REPO_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if res.returncode == 0:
            subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status pushed.")

        # Auto-shutdown logic
        if len(agents_list) > 0 and all_idle:
            print("모든 에이전트 작업 완료. 리소스(토큰) 절약을 위해 관제 데몬을 종료합니다.")
            break
            
        time.sleep(15)

if __name__ == "__main__":
    main()
