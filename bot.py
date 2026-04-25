import discord
from discord.ext import commands
from logic import get_question, add_qa, add_feedback, get_quiz
from config import TOKEN

# Setup Bot
bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
intents = discord.Intents.default()
intents.message_content = True  # ← TAMBAH INI

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} online!')

# user interface tanya jawab
@bot.command(name='ask')
async def ask_question(ctx, *, question):
    jawaban = get_question(question)
    
    embed = discord.Embed(
        title="❓ Pertanyaan",
        description=question,
        color=discord.Color.blue()
    )
    embed.add_field(name="Jawaban", value=jawaban, inline=False)
    embed.set_footer(text=f"Ditanya oleh {ctx.author.name}")
    
    await ctx.send(embed=embed)


# Quiz

@bot.command(name='quiz')
async def quiz_command(ctx):
    """
    Lihat semua soal quiz yang tersedia
    """
    quiz_list = get_quiz()
    
    if not quiz_list:
        await ctx.send("❌ Belum ada soal quiz!")
        return
    
    # Tampilkan soal dalam embed
    embed = discord.Embed(
        title="Daftar soal quiz",
        color=discord.Color.purple()
    )
    
    for idx, soal in enumerate(quiz_list, 1):
        soal_text = f"""
**Soal {idx}:** {soal[1]}

A) {soal[3]}
B) {soal[4]}
C) {soal[5]}

Jawaban Benar: {soal[2]}
"""
        embed.add_field(name=f"Soal {idx}", value=soal_text, inline=False)
    
    await ctx.send(embed=embed)

# help command
@bot.command(name='commands')
async def commands_command(ctx):
    """Daftar command yg bisa dipake"""
    embed = discord.Embed(
        title="Bot Helper Commands",
        color=discord.Color.blue()
    )   
    embed.add_field(
        name=" !tanya [pertanyaan]",
        value="Tanya bot helper tentang sesuatu",
        inline=False
    )   
    embed.add_field(
        name="!addfaq [pertanyaan | jawaban | kategori]",
        value="(Admin Only) Tambah FAQ baru",
        inline=False
    )
    embed.add_field(
        name="⭐ !feedback [rating 1-5] [pesan]",
        value="Berikan feedback tentang bot",
        inline=False
    )
    embed.add_field(
        name="!quiz",
        value="Lihat daftar soal quiz",
        inline=False
    )
    
    await ctx.send(embed=embed)

# FAQ command

@bot.command(name='addfaq')
async def add_faq_command(ctx, *, faq_text):
    """
    Admin: Tambah FAQ baru
    Format: !addfaq pertanyaan | jawaban | kategori
    """
    
    # Cek admin
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Hanya admin yang bisa menambah FAQ!")
        return
    
    # Pisahkan input
    parts = faq_text.split('|')
    
    if len(parts) != 3:
        await ctx.send("❌ Format salah!\nGunakan: `!addfaq pertanyaan | jawaban | kategori`")
        return
    
    question, answer, category = [p.strip() for p in parts]
    
    # Tambah ke database
    add_qa(question, answer, category)
    
    embed = discord.Embed(
        title="✅ FAQ Ditambahkan",
        color=discord.Color.green()
    )
    embed.add_field(name="Pertanyaan", value=question, inline=False)
    embed.add_field(name="Jawaban", value=answer, inline=False)
    embed.add_field(name="Kategori", value=category, inline=False)
    
    await ctx.send(embed=embed)

#feedback commmand

@bot.command(name='feedback')
async def give_feedback(ctx, rating: int, *, message):
    """
    Berikan feedback tentang bot
    Format: !feedback [rating 1-5] [pesan]
    """
    
    # Validasi rating
    if rating < 1 or rating > 5:
        await ctx.send("❌ Rating harus antara 1-5!")
        return
    
    # Simpan feedback
    add_feedback(ctx.author.name, message, rating)
    
    # Tampilkan konfirmasi
    stars = "⭐" * rating
    embed = discord.Embed(
        title="✅ Feedback Diterima",
        color=discord.Color.gold()
    )
    embed.add_field(name="Rating", value=stars, inline=False)
    embed.add_field(name="Pesan", value=message, inline=False)
    
    await ctx.send(embed=embed)
# Ganti dengan token bot Anda
bot.run(TOKEN)