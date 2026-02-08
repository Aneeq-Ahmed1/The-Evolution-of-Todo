import subprocess
import sys

# Start the server in a subprocess and capture output
cmd = [
    sys.executable, "-m", "uvicorn", 
    "main:app", 
    "--host", "127.0.0.1", 
    "--port", "8000", 
    "--reload"
]

print("Starting server...")
process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    universal_newlines=True,
    cwd=r"E:\Aneeq-AI\New folder\The Evolution of Todo(working)\phase_3_Aichatbot\backend"
)

# Wait a few seconds
import time
time.sleep(5)

# Check if the process is still running
if process.poll() is not None:
    # Process has terminated, get the output
    stdout, stderr = process.communicate()
    print("Server terminated early!")
    print("STDOUT:", stdout)
    print("STDERR:", stderr)
else:
    print("Server is running, PID:", process.pid)
    # Terminate the process
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()