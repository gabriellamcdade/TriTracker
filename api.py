from fastapi import FastAPI


app = FastAPI(
    title="TriTracker API",
    description="API for TriTracker training data and analysis",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "TriTracker API"
    }