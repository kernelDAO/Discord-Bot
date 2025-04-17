![discord](https://github.com/user-attachments/assets/cfe3f343-64c3-4e6e-b26b-f74077933e25)

> [!WARNING]
> This software is **not designed** for farming 24/7. It **needs to be monitored** at all times. Using it - **you** take responsibility for the **ban of your accounts** on discord servers. ALSO this code **uses Self-Bots**, which are **forbidden by Discord ToS**. Use of them is **punishable** by the **account blocking**.

> [!NOTE]
> If you see bad code or have a better idea — open a Pull Request.

# DiscordBot by kernelDAO

A simple software for farming roles on servers, powered by ChatGPT.

## Installation

1. Clone the repository:
```https://github.com/kernelDAO/Discord-Bot```

```cd Discord-Bot```


2. Install dependencies:
```pip install -r requirements.txt```


3. Add your Discord token and OpenAI keys in ```config.py```

4. Customize behavior in ```config.py```


## Configuration

```
TOKEN = "your_discord_token"     # Discord selfbot token

ACTIVE_CHANNELS = []             # Allowed channel IDs
ALLOWED_GUILDS = []              # Allowed server IDs

REPLY_PROBABILITY = 30           # % chance to reply to a message
REPLY_TO_REPLY_PROBABILITY = 70  # % chance to reply when replied to
GM_PROBABILITY = 0.6             # Chance to send GM message at startup

MIN_ANSWERS_BEFORE_PAUSE = 3     # Min replies before pause
MAX_ANSWERS_BEFORE_PAUSE = 6     # Max replies before pause

MIN_PAUSE_SECONDS = 600          # Min pause duration (in sec)
MAX_PAUSE_SECONDS = 1800         # Max pause duration (in sec)

MODEL = "gpt-4o-mini"          # OpenAI model name

OPENAI_API_KEYS = ["sk-xxx"]     # List of OpenAI API keys
OPENAI_PROXY = ""                # Optional proxy (http://user:pass@ip:port)
```

## Bot Logic
Here's a breakdown of how the selfbot operates step-by-step:

✅ On Startup (on_ready)
- *With a GM_PROBABILITY chance (e.g. 60%), the bot:*

- *Loads gms.txt*

- *Picks a random message*

- *Sends it to all active channels in allowed servers*

📩 On New Message (on_message)

Ignore messages from:

- *Itself (the bot)*

- *Unknown servers or channels (not in ALLOWED_GUILDS / ACTIVE_CHANNELS)*

- *While on cooldown pause*

Check if the message is a reply to the bot:

- *If yes → use REPLY_TO_REPLY_PROBABILITY (e.g. 70%)*

- *If no → use REPLY_PROBABILITY (e.g. 30%)*

- *If the chance fails, skip the message*

If responding:

- *Generate a GPT reply using the prompt and input message*

- *Simulate typing delay*

- *Send the message as a reply in the channel*

- *Log the response*

Track reply count:

- *After MIN_ANSWERS_BEFORE_PAUSE–MAX_ANSWERS_BEFORE_PAUSE replies,*

- *The bot enters a pause state (MIN_PAUSE_SECONDS–MAX_PAUSE_SECONDS)*

- *It stops responding until the cooldown ends*

### Example flow
```
User 1: hey what u doing

🤖 Bot (30% chance): just chillin lol

User 1 replies: for real?

🤖 Bot (70% chance): fr

…after a few messages…

🤖 Bot: [goes silent for 10–30 minutes] 😴```
