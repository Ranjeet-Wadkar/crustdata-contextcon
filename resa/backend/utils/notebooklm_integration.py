import subprocess
import json
import tempfile
import os

def run_cli_command(command_parts, capture_json=True):
    """Run a notebooklm CLI command and return parsed JSON or raw output."""
    try:
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        
        # Use shell=True on windows to ensure the CLI command resolves
        cmd = " ".join(command_parts) if os.name == 'nt' else command_parts
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            check=True,
            shell=(os.name == 'nt'),
            env=env
        )
        
        stdout = result.stdout.strip()
        
        # Sometime CLI prints informational stuff to stderr, so stdout should just be json.
        # But if not json, we return it.
        if capture_json:
            # simple json extracting if CLI polluted it
            start = stdout.find('{')
            end = stdout.rfind('}') + 1
            if start != -1 and end != -1:
                return json.loads(stdout[start:end])
            return json.loads(stdout)
            
        return stdout
    except subprocess.CalledProcessError as e:
        error_msg = f"NotebookLM API Error: {e.stderr}"
        print(error_msg)
        raise Exception(error_msg)

def create_notebooklm_deck(markdown_content: str, status_callback=None):
    """
    Creates a notebook, uploads content, triggers deck generation, waits, and downloads the PPTX.
    """
    if status_callback: status_callback("Creating NotebookLM project...")
    
    # 1. Create notebook
    nb_data = run_cli_command(["notebooklm", "create", '"Hackathon AI Synthesis"', "--json"])
    nb_id = nb_data.get("notebook", {}).get("id") or nb_data.get("id")
    if not nb_id:
        raise Exception(f"Failed to create notebook. Response: {nb_data}")
        
    # 2. Write content to temp file
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode='w', encoding='utf-8') as f:
            f.write(markdown_content)
            temp_path = f.name
            
        if status_callback: status_callback("Uploading synthesis report to Notebook...")
        # 3. Add source
        # we surround path with quotes in case of spaces
        src_data = run_cli_command(["notebooklm", "source", "add", f'"{temp_path}"', "-n", nb_id, "--json"])
        source_id = src_data.get("source", {}).get("id") or src_data.get("source_id") or src_data.get("id")
        
        if status_callback: status_callback("Waiting for Notebook to index source...")
        run_cli_command(["notebooklm", "source", "wait", source_id, "-n", nb_id], capture_json=False)
        
        if status_callback: status_callback("Generating high-quality Slide Deck (this can take 2-10 minutes)...")
        # 4. Generate Deck
        task_data = run_cli_command(["notebooklm", "generate", "slide-deck", "-n", nb_id, "--json"])
        task_id = task_data.get("task", {}).get("id") or task_data.get("task_id") or task_data.get("id")
        
        # Wait for artifact
        run_cli_command(["notebooklm", "artifact", "wait", task_id, "-n", nb_id, "--timeout", "900"], capture_json=False)
        
        if status_callback: status_callback("Downloading PPTX deck...")
        # 5. Download Deck
        out_file = "notebooklm_premium_deck.pptx"
        run_cli_command(["notebooklm", "download", "slide-deck", f'"{out_file}"', "--format", "pptx", "-a", task_id, "-n", nb_id], capture_json=False)
        
        return out_file
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
