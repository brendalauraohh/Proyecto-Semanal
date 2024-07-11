import discord
from discord.ext import commands, tasks
import datetime
import asyncio 

#Instancias del bot y se definen intents necesarios
intents= discord.Intents.default()
intents.message_content= True
bot= commands.Bot(command_prefix='!', intents= intents)

#Almacenar los objetivos en un diccionario
user_goals= {}

#Comando para instalar la interacción @bot.command
async def objetivo(ctx):
    today= datetime.datetime.today().weekday()
    user=ctx.author

    if today == 0: #lunes
        await user.send ("¿Cuál es tu objetivo para esta semana?")

        def check (m):
            return m.author== ctx.author and isinstance(m.channel, discord.DMChannel)
        
        try:
            msg= await bot.wait_for('message', check=check, timeout=120.0)
        except asyncio.TimeoutError:
            await user.send ('Se acabó el tiempo para responder')
            return
        
        user_goals=[user.id]={
            'goal': msg.content, 
            'task':[],
            'completed':False,
            'comments': '', 
            'difficulties': ''
        }
         
        await user.send (f "Objetivo'{msg.content}' establecido para esta semana")
        await user.send ("Por favor ingresa las tareas para tu objetivo (una por mensaje). Envía la palabra 'listo' cuando hayas terminado. ")

        while True:
            try: 
                task_msg=await bot.wait_for ('message', check=check, timeout=120.0)
                if task_msg.content.lower()== 'listo':
                    break
                user_goals[user.id]['task'].append({'tareas': task_msg.content, 'completed': False})
            except asyncio.TimeoutError:
                await user.send ('Se acabó el tiempo para responder.')
                break
        if user_goals[user.id]['task']:
            await user.send("Tareas agregadas para tu objetivo semanal")
        else:
            await user.send ("No se agregaron tareas para tu objetivo semanal")
    
    elif today== 4: #viernes
        if user.id in user_goals:
            await user.send("¿Lograste tu  objetivo? Responde con 'sí' o 'no'") 

            try: 
                msg= await bot.wait_for ('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await user.send ('Se acabó el tiempo para responder')
                return
            
            if msg.content.lower== 'si' or 'sí':
                user_goals[user.id]['completed']=True
                await user.send("¡Felicidades!¿Tienes algún comentario sobre tu progreso?")
            else:
                user_goals[user.id]['completed']=False
                await user.send("Lamento escuchar eso. ¿Cuáles fueron las partes que se te complicaron?")
            try: 
                comments=await bot.wait_for('message', check=check, timeout=120.0)
                user_goals[user.id]['comments']=comments.content
                if not user_goals[user.id]['completed']:
                    await user.send("Por favor, describe las dificultades que presentaste.")
                    difficulties=await bot.wait_for ('message', check=check, timeout=120.0)
                    user_goals[user.id]['difficulties']=difficulties.content
                await user.send (' Gracias por tu respuesta. ¡Ten un buen fin de semana!')

            except asyncio.TimeoutError:
                await user.send ("Se acabó el tiempo para responder")

        else:
            await user.send("No tienes un objetivo establecido para esta semana.")
    
    else:
        await user.send ("Este comando solo esta disponible los dias Lunes y Viernes")
