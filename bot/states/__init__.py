from .registration import RegistrationState
from aiogram.fsm.state import State, StatesGroup

# Состояние для ввода причины отказа
class FailReasonState(StatesGroup):
    waiting_for_custom_reason = State()

__all__ = ["RegistrationState", "FailReasonState"]