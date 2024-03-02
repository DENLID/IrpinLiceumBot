from aiogram.filters.callback_data import CallbackData

class MsCallback(CallbackData, prefix="ms"):
    action: str
    class_letter: str
    class_number: int
    class_student: int
    present_students: int
    ms_number_hv: int
    ms_students: str