from send import job

CHAT_ID = -1002312034777

job(CHAT_ID=CHAT_ID, text_gen=True, image_gen=True, problem=True, offset=1)
job(CHAT_ID=CHAT_ID, text_gen=True, image_gen=True, problem=False, offset=1)
