import os
import sys
import json
import urllib.request
import urllib.error

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"

    try:
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode())
                return data
    
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found ")
        else:
            print(f"Error: Could not fetch data (Status Code: {e.code})")
        return None
    
    except Exception as e :
        print(f"An unexpected error occurred: {e}")
        return None
    
def main():
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        return
    
    username = sys.argv[1]
    activities = fetch_github_activity(username)

    if not activities:
        return
    
    print(f"Recent activity for {username}:")
    print("-" * 30)

    for event in activities[:10]:
        event_type = event.get("type")
        repo_name = event.get("repo", {}).get("name")

        if event_type == "PushEvent":
            commit_count = event.get("payload", {}).get("size", 0)
            print(f"- Pushed {commit_count} commit(s) to {repo_name}")

        elif event_type == "IssuesEvent":
            action = event.get("payload", {}).get("action")
            print(f"- {action.capitalize()} an issue in {repo_name}")

        elif event_type == "WatchEvent":
         print(f"- Starred {repo_name}")

        elif event_type == "CreateEvent":
            ref_type = event.get("payload", {}).get("ref_type")
            print(f"- Created a {ref_type} in {repo_name}")

        else:
            clean_name = event_type.replace("Event", "")
            print(f"- {clean_name} in {repo_name}")

if __name__ == "__main__":
    main()