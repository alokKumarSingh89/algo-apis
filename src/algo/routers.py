from fastapi import APIRouter, HTTPException
from starlette import status
from src.algo.ThetaGain import execute


# Testing

execute();

algo = APIRouter(
    prefix="/algo",
    tags=["Algo List"])

@algo.get("")
def welcome():
    return {"message":"Running"}


