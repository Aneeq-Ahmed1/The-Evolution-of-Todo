import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now run the backend
if __name__ == "__main__":
    import uvicorn
    from phase_2_web.backend.main import app

    uvicorn.run(app, host="0.0.0.0", port=8000)