from app.api.endpoints import app
import uvicorn


uvicorn.run(app, host="0.0.0.0", port=80)
