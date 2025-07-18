import discord
import openai
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Bot personality & knowledge
system_prompt = """
You are NepalMartBot, the smart, friendly assistant of Nepal Digital Mart.
Your job:
- Help clients with prices, payment methods, and what the shop sells (Discord Nitro, VPN, Spotify, Netflix, game keys, Windows keys, custom emojis/banners)
- Suggest users to create a support ticket or DM staff for custom gift cards, game top-up, Steam keys, or anything not in stock
- Speak in short, polite, slightly playful sentences, and use emojis sometimes
- Always say you're part of Nepal Digital Mart
If users ask something unrelated, politely say: "I'm here to help with Nepal Digital Mart questions only! 😊"
"""

price_list = """
📦 **Nepal Digital Mart Price List:**  
💎 Nitro 1 month (Basic): Rs 350
💎 Nitro 12 months (Basic): Rs 2400
✨ Nitro 1 month (Advanced): Rs 900
✨ Nitro 12 months (Advanced): Rs 7100
🎮 Minecraft (Java & Bedrock): Rs 3200
🎟 Steam Game keys: Varies (DM/Ticket)
🔑 NordVPN 1m: Rs 2000 | 12m: Rs 9300 | 24m: Rs 12000
🛡 ProtonVPN 12m: Rs 14000
🖼 Canva Plus: DM/Ticket
🎵 Spotify Premium: Rs 200
📺 Netflix Pro: Rs 450
💻 Office 2019 Key: DM/Ticket
🤖 ChatGPT Premium: Rs 3000
😀 Custom Emojis pack: Rs 400
🖼 Custom Server banners: Rs 400
🪟 Windows 10/11 Premium Key: Rs 1400 each
🦠 Antivirus (1 year): DM/Ticket
♦️ Other VPN: DM/Ticket
💰 Payment: eSewa / Crypto
"""

@client.event
async def on_ready():
    print(f'✅ NepalMartBot is online as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    # Commands
    if content.startswith("!price"):
        await message.channel.send(price_list)
        return

    if content.startswith("!giftcard") or content.startswith("!topup"):
        await message.channel.send("🎁 For gift cards, game top-up & special orders: **please create a support ticket or DM us!** 🛠")
        return

    if content.startswith("!help"):
        await message.channel.send(
            "**🤖 NepalMartBot Help:**\n"
            "• `!price` → Show full price list\n"
            "• `!giftcard` / `!topup` → Ask about custom orders\n"
            "• Or just type your question and I'll help! 😊"
        )
        return

    # ChatGPT AI reply (in DM or in channels)
    if isinstance(message.channel, discord.DMChannel) or True:  # remove "or True" if you want it to answer only in DM
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # or "gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message.content}
                ]
            )
            reply = response['choices'][0]['message']['content']
            await message.channel.send(reply)
        except Exception as e:
            print(e)
            await message.channel.send("⚠️ Sorry, something went wrong. Please try again later!")

client.run(os.getenv("DISCORD_BOT_TOKEN"))