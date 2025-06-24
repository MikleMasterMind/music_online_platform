import os


class MusicFileDB:
    def __init__(self, path_to_mp3 = "./music_db/data"):
        self.path_to_mp3 = path_to_mp3
        files = os.listdir(path_to_mp3)
        mp3_files_only = [f for f in files if os.path.isfile(os.path.join(self.path_to_mp3, f)) and f[len(f) - 3:] == 'mp3']
        self.music_lst = set(mp3_files_only)
    
    def music_exist(self, music_title):
        return music_title in self.music_lst

    def get_music(self, music_title, chunk_size = 4096):
        if music_title not in self.music_lst:
            return

        filename = f"{self.path_to_mp3}/{music_title}"
        with open(filename, 'rb') as f:
            while chunk := f.read(chunk_size):
                yield chunk
