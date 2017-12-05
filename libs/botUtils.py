from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def createMarkup(keys):
    buttons = []
    for row in keys:
        rbuttons = []
        for k in row:
            callback = 'ignore' if len(k) == 1 else k[1]
            rbuttons.append(InlineKeyboardButton(text = k[0], callback_data = callback))
        buttons.append(rbuttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
