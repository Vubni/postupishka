from typing import Callable, Optional, TypeVar, Awaitable, Dict, Any
from functools import wraps
from pydantic import BaseModel, ValidationError
import json
from aiohttp import web
from pydantic import field_validator, model_validator
import core

T = TypeVar("T", bound=BaseModel)

class EmailError(Exception):
    def __init__(self, message="Ошибка проверки email", errors=None):
        self.message = message
        self.errors = errors or []  # Добавляем атрибут errors
        super().__init__(self.message)

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
                errors = [
                    {
                        "name": error["loc"][-1] if error["loc"] else "general",  # Проверяем, есть ли элементы в loc
                        "type": error["type"],
                        "message": error["msg"],
                        "value": all_data.get(error["loc"][-1] if error["loc"] else None),  # Аналогично проверяем loc
                    }
                    for error in e.errors()
                ]
                return web.json_response({
                    "error": "Validation failed",
                    "errors": errors,
                    "received_params": all_data,
                }, status=400)
            except EmailError as e:
                errors = [
                    {
                        "name": "email",
                        "type": "email_validation",
                        "message": e.message,
                        "value": all_data.get("email"),
                    }
                ]
                return web.json_response({
                    "error": "Email validation failed",
                    "errors": errors,
                    "received_params": all_data,
                }, status=422)

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
            raise EmailError('Email does not comply with email standards or dns mail servers are not found')
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
            raise EmailError('Email does not comply with email standards or dns mail servers are not found')
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
    
    @field_validator('question')
    def check_email(cls, v):
        if not v:
            raise ValueError('Qestion field cannot be empty')
        if len(v) > 120:
            raise ValueError("Question is longer than 120")
        return v
    
class Schedule_add(BaseModel):
    content: str
    
    @field_validator('content')
    def check_email(cls, v):
        if not v:
            raise ValueError('Content field cannot be empty')
        if len(v) > 240:
            raise ValueError("Content is longer than 240")
        return v
    
class Spec_answer(BaseModel):
    answer: str
    
    @field_validator('answer')
    def check_email(cls, v):
        if not v:
            raise ValueError('Answer field cannot be empty')
        if len(v) > 240:
            raise ValueError("Answer is longer than 240")
        return v
    
class Univer_add(BaseModel):
    university: str
    direction: str
    scores: dict
    
    @field_validator('scores')
    def check_scores(cls, v):
        if "min" not in v or "avg" not in v or "bud" not in v:
            raise ValueError('Scores must contain min, avg, bud')
        if not (isinstance(v["min"], int) and isinstance(v["avg"], int) and isinstance(v["bud"], int)):
            raise ValueError('Scores min, avg, bud is not int')
        if v["min"] < 0 or v["avg"] < 0 or v["bud"] < 0:
            raise ValueError('Scores min or avg or bud < 0')
        return v