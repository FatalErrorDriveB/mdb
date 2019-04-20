import sqlite3


class DataBase:
    def __init__(self, db, c):
        self.db = db
        self.c = c
        db = sqlite3.connect('user_info.db')
        c = db.cursor()

    class Profile:
        def _init_(self, name, level, completed_stories, exp, atk, hp, block, max_hp, gwc, gold):
            self.name = name
            self.level = level
            self.completed_stories = completed_stories
            self.gold = gold
            self.exp = exp
            self.atk = atk
            self.max_hp = max_hp
            self.hp = hp
            self.block = block
            self.gwc = gwc  # Global Word Count

    def create_profile(self):
        self.c.execute("""CREATE TABLE profiles (
                   name text,
                   lvl integer,
                   exp real,
                   gold real,
                   max_hp real,
                   hp real,
                   atk integer,
                   block integer,
                   global_word_count integer,
                   completed_stories integer
                   )""")
        self.db.commit()
        self.db.close()

    def update_profile(self, profile):
        self.c.execute("INSERT INTO profiles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (profile.lvl, profile.exp, profile.gold, profile.max_hp,
                        profile.hp, profile.atk, profile.block, profile.global_word_count, profile.completed_stories))
        self.db.commit()

    def load_profile(self, name):
        profile = self.Profile()
        p = self.db.profiles("?", name)
        profile.name = name
        profile.level = p.lvl
        profile.exp = p.exp
        profile.gold = p.gold
        profile.max_hp = p.max_hp
        profile.hp = p.hp
        profile.atk = p.atk
        profile.block = p.block
        profile.gwc = p.global_word_count
        profile.completed_stories = p.completed_stories
        return profile
