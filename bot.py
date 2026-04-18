import discord
from discord.ext import commands
from logic import get_answer, add_qa, add_feedback, get_quiz

bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())

@bot.command()
    """pertanyaan user ke bot"""
    jawaban = get_answer(question):