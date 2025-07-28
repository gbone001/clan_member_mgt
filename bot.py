import discord
from discord.ext import commands
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def create_pool():
    return await asyncpg.create_pool(os.getenv("PG_URL"))

@bot.event
async def on_ready():
    bot.db = await create_pool()
    print(f"{bot.user} is online!")

@bot.command()
async def register(ctx, platform: str, tag: str, email: str = None):
    discord_id = ctx.author.id
    username = ctx.author.name
    
    async with bot.db.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (discord_id, username) VALUES ($1, $2)
            ON CONFLICT (discord_id) DO NOTHING
        """, discord_id, username)

        await conn.execute("""
            INSERT INTO gamer_tags (discord_id, platform, tag)
            VALUES ($1, $2, $3)
            ON CONFLICT (discord_id, platform) DO UPDATE SET tag=$3
        """, discord_id, platform, tag)

        if email:
            await conn.execute("""
                INSERT INTO contact_info (discord_id, email, consent)
                VALUES ($1, $2, TRUE)
                ON CONFLICT (discord_id) DO UPDATE SET email=$2, consent=TRUE
            """, discord_id, email)

    await ctx.send(f"✅ Info registered for {username}!")

@bot.command()
async def myinfo(ctx):
    discord_id = ctx.author.id
    async with bot.db.acquire() as conn:
        tags = await conn.fetch("""
            SELECT platform, tag FROM gamer_tags WHERE discord_id = $1
        """, discord_id)
        contact = await conn.fetchrow("""
            SELECT email, consent FROM contact_info WHERE discord_id = $1
        """, discord_id)

    response = "🎮 Gamer Tags:\n"
    for row in tags:
        response += f"- {row['platform']}: {row['tag']}\n"
    if contact and contact['consent']:
        response += f"\n📧 Email: {contact['email']}"
    await ctx.send(response)

@bot.command()
async def showt17(ctx, member: discord.Member = None):
    """Show a member's T17 gamer tag"""
    if member is None:
        member = ctx.author
    
    discord_id = member.id
    async with bot.db.acquire() as conn:
        t17_tag = await conn.fetchrow("""
            SELECT tag FROM gamer_tags 
            WHERE discord_id = $1 AND platform = 'T17'
        """, discord_id)
    
    if t17_tag:
        await ctx.send(f"🎮 {member.display_name}'s T17 tag: **{t17_tag['tag']}**")
    else:
        await ctx.send(f"❌ No T17 tag found for {member.display_name}")

bot.run(os.getenv("DISCORD_TOKEN"))
