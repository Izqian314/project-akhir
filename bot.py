import discord
from discord.ext import commands
from logic import get_question, add_qa, add_feedback, get_quiz
from config import TOKEN
from logic import add_quiz_score, get_quiz_by_id, check_quiz_answer
import random
# Setup Bot
intents = discord.Intents.default()
intents.message_content = True  # ← TAMBAH INI

bot = commands.Bot(command_prefix='!', intents=intents)
user_quiz_progress = {}

@bot.event
async def on_ready():
    print(f'Bot {bot.user} online!')

# user interface tanya jawab
@bot.command(name='ask')
async def ask_question(ctx, *, question):
    jawaban = get_question(question)
    
    embed = discord.Embed(
        title="Pertanyaan",
        description=question,
        color=discord.Color.blue()
    )
    embed.add_field(name="Jawaban", value=jawaban, inline=False)
    embed.set_footer(text=f"Ditanya oleh {ctx.author.name}")
    
    await ctx.send(embed=embed)


# Quiz

@bot.command(name='quiz')
async def quiz_command(ctx):
    quiz_list = get_quiz()
    
    if not quiz_list:
        await ctx.send("Soal Quiz tidak ada!")
        return
    
    # acak soal
    random.shuffle(quiz_list)

    # Tampilkan soal dalam embed
    user_quiz_progress[ctx.author.id] = {
        'quiz_list': quiz_list,
        'current_index': 0,
        'score': 0
    }
    
    soal = quiz_list[0]
    soal_text = f"""
**Soal 1 dari {len(quiz_list)}:** {soal[1]}

A) {soal[3]}
B) {soal[4]}
C) {soal[5]}

Ketik `!answer A` atau `!answer B` atau `!answer C` untuk menjawab
"""
    embed = discord.Embed(
        title="🎯 Quiz Dimulai!",
        description=soal_text,
        color=discord.Color.blue()
    )
    
    await ctx.send(embed=embed)


# command jawab soal quiz
@bot.command(name='answer')
async def answer_quiz(ctx, *, answer_text):
    user_id = ctx.author.id

    if user_id not in user_quiz_progress:
        await ctx.send("mulai quiz dengan !quiz")
        return
    
    progress = user_quiz_progress[user_id]
    current_index = progress["current_index"]
    quiz_list = progress['quiz_list']
    
    #cek apakah quiz sudah selesai
    if progress['current_index'] >= len(quiz_list):
        await ctx.send("Quiz selesai.")
        return

    # Get soal saat ini
    soal = quiz_list[current_index]
    correct_answer = soal[2]
    
    # Validate answer
    valid_answers = ['A', 'B', 'C']
    answer_upper = answer_text.strip().upper()
    
    if answer_upper not in valid_answers:
        await ctx.send("❌ Jawaban harus A, B, atau C!")
        return
    
    # Mapping jawaban
    answer_map = {
        'A': soal[3],
        'B': soal[4],
        'C': soal[5]
    }
    
    user_answer = answer_map[answer_upper]
    
    # Check jawaban
    is_correct = user_answer.lower().strip() == correct_answer.lower().strip()
    
    if is_correct:
        progress['score'] += 1
        result_text = "✅ **BENAR!**"
        color = discord.Color.green()
    else:
        result_text = f"❌ **SALAH!** Jawaban benar: {correct_answer}"
        color = discord.Color.red()
    
    embed = discord.Embed(
        title="📊 Hasil Jawaban",
        description=result_text,
        color=color
    )
    
    # Check apakah ada soal berikutnya
    if current_index + 1 < len(quiz_list):
        # Tampilkan soal berikutnya
        progress['current_index'] += 1
        next_soal = quiz_list[progress["current_index"]]
        soal_number = progress["current_index"] + 1
        
        soal_text = f"""
**Soal {soal_number} dari {len(quiz_list)}:** {next_soal[1]}

A) {next_soal[3]}
B) {next_soal[4]}
C) {next_soal[5]}

Ketik `!answer A` atau `!answer B` atau `!answer C` untuk menjawab
"""
        
        embed.add_field(name="Soal Berikutnya", value=soal_text, inline=False)
        embed.set_footer(text=f"Score: {progress['score']}/{soal_number - 0}")
    else:
        # Quiz selesai
        total_score = progress['score']
        total_soal = len(quiz_list)
        percentage = (total_score / total_soal) * 100
        
        embed.add_field(
            name="🏆 Quiz Selesai!",
            value=f"Score: {total_score}/{total_soal} ({percentage:.1f}%)",
            inline=False
        )
        
        # Simpan score
        add_quiz_score(ctx.author.name, total_score)
        
        # Hapus progress user
        del user_quiz_progress[user_id]
    
    await ctx.send(embed=embed)

    pass

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

