from typing import Dict
from pydantic import BaseModel
from pydantic.typing import(List, Dict)


class Client(BaseModel):
    list_ans: List[Dict[str,str]] = None
