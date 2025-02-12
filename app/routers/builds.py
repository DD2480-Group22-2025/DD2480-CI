from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.lib.database_api import get_entries, get_entry_by_id

router = APIRouter()

def error_page(message: str) -> str:
    return f"""
    <html>
        <head>
            <title>Error</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 40px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                .error-box {{
                    background-color: #ffebee;
                    border: 1px solid #ffcdd2;
                    border-radius: 5px;
                    padding: 20px;
                    margin: 20px;
                    max-width: 600px;
                }}
                .back-link {{
                    margin-top: 20px;
                }}
                .back-link a {{
                    color: #0066cc;
                    text-decoration: none;
                }}
                .back-link a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="error-box">
                <h2>Error</h2>
                <p>{message}</p>
            </div>
            <div class="back-link">
                <a href="/builds">← Back to Build List</a>
            </div>
        </body>
    </html>
    """

@router.get("/builds", response_class=HTMLResponse)
async def get_builds():
    builds = get_entries()
    
    if isinstance(builds, dict) and "error" in builds:
        return HTMLResponse(content=error_page(builds["error"]), status_code=500)
    
    if not builds:
        return HTMLResponse(content=error_page("No builds found in the database."), status_code=404)
    
    html_content = """
    <html>
        <head>
            <title>CI Build History</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .build-list { list-style: none; padding: 0; }
                .build-item { 
                    margin: 10px 0;
                    padding: 15px;
                    background-color: #f5f5f5;
                    border-radius: 5px;
                }
                .build-item a {
                    color: #0066cc;
                    text-decoration: none;
                }
                .build-item a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>CI Build History</h1>
            <ul class="build-list">
    """
    
    for build in builds:
        build_id = build[0]
        commit_hash = build[1]
        date = build[2]
        html_content += f"""
                <li class="build-item">
                    <a href="/builds/{build_id}">
                        Build #{build_id} - Commit: {commit_hash} - Date: {date}
                    </a>
                </li>
        """
    
    html_content += """
            </ul>
        </body>
    </html>
    """
    return html_content

@router.get("/builds/{build_id}", response_class=HTMLResponse)
async def get_build(build_id: str):
    try:
        build_id_int = int(build_id)
    except ValueError:
        return HTMLResponse(
            content=error_page("Invalid build ID format. Must be a number."),
            status_code=400
        )
    
    build = get_entry_by_id(build_id_int)
    
    if isinstance(build, dict) and "error" in build:
        return HTMLResponse(content=error_page(build["error"]), status_code=500)
    
    if not build or len(build) == 0:
        return HTMLResponse(
            content=error_page(f"Build #{build_id} not found."),
            status_code=404
        )
    
    build = build[0]
    commit_hash = build[1]
    date = build[2]
    test_result = build[3]
    lint_result = build[4]
    
    html_content = f"""
    <html>
        <head>
            <title>Build #{build_id} Details</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .back-link {{ margin-bottom: 20px; }}
                .back-link a {{ color: #0066cc; text-decoration: none; }}
                .back-link a:hover {{ text-decoration: underline; }}
                .build-details {{ 
                    background-color: #f5f5f5;
                    padding: 20px;
                    border-radius: 5px;
                }}
                .build-log {{
                    background-color: #2b2b2b;
                    color: #ffffff;
                    padding: 15px;
                    border-radius: 5px;
                    white-space: pre-wrap;
                    font-family: monospace;
                }}
            </style>
        </head>
        <body>
            <div class="back-link">
                <a href="/builds">← Back to Build List</a>
            </div>
            <div class="build-details">
                <h1>Build #{build_id}</h1>
                <p><strong>Commit Hash:</strong> {commit_hash}</p>
                <p><strong>Build Date:</strong> {date}</p>
                <h2>Test-log Log:</h2>
                <div class="Test-log">
                    {test_result}
                </div>
                <h2>Linter-log:</h2>
                <div class="Linter-log">
                    {lint_result}
                </div>
            </div>
        </body>
    </html>
    """
    return html_content

