import discord
import json
import asyncio

client = discord.Client()
token = input("[?] Auth token: ").strip()
msg_txt = input("[?] Content to broadcast: ").strip()

@client.event
async def onrdy():
    print("[*] Delivery session launched...\n")

    try:
        with open("ids.json", "r") as f:
            targets = json.load(f)
    except Exception as err:
        print(f"[ERR] Failed to read data: {err}")
        await client.close()
        return

    total = len(targets)
    sent = 0

    for idx, uid in enumerate(targets):
        try:
            usr = await client.fetch_user(uid)
            await usr.send(msg_txt)
            sent += 1
            print(f"[✓] Dispatched {idx+1}/{total} → {usr.name}")
            await asyncio.sleep(1.2)
        except Exception as err:
            print(f"[x] Skipped {uid}: {err}")

    print(f"\n[+] Broadcast complete. {sent}/{total} successful.")
    await client.close()

client.on_ready = onrdy
client.run(token, bot=False)
