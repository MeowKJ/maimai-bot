def get_raw_message(message):
    print(message)
    return message.split(">")[1] if ">" in message else message
