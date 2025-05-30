from marshmallow import Schema, fields

class UserRegisterSchema(Schema):
    email = fields.Str(required=True, description="email пользователя. До 256 символов")
    first_name = fields.Str(required=True)
    class_number = fields.Int(required=True)
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
    verified = fields.Bool(description="Верифицирован ли аккаунт")
    
    
class UserEditSchema(Schema):
    email = fields.Str(required=False, description="email пользователя. До 256 символов")
    first_name = fields.Str(required=False)
    class_number = fields.Int(required=False)
    password_old = fields.Str(required=False)
    password_new = fields.Str(required=False)
    subjects = fields.List(fields.Nested(SubjectSchema), required=False)
    
    
class ErrorDetailSchema(Schema):
    """Схема для детального описания одной ошибки."""
    name = fields.Str(description="Имя параметра, вызвавшего ошибку")
    type = fields.Str(description="Тип ошибки (например, missing)")
    message = fields.Str(description="Сообщение об ошибке")
    value = fields.Raw(description="Значение параметра, если оно было передано", allow_none=True)

class Error400Schema(Schema):
    """Основная схема ответа с ошибками."""
    error = fields.Str(description="Общее сообщение об ошибке")
    errors = fields.List(fields.Nested(ErrorDetailSchema), description="Список детальных ошибок")
    received_params = fields.Dict(description="Параметры, которые были успешно получены")
    
class TgUrlSchema(Schema):
    url = fields.Str()
    
class QuestionSchema(Schema):
    question = fields.Str(description="Вопрос от ИИ для пользователя")
    counts_remaind = fields.Int(description="Количество оставшихся вопросов")
    
class QuestionSchema_Psycho(Schema):
    question = fields.Str(description="Вопрос к психологу")

class AnswerAddSchema(Schema):
    answer = fields.Str(required=True, description="Ответ на последний вопрос")
    

class ScoreSchema(Schema):
    min = fields.Int(required=True, description="Минимальный балл на платку")
    avg = fields.Int(required=True, description="Средний балл поступивших")
    bud = fields.Int(required=True, description="Балл для бюджетного места")
    
class University2Schema(Schema):
    university = fields.Str(required=True, description="Название университета")
    directions = fields.List(fields.Str(), required=True, description="Список направлений подготовки")
    scores = fields.Nested(ScoreSchema, required=True, description="Баллы для поступления")
    features = fields.List(fields.Str(), required=True, description="Особенности университета")
    information = fields.Bool(required=True, description="Флаг дополнительной информации")
    
class UniversitySchema(Schema):
    status = fields.Str("done", description="Статус обработки")
    result = fields.List(fields.Nested(University2Schema))
    
class University_load(Schema):
    status = fields.Str("processing")
    
    
    
class AddUniversity(Schema):
    university = fields.Str(required=True, description="Название университета")
    direction = fields.Str(required=False, description="Направление")
    scores = fields.Nested(ScoreSchema, required=True, description="Примерные баллы для поступления")
    
class GetUniversity(Schema):
    university = fields.Str(description="Название университета")
    direction = fields.Str(description="Направление подготовки")
    scores = fields.Nested(ScoreSchema, description="Баллы для поступления")
    
class AddSchedule(Schema):
    content = fields.Str(required=True, description="Информация от человека про его расписание")
    
class CreateScheduleError(Schema):
    error = fields.Str(description="Причина невозможности добавления в расписание")
    
class DayScheduleItemSchema(Schema):
    time_start = fields.Time(required=True, description="Время начала занятия (в формате HH:MM)")
    time_stop = fields.Time(required=True, description="Время окончания занятия (в формате HH:MM)")
    name = fields.Str(required=True, description="Название занятия")
    description = fields.Str(required=True, description="Описание занятия")
    
class DayInfoSchema(Schema):
    day_in_month = fields.Int(required=True, description="День месяца")
    schedule = fields.List(fields.Nested(DayScheduleItemSchema), required=True, description="Расписание на день")
    
class WeekScheduleSchema(Schema):
    week = fields.Str(required=True, description="Номер недели или дата начала недели")
    info = fields.List(fields.Nested(DayInfoSchema), required=True, description="Информация о днях недели")
    
class GetSchedule(Schema):
    data = fields.List(fields.Nested(WeekScheduleSchema), required=True, description="Список расписаний по неделям")
    
class AiDialog(Schema):
    role = fields.Str(required=True, description="Собеседник (user - пользователь, assistant - искусственный интеллект)")
    content = fields.Str(required=True, description="Содержимое сообщения")
    
class Specialization_timer(Schema):
    days = fields.Int(description="дни до завершения таймера")
    hours = fields.Int(description="часы")
    minutes = fields.Int(description="минуты")
    
class AlreadyBeenTaken(Schema):
    name = fields.Str(description="Название переменной, которая занята")
    error = fields.Str(description="Описание, что переменная занята")