import discord
from discord.ext import commands
import db
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Substitua 'your_token_here' pelo token do seu bot
TOKEN = 'MTI0NzQzMzQ2MzA1ODAxMDE3NA.GwXcIG.mXvu206MlClM8xGCdcVFyH5G_9u6Cr0yMtNpNE'

# Configurações do bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# IDs dos usuários autorizados
AUTHORIZED_USERS = {123456789012345678, 987654321098765432}  # Substitua com os IDs reais

# Criar a tabela no banco de dados
db.create_table()

# Comandos do bot
@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} está online!')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(generate_weekly_report, 'cron', day_of_week='sun', hour=22, minute=0)
    scheduler.start()

def is_authorized(user_id):
    return user_id in AUTHORIZED_USERS

@bot.command(name='setmeta')
async def set_meta(ctx, funcionario: str, meta: str):
    if not is_authorized(ctx.author.id):
        await ctx.send('Você não tem permissão para definir metas.')
        return
    db.add_meta(funcionario, meta)
    await ctx.send(f'Meta "{meta}" definida para {funcionario}.')

@bot.command(name='metas')
async def listar_metas(ctx):
    metas = db.get_metas()
    if not metas:
        await ctx.send('Nenhuma meta definida.')
    else:
        metas_str = "\n".join([f'{row[1]}: {row[2]} - {row[3]} (Criada em: {row[4]})' for row in metas])
        await ctx.send(f'Metas atuais:\n```\n{metas_str}\n```')

@bot.command(name='statusmeta')
async def status_meta(ctx, funcionario: str, status: str):
    if not is_authorized(ctx.author.id):
        await ctx.send('Você não tem permissão para atualizar o status das metas.')
        return
    db.update_status(funcionario, status)
    await ctx.send(f'Status da meta de {funcionario} atualizado para {status}.')

@bot.command(name='deletemeta')
async def delete_meta(ctx, funcionario: str, meta: str):
    if not is_authorized(ctx.author.id):
        await ctx.send('Você não tem permissão para deletar metas.')
        return
    db.delete_meta(funcionario, meta)
    await ctx.send(f'Meta "{meta}" de {funcionario} foi deletada.')

@bot.command(name='metasfuncionario')
async def metas_funcionario(ctx, funcionario: str):
    metas = db.get_metas_by_funcionario(funcionario)
    if not metas:
        await ctx.send(f'Nenhuma meta encontrada para {funcionario}.')
    else:
        metas_str = "\n".join([f'{row[2]} - {row[3]} (Criada em: {row[4]})' for row in metas])
        await ctx.send(f'Metas de {funcionario}:\n```\n{metas_str}\n```')

@bot.command(name='relatoriosemanal')
async def relatorio_semanal(ctx):
    await generate_weekly_report(ctx)
    await ctx.send('Relatório semanal gerado e metas resetadas.')

async def generate_weekly_report(ctx=None):
    # Calcular a data de início e fim da semana passada
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    # Obter metas da semana passada
    metas = db.get_metas_by_date_range(start_date, end_date)

    if not metas:
        if ctx:
            await ctx.send('Nenhuma meta encontrada para a semana passada.')
        return

    # Criar o relatório
    atingidas = [meta for meta in metas if meta[3].lower() == 'completa']
    nao_atingidas = [meta for meta in metas if meta[3].lower() != 'completa']

    atingidas_str = "\n".join([f'{meta[1]}: {meta[2]} (Criada em: {meta[4]})' for meta in atingidas])
    nao_atingidas_str = "\n".join([f'{meta[1]}: {meta[2]} (Criada em: {meta[4]})' for meta in nao_atingidas])

    channel = discord.utils.get(bot.get_all_channels(), name='relatorios')  # Substitua com o nome do canal de relatórios

    if channel:
        await channel.send(f'Relatório Semanal de Metas\n\n**Metas Atingidas:**\n```\n{atingidas_str}\n```\n**Metas Não Atingidas:**\n```\n{nao_atingidas_str}\n```')
    
    # Resetar as metas
    db.reset_metas()

# Executar o bot
bot.run(TOKEN)
