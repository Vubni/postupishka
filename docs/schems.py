from marshmallow import Schema, fields

class UserRegisterSchema(Schema):
    email = fields.Str(required=True, description="email пользователя. До 256 символов")
    firstName = fields.Str(required=True)
    _class = fields.Int(required=True)
    password = fields.Str(required=True)

class TokenResponseSchema(Schema):
    token = fields.Str(description="Токен для взаимодействия с аккаунтом")

class UserAuthSchema(Schema):
    identifier = fields.Str(required=True)
    password = fields.Str(required=True)


class SubjectSchema(Schema):
    subject = fields.Str()
    current_score = fields.Float()
    desired_score = fields.Float()

class UserProfileSchema(Schema):
    email = fields.Str()
    first_name = fields.Str()
    class_number = fields.Int()
    subjects = fields.List(fields.Nested(SubjectSchema))
    
    
class UserEditSchema(Schema):
    email = fields.Str(required=False, description="email пользователя. До 256 символов")
    firstName = fields.Str(required=False)
    class_number = fields.Int(required=False)
    password_old = fields.Str(required=False)
    password_new = fields.Str(required=False)
    subjects = fields.List(fields.Nested(SubjectSchema), required=False)
    
    
class Error400Schema(Schema):
    name = fields.Str(description="Имя параметра, не соответствующего требованиям")
    error = fields.Str(description="Не соблюденное требование")
    
class TgUrlSchema(Schema):
    url = fields.Str()
    
class QuestionSchema(Schema):
    question = fields.Str(description="Вопрос от ИИ для пользователя")
    counts_remaind = fields.Int(description="Количество оставшихся вопросов")
    
    

class AnswerAddSchema(Schema):
    answer = fields.Str(required=True, description="Ответ на последний вопрос")
    

class ScoreSchema(Schema):
    min = fields.Int(required=True, description="Минимальный балл на платку")
    avg = fields.Int(required=True, description="Средний балл поступивших")
    bud = fields.Int(required=True, description="Балл для бюджетного места")

class UniversitySchema(Schema):
    university = fields.Str(required=True, description="Название университета")
    directions = fields.List(fields.Str(), required=True, description="Список направлений подготовки")
    scores = fields.Nested(ScoreSchema, required=True, description="Баллы для поступления")
    features = fields.List(fields.Str(), required=True, description="Особенности университета")
    information = fields.Bool(required=True, description="Флаг дополнительной информации")
    
    
    
class AddUniversity(Schema):
    university = fields.Str(required=True, description="Название университета")
    direction = fields.Str(required=False, description="Направление")
    scores = fields.Nested(ScoreSchema, required=True, description="Примерные баллы для поступления")