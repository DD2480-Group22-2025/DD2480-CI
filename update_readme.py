'''Module to update the README.md file with the ngrok URL from the latest successful build.'''

import requests
import re
import subprocess

README_FILE = "README.md"

def get_public_url():
    '''Fetch the public ngrok URL'''
    try:
        response = requests.get("http://localhost:4022/api/tunnels")
        response.raise_for_status()
        
        # Parse the JSON response
        response_json = response.json()
        
        # Extract the public URL from the first tunnel object
        if "tunnels" in response_json and len(response_json["tunnels"]) > 0:
            public_url = response_json["tunnels"][0].get("public_url")
            if public_url:
                return public_url
            else:
                print("Error: No public_url found in the tunnel response.")
                return None
        else:
            print("Error: No tunnels found in the response.")
            return None
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching ngrok URL: {e}")
        return None

    
def update_readme(public_url):
    '''Update the README.md file with the the latest ngrok URL'''
    if public_url is None:
        print("No public URL fetched. README.md will not be updated.")
        return
    
    with open(README_FILE, "r", encoding = "utf-8") as file:
        content = file.read()
        new_content = re.sub(r"\[FastAPI CI Build List\]\(https://.*?\)",f"[FastAPI CI Build List]({public_url}/builds)",content)
    
    if content != new_content:
        with open(README_FILE, "w", encoding = "utf-8") as file:
            file.write(new_content)
            print(f"Updated README.md with the public URL: {public_url}")
    else:
        print("README.md is up to date. No changes required.")

def commit_readme():
    '''Automatically commit the README changes to git'''
    subprocess.run(["git", "add", "README.md"])
    subprocess.run(["git", "commit", "-m", "Updated README.md with the latest public URL"])
    subprocess.run(["git", "push","origin","main"])


if __name__ == "__main__":
    public_url = get_public_url()
    if public_url:
        update_readme(public_url)
        commit_readme()