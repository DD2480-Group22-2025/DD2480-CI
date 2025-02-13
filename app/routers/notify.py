import os
import shutil
import subprocess
import sys
from dotenv import load_dotenv
from fastapi import APIRouter, Request, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

sys.path.append('app/lib')
from util import clone_repo, update_commit_status, delete_repo

# Load environment variables from a .env file, if present
load_dotenv()

router = APIRouter()

class WebhookPayload(BaseModel):
    ref: str
    repository: Dict[str, Any]
    head_commit: Dict[str, Any]
    before: str | None = None
    after: str | None = None
    created: bool | None = None
    deleted: bool | None = None
    forced: bool | None = None
    base_ref: str | None = None
    compare: str | None = None
    commits: list[Dict[str, Any]] | None = None
    pusher: Dict[str, Any] | None = None
    sender: Dict[str, Any] | None = None
    organization: Dict[str, Any] | None = None

def run_test_file(repo_path: str, test_file: str) -> Dict[str, Any]:
    """Run a specific test file and return the results"""
    try:
        # Get just the filename without the tests/ prefix
        test_filename = os.path.basename(test_file)
        test_path = os.path.join("tests", test_filename)
        abs_test_path = os.path.join(repo_path, test_path)
        
        print(f"\nDEBUG: Testing file {test_file}")
        print(f"DEBUG: Absolute test path: {abs_test_path}")
        
        if not os.path.exists(abs_test_path):
            print(f"DEBUG: Test file not found at {abs_test_path}")
            return {
                "success": False,
                "output": "",
                "error": f"Test file not found: {test_path}"
            }

        # First verify pytest is available in the environment
        try:
            pytest_version = subprocess.run(['python3', '-m', 'pytest', '--version'], 
                         capture_output=True, 
                         text=True,
                         check=True)
            print(f"DEBUG: pytest version: {pytest_version.stdout}")
        except subprocess.CalledProcessError:
            print("DEBUG: pytest is not available in the environment")
            return {
                "success": False,
                "output": "",
                "error": "pytest is not available in the environment"
            }

        print(f"DEBUG: Running pytest from directory: {repo_path}")
        # Run the test from the repo root to ensure proper import paths
        result = subprocess.run(
            ['python3', '-m', 'pytest', test_path, '-v'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"DEBUG: Test return code: {result.returncode}")
        print(f"DEBUG: Test stdout: {result.stdout}")
        print(f"DEBUG: Test stderr: {result.stderr}")
        
        # Check if the test actually ran or if it was collected but not run
        if "no tests ran" in result.stdout.lower():
            return {
                "success": False,
                "output": result.stdout,
                "error": "No tests were actually executed"
            }
        
        # Check for test failures vs execution failures
        if result.returncode != 0:
            if "FAILURES" in result.stdout:
                # This is a legitimate test failure, which should be reported as such
                return {
                    "success": False,
                    "output": result.stdout,
                    "error": "Tests failed"
                }
            else:
                # This is an execution error
                return {
                    "success": False,
                    "output": result.stdout,
                    "error": f"Test execution error: {result.stderr}"
                }
            
        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr
        }
    except subprocess.TimeoutExpired:
        print("DEBUG: Test execution timed out after 30 seconds")
        return {
            "success": False,
            "output": "",
            "error": "Test execution timed out after 30 seconds"
        }
    except Exception as e:
        print(f"DEBUG: Unexpected error running tests: {str(e)}")
        return {
            "success": False,
            "output": "",
            "error": f"Error running tests: {str(e)}"
        }

def ensure_clean_clone_dir(repo_dir_name: str) -> None:
    """Ensure the clone directory is clean before cloning"""
    clone_path = os.path.join("./cloned_repo", repo_dir_name)
    if os.path.exists(clone_path):
        try:
            shutil.rmtree(clone_path)
        except Exception as e:
            print(f"Warning: Failed to clean up existing directory: {str(e)}")

@router.post("/webhook")
async def notify(payload: WebhookPayload):
    repo_dir_name = None
    try:
        repo_url = payload.repository["clone_url"]
        identifier = payload.repository["pushed_at"]
        branch = payload.ref.replace("refs/heads/", "")
        owner, name = payload.repository["full_name"].split("/")
        os.environ["REPO_OWNER"] = owner
        os.environ["REPO_NAME"] = name
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing payload: {str(e)}")

    print(f"Push event to {repo_url} on branch {branch}")
    commit_sha = payload.head_commit["id"]

    test_contexts = ["CI/test_syntax", "CI/test_notifier", "CI/test_CI"]
    # Initial status set to pending
    for context in test_contexts:
        try:

            update_commit_status(commit_sha, "pending", "Setting up CI environment", context)
        except Exception as e:
            print(f"Failed to set initial status for {context}: {str(e)}")

    repo_dir_name = repo_url.split("/")[-1].split(".")[0] + "-" + str(identifier)
    ensure_clean_clone_dir(repo_dir_name)

    print("Attempting to clone repo... with branch: ", branch)
    clone_success = clone_repo(repo_url, identifier, branch)
    if not clone_success:
        error_msg = "Repository clone failed"
        for context in test_contexts:
            try:
                update_commit_status(commit_sha, "error", error_msg, context)
            except Exception as e:
                print(f"Failed to update clone failure status: {str(e)}")
        return {"message": error_msg, "status": "error"}

    print("Repo cloned successfully!")
    repo_path = f"./cloned_repo/{repo_dir_name}"
    
    result = {
        "status": "ok",
        "steps": {
            "test_syntax": {"status": "pending", "description": "Not started"},
            "test_notifier": {"status": "pending", "description": "Not started"},
            "test_CI": {"status": "pending", "description": "Not started"}
        }
    }

    test_files = [
        ("test_syntax", "tests/test_syntax.py"),
        ("test_notifier", "tests/test_notifier.py"),
        ("test_CI", "tests/test_CI.py")
    ]

    try:
        for test_name, test_file in test_files:
            print(f"\n=== Starting {test_name} ===")
            
            try:
                test_results = run_test_file(repo_path, test_file)
                status = "success" if test_results["success"] else "failure"
                description = (f"{test_name} passed" if test_results["success"] 
                             else f"{test_name} failed: {test_results.get('error', '')[:140]}")
                
                print(f"DEBUG: {test_name} results:")
                print(f"DEBUG: Status: {status}")
                print(f"DEBUG: Description: {description}")
                
                update_commit_status(commit_sha, status, description, f"CI/{test_name}")
                
                result["steps"][test_name] = {
                    "status": status,
                    "description": description,
                    "output": test_results.get("output", ""),
                    "error": test_results.get("error", "")
                }
            except Exception as e:
                error_msg = f"Test execution error: {str(e)}"
                print(f"DEBUG: Error in {test_name}: {error_msg}")
                update_commit_status(commit_sha, "error", error_msg, f"CI/{test_name}")
                result["steps"][test_name] = {
                    "status": "error",
                    "description": error_msg
                }

    except Exception as e:
        error_msg = f"CI process error: {str(e)}"
        print(error_msg)
        # Update any remaining pending statuses to error
        for step_name in result["steps"]:
            if result["steps"][step_name]["status"] == "pending":
                update_commit_status(commit_sha, "error", error_msg, f"CI/{step_name}")
                result["steps"][step_name] = {
                    "status": "error",
                    "description": error_msg
                }
    finally:
        if repo_dir_name:
            delete_repo(repo_dir_name)

    return result

