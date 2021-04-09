
from tortoise import Tortoise, run_async 
from django.conf import settings
from .tortoise_models import ChatMessage

async def chat_save_message(username, room_id, message):

    """ function to store chat message in sqlite """

    await Tortoise.init(**settings.TORTOISE_INIT)
    await Tortoise.generate_schemas()

    await ChatMessage.create(room_id=room_id,  
                            username=username,
                            message=message
                       )
    
    await Tortoise.close_connections()



async def chat_delete_message(id):
    await Tortoise.init(**settings.TORTOISE_INIT)
    delete_message = await ChatMessage.filter(id=int(id)).delete()
    # chat_message = await ChatMessage.filter(room_id=1).order_by('date_created').values()
    await Tortoise.close_connections()