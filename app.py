from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Dummy Loan API", version="1.0.0")


class LoanRequest(BaseModel):
    credit_score: int = Field(ge=300, le=850)
    debt_to_income: float = Field(ge=0, le=1)


@app.get("/")
def root():
    return {"message": "Dummy Loan API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(request: LoanRequest):
    if request.credit_score < 600 or request.debt_to_income > 0.45:
        risk = "high"
    elif request.credit_score >= 700 and request.debt_to_income <= 0.30:
        risk = "low"
    else:
        risk = "medium"
    return {"risk": risk, "model": "dummy-rules-v1"}
