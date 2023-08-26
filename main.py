from fastapi import FastAPI


app = FastAPI()

@app.get("/get")
def root():
    return "hello world"