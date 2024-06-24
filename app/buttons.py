from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b1 = KeyboardButton('Check my plans')
b2 = KeyboardButton('Add new plan')
b3 = KeyboardButton('Delete plan')
b4 = KeyboardButton('Edit plan')

main_kb.add(b1, b2, b3, b4)


save_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

b5 = KeyboardButton('Check my money')
b6 = KeyboardButton('Save')

save_kb.add(b5, b6)


change_plan_status = ReplyKeyboardMarkup(row_width=2)

b7 = KeyboardButton(text='✅')
b8 = KeyboardButton(text='❌')

change_plan_status.add(b7, b8)


choose_what_to_chage = ReplyKeyboardMarkup(row_width=2)

b9 = KeyboardButton(text='Change text of plan')
b10 = KeyboardButton(text='Change status of plan')

choose_what_to_chage.add(b9, b10)
