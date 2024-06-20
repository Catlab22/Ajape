import db

def get_killed(night: bool) -> str | None:
    if not night:
        username_killed = db.citizen_kill()
        return f"Горожане... {username_killed}" 
    username_killed = db.mafia_kill()
    return f"Мафия... {username_killed}"

