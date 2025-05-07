from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    waiting_for_subjects = State()
    waiting_for_fears = State()

class MainMenuStates(StatesGroup):
    main = State()
    psycho = State()
    tests = State()
    daily_help = State()

class Choice(StatesGroup):
    q = State()
    AskAI = State()

class Tests(StatesGroup):
    rus_orfoepia = State()

class Wait(StatesGroup):
    wait_generation = State()