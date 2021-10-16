async def get_data(message: types.Message=None, call: types.CallbackQuery=None, session_id=None, whole_quiz=None, chosen_quiz=None, entity=None, admin_data=admin_data):

    if whole_quiz == 'Yes':
        data_by_session_id = "SELECT * FROM users WHERE session_id = %s"
        cursor.execute(data_by_session_id, (session_id,))

        quiz = {}