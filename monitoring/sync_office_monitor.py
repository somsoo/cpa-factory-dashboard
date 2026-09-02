import os
import json
import time
import subprocess
from datetime import datetime

LOG_FILE = r"C:\Users\hsm29\.gemini\antigravity\brain\8e80c36e-a05d-43f7-8910-a92553980485\.system_generated\logs\transcript.jsonl"
STATUS_FILE = r"C:\Users\hsm29\Documents\total-system-dashboard\monitoring\onepage_status.json"
REPO_DIR = r"C:\Users\hsm29\Documents\total-system-dashboard"

def parse_logs_for_status():
    status = {
        "frontend_dev": {"name": "Frontend Dev", "emoji": "🧑‍💻", "status": "IDLE", "message": "대기 중"},
        "seo_copywriter": {"name": "SEO Planner", "emoji": "✍️", "status": "IDLE", "message": "대기 중"},
        "qa_reviewer": {"name": "QA Reviewer", "emoji": "🕵️", "status": "IDLE", "message": "대기 중"},
        "main_agent": {"name": "Factory Manager (Main)", "emoji": "🤖", "status": "RUNNING", "message": "작업 모니터링 중..."}
    }
    
    if not os.path.exists(LOG_FILE):
        return status

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Parse the last 500 lines to find recent agent activity
        for line in lines[-500:]:
            try:
                data = json.loads(line)
                
                # Check for subagent invocation (RUNNING)
                if data.get('type') == 'PLANNER_RESPONSE' and 'tool_calls' in data:
                    for tool in data['tool_calls']:
                        if tool.get('name') == 'invoke_subagent':
                            args = tool.get('arguments', {})
                            for agent in args.get('Subagents', []):
                                role = agent.get('TypeName', '')
                                if 'frontend' in role.lower():
                                    status['frontend_dev']['status'] = 'RUNNING'
                                    status['frontend_dev']['message'] = 'UI/UX 코드 수정 중...'
                                elif 'seo' in role.lower() or 'copywriter' in role.lower():
                                    status['seo_copywriter']['status'] = 'RUNNING'
                                    status['seo_copywriter']['message'] = 'SEO 및 약관 작성 중...'
                                elif 'qa' in role.lower() or 'reviewer' in role.lower():
                                    status['qa_reviewer']['status'] = 'RUNNING'
                                    status['qa_reviewer']['message'] = '코드 검수 중...'
                                    
                # Check for system messages (subagent finished -> IDLE)
                if data.get('type') == 'SYSTEM_MESSAGE':
                    content = data.get('content', '')
                    if 'finished with result' in content or 'has been successfully refactored' in content:
                        # Simple heuristic to mark them idle again based on recent logs
                        pass
                        
            except:
                continue
    except Exception as e:
        print(f"Error reading log: {e}")
        
    return status

def main():
    print("Starting Virtual Office Sync Daemon...")
    while True:
        status_data = parse_logs_for_status()
        
        output = {
            "last_updated": datetime.now().isoformat(),
            "agents": status_data
        }
        
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            
        # Push to Git (every 60 seconds to avoid spam)
        subprocess.run(["git", "add", "monitoring/onepage_status.json"], cwd=REPO_DIR, stdout=subprocess.DEVNULL)
        res = subprocess.run(["git", "commit", "-m", "Auto-sync: Virtual Office Status Update"], cwd=REPO_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if res.returncode == 0:
            subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status pushed to GitHub.")
            
        time.sleep(60)

if __name__ == "__main__":
    main()
