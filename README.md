🛠️ Bot Overview
The bot will:
- Accept commands like !register, !myinfo, !updateinfo
- Collect gamertags for platforms (Steam, PSN, Xbox, etc.)
- Optionally store email, phone, or social handles (only if user agrees)
- Securely save everything in PostgreSQL

✏️ Command Flow

!register
User starts the process → bot asks for platform and tag info → optional contact details → saves in DB

!myinfo
Bot retrieves and displays user's registered tags and contact info (if consented)

!updateinfo
User modifies existing info → bot updates PostgreSQL

🔐 Safety & Privacy Notes
- Use role-based access or DMs for sensitive input.
- Never collect private info without opt-in consent.
- Validate phone and email formats before storing.
- Consider hashing contact data if needed.

🚀 Launch the Bot
From the discord-bot/ directory, run:
docker-compose up --build


Your bot will be live and connected to PostgreSQL, fully isolated in its container!
