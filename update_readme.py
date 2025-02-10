'''Module to update the README.md file with the latest ngrok URL.'''

import requests
import re
import subprocess

README_FILE = "README.md"

def get_ngrok_url():
    '''Fetch the public ngrok URL'''
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        response.raise_for_status()
        data = response.json()
        return  data["tunnels"][0]["public_url"]
    except (requests.RequestException, IndexError, KeyError):
        print("Error: Unable to fetch ngrok URL")
        return None
    
def update_readme(ngrok_url):
    '''Update the README.md file with the the latest ngrok URL'''
    if ngrok_url is None:
        print("No ngrok URL fetched. README.md will not be updated.")
        return
    with open(README_FILE, "r", encoding = "utf-8") as file:
        content = file.read()
        new_content = re.sub(r"\[FastAPI CI Build List\]\(https://.*?\)",f"[FastAPI CI Build List]({ngrok_url}/builds)",content)
    
    with open(README_FILE, "w", encoding = "utf-8") as file:
        file.write(new_content)
    
    print(f"Updated README.md with ngrok URL: {ngrok_url}")

def commit_readme():
    '''Automatically commit the README changes to git'''
    subprocess.run(["git", "add", "README.md"])
    subprocess.run(["git", "commit", "-m", "Updated README.md with the latest ngrok URL"])
    subprocess.run(["git", "push"])


if __name__ == "__main__":
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        update_readme(ngrok_url)
        commit_readme()
    