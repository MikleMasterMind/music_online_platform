import asyncio
import shlex


class ConectProcessor:
    def __init__(self, musicSQL_db, musicFile_db, logged_users):
        self.musicSQL = musicSQL_db  # Объект для работы с БД
        self.musicFile = musicFile_db
        # self.logged_users = logged_users  # Ссылка на словарь logged_users из MusicServer
        # self.registered_users = musicSQL_db.get_registered_users()  # Ссылка на множество registered_users из MusicServer
        #self.logged_in = False
        

    async def process_command(self, command, writer) -> list:   
        try:
            match command:
                # case ['registration', username, name, password]:
                #     if writer in self.logged_users:
                #         return f"Make a <logout> in order to register a new user."
                #     if username not in self.registered_users:
                #         self.music.add_user(username, name, password)
                #         self.registered_users.add(username)
                #         res = f"User {username} registered successfully"
                #         return res
                #     return f"Username {username} is occupied, use a different one."
                # case ['login', username, password]:
                #     if writer in self.logged_users:
                #         return "You are already logged in. Logout first."
                #     if self.music.verify_user(username, password):
                #         self.logged_users[writer] = username
                #         res =  f"Welcome, {username}!"
                #         return res
                #     res = "Login failed"
                #     return res 
                # case ['logout']:
                #     if writer in self.logged_users:
                #         username = self.logged_users[writer]
                #         del self.logged_users[writer]
                #         return f"Logged out successfully, {username}"
                #     return "You are not logged in"
                case ["GET", "FILE", *music_title]:
                    music_title = f'{" ".join(music_title)}.mp3'.replace(' ', '-')
                    if self.musicFile.music_exist(music_title):
                        return ["FILE", self.musicFile.get_music(music_title)]
                    else:
                        return []
                case ["FIND", "FILE", *music_title]:
                    music_title = f'{" ".join(music_title)}.mp3'.replace(' ', '-') 
                    if self.musicFile.music_exist(music_title):
                        answer = "FOUND FILE"
                    else:
                        answer = "NOT FOUND FILE"
                    return ["TEXT", answer]
                case ["ADD", "FILE", *music_title]:
                    music_title = f'{" ".join(music_title)}.mp3'.replace(' ', '-') 
                    if self.musicFile.music_exist(music_title):
                        i = 1
                        music_title = f'{music_title}-{i}'
                        while self.musicFile.music_exist(music_title):
                            i += 1
                    self.musicFile.init_file(music_title)
                    return ["GET", "FILE"]
                case _:
                    return []
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    def write_to_file(self, data):
        self.musicFile.write_data(data)
    
    def close_file_conn(self):
        self.musicFile.close_file()