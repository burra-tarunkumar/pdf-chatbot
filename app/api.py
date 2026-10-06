from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def root():
    return {"message": "PDF Chatbot API is running."}