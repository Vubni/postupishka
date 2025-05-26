from typing import Callable, Optional, TypeVar, Awaitable, Dict, Any
from functools import wraps
from pydantic import BaseModel, ValidationError
import json
from aiohttp import web
from pydantic import field_validator, model_validator
import core

T = TypeVar("T", bound=BaseModel)

def validate(model: type[T]) -> Callable:
    def decorator(handler: Callable[[web.Request, Any], Awaitable[web.Response]]):
        @wraps(handler)
        async def wrapper(request: web.Request) -> web.Response:
            try:
                data = await request.json()
            except json.JSONDecodeError:
                data = {}

            all_data = dict(request.query)
            all_data.update(data)

            try:
                parsed = model(**all_data)
            except ValidationError as e:
                errors = []
                for error in e.errors():
                    err = {
                        "name": error["loc"][-1],
                        "type": error["type"],
                        "message": error["msg"],
                        "value": all_data.get(error["loc"][-1]),
                    }
                    errors.append(err)

                return web.json_response({
                    "error": "Validation failed",
                    "errors": errors,
                    "received_params": all_data,
                }, status=400)

            return await handler(request, parsed)
        return wrapper
    return decorator



class Register(BaseModel):
    email: str
    class_number: int
    first_name : str
    password : str
    
    @field_validator('email')
    def check_email(cls, v):
        if len(v) > 256:
            raise ValueError('Email cannot exceed 256 characters')
        if not core.is_valid_email(v):
            raise ValueError('Email does not comply with email standards or dns mail servers are not found')
        return v
    
    @field_validator('class_number')
    def check_class_number(cls, v):
        if not (9 <= v <= 11):
            raise ValueError('Class_number must be between 9 and 11')
        return v
    
class Auth(BaseModel):
    identifier: str
    password : str
    
    @field_validator('identifier')
    def check_identifier(cls, v):
        if len(v) > 256:
            raise ValueError('Identifier cannot exceed 256 characters')
        return v
    
class Profile_patch(BaseModel):
    email: Optional[str] = None
    first_name : Optional[str] = None
    password_old : Optional[str] = None
    password_new : Optional[str] = None
    class_number : Optional[int] = None
    subjects : Optional[list[dict]] = None
    
    @field_validator('class_number')
    def check_class_number(cls, v):
        if not (9 <= v <= 11):
            raise ValueError('Class_number must be between 9 and 11')
        return v
    
    @field_validator('email')
    def check_email(cls, v):
        if len(v) > 256:
            raise ValueError('Email cannot exceed 256 characters')
        if not core.is_valid_email(v):
            raise ValueError('Email does not comply with email standards or dns mail servers are not found')
        return v
    
    @model_validator(mode='after')
    def check_others(self):
        if self.password_new is not None and self.password_old is None:
            raise ValueError('password_old is required if password_new is provided')
        if self.password_old is not None and self.password_new is None:
            raise ValueError('password_new is required if password_old is provided')
        if all(value is None for value in self.model_dump().values()):
            raise ValueError('At least one field must be provided')
        return self
    
class Psych_question(BaseModel):
    question: str
    
class Schedule_add(BaseModel):
    content: str
    
class Spec_answer(BaseModel):
    answer: str
    
class Univer_add(BaseModel):
    university: str
    direction: str
    scores: dict
    
    @field_validator('scores')
    def check_scores(cls, v):
        if "min" not in v or "avg" not in v or "bud" not in v:
            raise ValueError('Scores must contain min, avg, bud')
        return v