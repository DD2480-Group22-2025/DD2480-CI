from fastapi import APIRouter, Request, HTTPException
import os
from github import Github  # PyGithub library
from dotenv import load_dotenv

# Load environment variables from a .env file, if present
load_dotenv()

router = APIRouter()

#Updating the status of a commit on GitHub
def update_commit_status(commit_sha: str, state: str, description: str, context: str = "CI Notification") -> dict:
    """
    commit_sha: The commit hash (SHA) to update.
    state: The build status ("pending", "success", or "failure").
    description: A short message describing the build result.
    context: A label for this status (default "CI Notification").
    """

    # Retive GitHub token and repo details
    token = os.getenv("CI_SERVER_AUTH_TOKEN")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    
    # Ensure all required configuration values are present
    if not token or not repo_owner or not repo_name:
        raise Exception("Missing GitHub configuration. Please check the hardcoded values.")
    
    # Create a GitHub client with the token
    g = Github(token)
    try:
        repo = g.get_repo(f"{repo_owner}/{repo_name}")
    except Exception as e:
        raise Exception(f"Error accessing repository: {str(e)}")
    
    try:
        commit = repo.get_commit(commit_sha)
        status = commit.create_status(
            state=state,           # "pending", "success", or "failure"
            target_url="",         # Optionally, add a URL for build logs
            description=description,
            context=context
        )
        return status.raw_data
    except Exception as e:
        raise Exception(f"Error updating commit status: {str(e)}")

@router.post("/webhook")
async def notify(request: Request):

    try:
        # Parse the incoming JSON payload
        payload = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {str(e)}")
    
    # Extract required data from the payload
    commit_sha = payload.get("commit")
    state = payload.get("status")
    description = payload.get("description", "No description provided")
    
    # Ensure the payload contains required fields
    if not commit_sha or not state:
        raise HTTPException(status_code=400, detail="Payload must include 'commit' and 'status'.")
    
    try:
        # Update the commit status on GitHub
        result = update_commit_status(commit_sha, state, description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating commit status: {str(e)}")
    
    # Return a success response with GitHub's response data
    return {"message": "Notification sent", "result": result}
