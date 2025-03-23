from fastApi import FastAPI, HTTPEexception, Depends
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()