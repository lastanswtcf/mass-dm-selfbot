import discord
import json

print("[*] Initializing scanner core...")

try:
    with open("ids.json", "r") as f:
        uid_cache = json.load(f)
except Exception as err:
    print(f"[ERR] Unable to load uid data: {err}")
    rsp = input("[?] Create new uid list? (y/n): ").strip().lower()
    while rsp not in ("y", "n"):
        rsp = input("[?] Create new uid list? (y/n): ").strip().lower()
    if rsp == "y":
        with open("ids.json", "w") as f:
            uid_cache = []
            json.dump(uid_cache, f)
        print("[+] Storage initialized.")

def logid(user):
    if getattr(user, "bot", False):
        return
    uid = user.id
    if uid not in uid_cache:
        uid_cache.append(uid)
        with open("ids.json", "w") as f:
            json.dump(uid_cache, f)
        print(f"[+] UID logged: {uid} | Total: {len(uid_cache)}")

client = discord.Client()
token = input("[?] Provide token: ")

 # events
@client.event
async def onrd():
    print("[✓] Scanner active.\n")
@client.event
async def onmsg(msg):
    logid(msg.author)
@client.event
async def onrxn(payload):
    if payload.member:
        logid(payload.member)
@client.event
async def onjn(user):
    logid(user)
@client.event
async def onupd(_, new):
    logid(new)
@client.event
async def onvc(member, _, __):
    logid(member)

client.on_ready = onrd
client.on_message = onmsg
client.on_raw_reaction_add = onrxn
client.on_member_join = onjn
client.on_member_update = onupd
client.on_voice_state_update = onvc

client.run(token, bot=False)
