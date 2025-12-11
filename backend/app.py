from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, autocorrect, generate, edit

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(autocorrect.router)
app.include_router(generate.router)
app.include_router(edit.router)

