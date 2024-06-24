from aiogram import Bot,Dispatcher,types, executor
import logging
logging.basicConfig(level=logging.INFO)
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import time

API_TOKEN = '7015223960:AAHsWLBVwKrVxGpeAFRvwoV5enn85xklOmI'
bot = Bot(API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


from app import database
from app import buttons
from app import states


# def get_user_plans():
    # user_id = message.from_user.id
    # plans = database.get_plans(user_id)
    # if plans:
    #     text = ''
    #     for i, plan in enumerate(plans):
    #         text += f'{i+1}. {plan[2]}\n'


@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message):
    database.create_db()
    username = message.from_user.username
    user_id = message.from_user.id
    fullname = message.from_user.full_name
    database.add_user(user_id, username, fullname)
    await message.reply("Hi Im planner Bot", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message):
    text = '/start - command to start bot\n/checkmyplans - check your plans\n/saveup - save up money for something\n/help - command help to get all commands of bot'
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['saveup'], state='*')
async def save_up(message: types.Message):
    saved_money_check = database.saved_money(message.from_user.id)
    if saved_money_check is not None:
        await message.answer(f'Your saved money: {saved_money_check[0]}', reply_markup=buttons.save_kb)
    else:
        await message.answer('You have no saved money', reply_markup=buttons.save_kb)

@dp.message_handler(text='Save')
async def save_money_up(message: types.Message):
    await message.answer('Enter amount of money', reply_markup=types.ReplyKeyboardRemove())
    await states.Save_Up.money.set()
@dp.message_handler(state=states.Save_Up.money)
async def save_money_up_state(msg: types.Message, state: FSMContext):
    money = int(msg.text)
    user_id = msg.from_user.id
    database.save_up_add_money(user_id, money)
    await msg.answer('Money saved', reply_markup=buttons.save_kb)
    await state.finish()

@dp.message_handler(text='Check my money')
async def check_my_money(message: types.Message):
    saved_money_check = database.saved_money(message.from_user.id)
    if saved_money_check is not None:
        await message.answer(f'Your saved money: {saved_money_check[0]}', reply_markup=buttons.save_kb)
    else: 
        await message.answer('You have no saved money', reply_markup=buttons.save_kb)



@dp.message_handler(text='Add new plan', state='*')
async def add_new_plan(message: types.Message):
    await message.reply('Write new plan', reply_markup=buttons.main_kb)
    await states.Add_Plan.plan.set()
    # try:
    #     @dp.message_handler()
    #     async def add_plan(message: types.Message):
    #         user_id = message.from_user.id
    #         plan = message.text
    #         database.add_plan(user_id, plan)
    #         await message.reply('Plan added', reply_markup=buttons.main_kb)
    # except:
    #     await message.reply('Plan not added {Error}', reply_markup=buttons.main_kb)

@dp.message_handler(state=states.Add_Plan.plan)
async def add_plan_state(msg: types.Message, state: FSMContext):
    plan = msg.text
    user_id = msg.from_user.id
    database.add_plan(user_id, plan, status=0)
    await msg.answer('Plan added', reply_markup=buttons.main_kb)
    await state.finish()



@dp.message_handler(text='Delete plan', state='*')
async def delete_plan(message: types.Message):
    plans = database.get_plans(message.from_user.id)
    if len(plans) == 0:
        await message.reply('You have no plans', reply_markup=buttons.main_kb)
    else:
        text = ''
        for i, plan in enumerate(plans):
            text += f'{i+1}. {plan[2]}\n'
        await message.answer(text, reply_markup=buttons.main_kb)
        await message.answer('Write plan number', reply_markup=types.ReplyKeyboardRemove())
        await states.Plan_id.pk.set()

@dp.message_handler(state=states.Plan_id.pk)
async def delete_plan_pk(msg: types.Message, state: FSMContext):
    await state.update_data(id=int(msg.text))
    data = await state.get_data()
    id = data.get('id')
    if database.check_plan_id(msg.from_id, id) is not None:
        pk = database.check_plan_id(msg.from_id, id)
        database.delete_plan(pk, msg.from_id)
        await msg.answer("Plan success remove", reply_markup=buttons.main_kb)
    await state.finish()




@dp.message_handler(text='Check my plans', state='*')
async def check_plans(message: types.Message):
    user_id = message.from_user.id
    plans = database.get_plans(user_id)
    if plans:
        text = ''
        for i, plan in enumerate(plans):
            if plan[-1] == 0:
                text += f'{i+1}. {plan[2]} - ❌\n'
            else:
                text += f'{i+1}. {plan[2]} - ✅\n'
        await message.reply(text, reply_markup=buttons.main_kb)
    else:
        await message.reply('You have no plans', reply_markup=buttons.main_kb)
  

@dp.message_handler(text='Edit plan', state='*')
async def edit_plan(message: types.Message):
        # await message.answer('What do you want to change?', reply_markup=buttons.choose_what_to_chage)
        plans = database.get_plans(message.from_user.id)
        if len(plans) == 0:
            await message.reply('You have no plans', reply_markup=buttons.main_kb)
        else:
            text = ''
            for i, plan in enumerate(plans):
                if plan[-1] == 0:
                    text += f'{i+1}. {plan[2]} - ❌\n'
                else:
                    text += f'{i+1}. {plan[2]} - ✅\n'
            await message.answer('Write plan number', reply_markup=types.ReplyKeyboardRemove())
        await states.Edit_Plan.pk.set()


@dp.message_handler(state=states.Edit_Plan.pk)
async def edit_plan_pk(msg: types.Message, state: FSMContext):
    await state.update_data(pk=int(msg.text))
    id = int(msg.text)
    if database.check_plan_id(msg.from_id, id) is not None:
        plan = database.check_plan_id(msg.from_id, id)
        await msg.answer(f'What do you want to change?\n\n{plan[2]}', reply_markup=buttons.choose_what_to_chage)


@dp.message_handler(text='Change text of plan', state='*')
async def change_text_plan(message: types.Message, state: FSMContext):
    data = await state.get_data('id')
    await message.answer('Change ')





# @dp.message_handler(text='Change text of plan')
# async def change_text_plan(message: types.Message):
#     await message.answer('Write plan number', reply_markup=types.ReplyKeyboardRemove())
#     plans = database.get_plans(message.from_user.id)
#     if len(plans) == 0:
#         await message.reply('You have no plans', reply_markup=buttons.main_kb)
#     else:
#         text = ''
#         for i, plan in enumerate(plans):
#             if plan[-1] == 0:
#                 text += f'{i+1}. {plan[2]} - ❌\n'
#             else:
#                 text += f'{i+1}. {plan[2]} - ✅\n'
#         await message.answer(text, reply_markup=buttons.main_kb)
#         await message.answer('Write plan number')
#         await states.Edit_Plan.pk.set()


# @dp.message_handler(state=states.Edit_Plan.pk)
# async def edit_plan_pk(msg: types.Message, state: FSMContext):
#     await state.update_data(pk=int(msg.text))
#     id = int(msg.text)
#     if database.check_plan_id(msg.from_id, id) is not None:
#         pk = database.check_plan_id(msg.from_id, id)
#         data = await state.update_data(pk=pk)
#         await msg.answer('Write new plan')
#         await states.Edit_Plan.edited_plan.set()
#         # await msg.answer("Plan success edit", reply_markup=buttons.main_kb)
#     else:
#         await msg.answer("Plan not found", reply_markup=buttons.main_kb)

# @dp.message_handler(state=states.Edit_Plan.edited_plan)
# async def edit_plan_pk(msg: types.Message, state: FSMContext):
#     await state.update_data(new_plan=msg.text)
#     data = await state.get_data()
#     pk = data.get('pk')
#     # await state.update_data(new_plan=msg.text)
#     data = await state.get_data()
#     pk = data.get('pk')
#     new_plan = msg.text
#     database.edit_plan(msg.from_id, new_plan, pk)
#     await msg.answer("Plan success edited", reply_markup=buttons.main_kb)
#     await state.finish()


# @dp.message_handler(text='Change status of plan')
# async def change_status_plan(message: types.Message):
#     plans = database.get_plans(message.from_user.id)
#     if len(plans) == 0:
#         await message.reply('You have no plans', reply_markup=buttons.main_kb)
#     else:
#         text = ''
#         for i, plan in enumerate(plans):
#             if plan[-1] == 0:
#                 text += f'{i+1}. {plan[2]} - ❌\n'
#             else:
#                 text += f'{i+1}. {plan[2]} - ✅\n'
#         await message.answer(text, reply_markup=buttons.main_kb)
#         await message.answer('Write plan number')
#         await states.Edit_Plan.pk.set()


# @dp.message_handler(state=states.Edit_Plan.pk)

    

    
# @dp.message_handler(text='Change plan')
# async def edit_plan(message: types.Message):
#     await message.answer('Write plan number', reply_markup=types.ReplyKeyboardRemove())
#     await states.Edit_Plan.pk.set()

# @dp.message_handler(state=states.Edit_Plan.pk)
# async def edit_plan_pk(msg: types.Message, state: FSMContext):
#     await state.update_data(pk=int(msg.text))
#     id = int(msg.text)
#     if database.check_plan_id(msg.from_id, id) is not None:
#         pk = database.check_plan_id(msg.from_id, id)
#         data = await state.update_data(pk=pk)
#         await msg.answer('Write new plan')
#         await states.Edit_Plan.edited_plan.set()
#         # await msg.answer("Plan success edit", reply_markup=buttons.main_kb)
#     else:
#         await msg.answer("Plan not found", reply_markup=buttons.main_kb)


# @dp.message_handler(state=states.Edit_Plan.edited_plan)
# async def edit_plan_pk(msg: types.Message, state: FSMContext):
#     await state.update_data(new_plan=msg.text)
#     data = await state.get_data()
#     pk = data.get('pk')
#     # await state.update_data(new_plan=msg.text)
#     data = await state.get_data()
#     pk = data.get('pk')
#     new_plan = msg.text
#     database.edit_plan(msg.from_id, new_plan, pk)
#     await msg.answer("Plan success edited", reply_markup=buttons.main_kb)
#     await state.finish()

# @dp.message_handler(text='Change status')
# async def change_status(message: types.Message):
#     await message.answer('Write plan number', reply_markup=types.ReplyKeyboardRemove())
#     await states.Edit_Plan.pk.set()

# @dp.message_handler(state=states.Edit_Plan.pk)
# async def change_status_pk(msg: types.Message, state: FSMContext):
#     await state.update_data(pk=int(msg.text))
#     id = int(msg.text)
#     if database.check_plan_id(msg.from_id, id) is not None:
#         pk = database.check_plan_id(msg.from_id, id)
#         data = await state.update_data(pk=pk)
#         # await msg.answer(f'Your plan\'s status is {}', reply_markup=buttons.change_plan_status)
#     else:
#         await msg.answer("Plan not found", reply_markup=buttons.main_kb)

# @dp.message_handler(text='Change plan status')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)