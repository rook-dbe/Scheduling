from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from google.protobuf import text_format
from ortools.sat.python import cp_model
from typing import List, Tuple
from scheduling import solve_shift_scheduling

class RequestData(BaseModel):
  num_employees: int
  num_weeks: Optional[int] = 3
  shifts: Optional[List[str]] = ["O", "M", "A", "N"]
  fixed_assignments: Optional[List[int]] = []
  requests: Optional[List[Tuple[int, int, int, int]]] = []
  shift_constraints: Optional[List[Tuple[int, int, int, int, int, int, int]]] = None
  weekly_sum_constraints: Optional[List[Tuple[int, int, int, int, int, int, int]]] = None
  penalized_transitions: Optional[List[Tuple[int, int, int]]] = None
  weekly_cover_demands: Optional[List[Tuple[int, int, int]]] = None
  excess_cover_penalties: Optional[Tuple[int, int, int]] = None

class ResponseData(BaseModel):
  status: int
  result: List[int]
  inputs: str
  penalties: str
  response_stats: str

app = FastAPI()

@app.post("/scheduling", status_code=201,response_model=ResponseData)
async def scheduling(data:RequestData):
    data_dict = data.dict()
    ans = solve_shift_scheduling(data_dict)
    return ans

lambda_handler = Mangum(app)
