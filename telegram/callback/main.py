from json import load, dumps
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from html import escape
from telegram.FSM import fsm
from aiogram.fsm.context import FSMContext
from aiogram import types
from telegram import botstates
from create_bot import bot
from ai.yandex_ai import Psychologist, Analyzer

router = Router()


@router.callback_query(lambda call: call.data == "subscription")
async def process_subjects(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer("Сегодня в честь ЭКСПО - подписка бесплатная и её нельзя продлить. Всё ради вас💘", True)

@router.callback_query(lambda call: call.data == "edit_subjects")
async def process_subjects(callback_query: types.CallbackQuery, state: FSMContext):
    functions.delete_subjects(callback_query.from_user.id)
    await callback_query.message.edit_text("Привет! Я — твой помощник в выборе вуза и подготовке к экзаменам. Давай начнём с короткой анкеты, чтобы я понял, как тебе помочь! 🎓\n\n Какие предметы ты сдаёшь? Когда выберешь, нажми 'Я выбрал'", reply_markup=keyboards.create_subjects())
    await state.set_state(botstates.RegistrationStates.waiting_for_subjects)