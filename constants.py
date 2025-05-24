import os
from zoneinfo import ZoneInfo

SLEEP_TIME_LIMIT = 3600
IST = ZoneInfo("Asia/Kolkata")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
# Message bodies
BODIES = [
    """Hi {name},

Wishing you a fantastic birthday filled with joy, laughter, and celebration! 🎂🎈
May this year bring you new adventures and cherished memories.
""",
    """Hey {name},

Happy Birthday! 🎉✨
Hope your day is as amazing as you are. Stay awesome and keep smiling! 😊🎁
""",
    """Hi {name},

Cheers to you on your birthday! 🥂🎂
May this special day be the beginning of an amazing year ahead! 🎁🌈
""",
    """Hello {name},

Wishing you smiles, laughter, and tons of love on your birthday! 😊💖
Enjoy every moment of your special day! 🎉🎂
""",
    """Hey {name},

Hope your birthday is as sweet and bright as you are! 🍰🌟
Have a wonderful celebration! 🎈🎁
""",
    """Hi {name},

Happy Birthday to you! 🎊🎂
May your day be filled with happiness, your year with purpose, and your heart with love. ❤️
""",
    """Hi {name},

Wishing you a magical birthday and a year full of sparkles and dreams come true! ✨🎉
Have an amazing one! 🎂🎁
""",
    """Hi {name},

On your special day, may laughter and love surround you. ❤️🎉
Wishing you the happiest birthday and a brilliant year ahead! 🎂✨
""",
    """Hi {name},

Wishing you joy that lasts the whole year, not just your birthday! 🎈🥳
Have an awesome celebration and a fabulous year ahead! 🎁🍰
""",
]
