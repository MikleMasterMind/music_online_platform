import unittest
import os
import tempfile
from unittest.mock import patch, mock_open, MagicMock
from src.music_db.MusicFileDB import MusicFileDB

class TestMusicFileDB(unittest.TestCase):
    """Test cases for MusicFileDB class"""

    def setUp(self):
        """Create temporary directory and test files"""
        self.test_dir = tempfile.mkdtemp()
        
        self.test_mp3s = ['song1.mp3', 'song2.mp3']
        for fname in self.test_mp3s:
            with open(os.path.join(self.test_dir, fname), 'wb') as f:
                f.write(b'test data')
        
        with open(os.path.join(self.test_dir, 'not_mp3.txt'), 'wb') as f:
            f.write(b'text data')
            
        self.db = MusicFileDB(self.test_dir)

    def tearDown(self):
        """Clean up temporary directory"""
        for fname in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, fname))
        os.rmdir(self.test_dir)

    def test_initialization(self):
        """Test that initialization correctly loads MP3 files"""
        self.assertEqual(len(self.db.music_lst), 2)
        self.assertIn('song1.mp3', self.db.music_lst)
        self.assertIn('song2.mp3', self.db.music_lst)
        self.assertNotIn('not_mp3.txt', self.db.music_lst)

    def test_music_exist(self):
        """Test music_exist method"""
        self.assertTrue(self.db.music_exist('song1.mp3'))
        self.assertTrue(self.db.music_exist('song2.mp3'))
        self.assertFalse(self.db.music_exist('nonexistent.mp3'))
        self.assertFalse(self.db.music_exist('not_mp3.txt'))

    def test_get_music_existing(self):
        """Test get_music with existing file"""
        with patch('builtins.open', mock_open(read_data=b'test data')) as mocked_open:
            generator = self.db.get_music('song1.mp3')
            
            size = next(generator)
            self.assertEqual(size, b'9\n')  
            data = next(generator)
            self.assertEqual(data, b'test data')
            
            with self.assertRaises(StopIteration):
                next(generator)
            
            mocked_open.assert_called_once_with(f"{self.test_dir}/song1.mp3", 'rb')

    def test_get_music_nonexistent(self):
        """Test get_music with non-existent file"""
        result = list(self.db.get_music('nonexistent.mp3'))  
        self.assertEqual(result, [])  # return empty list 

    def test_file_operations(self):
        """Test file writing operations"""
        test_file = 'new_song.mp3'
        self.db.init_file(test_file)
        self.assertIn(test_file, self.db.music_lst)
        self.assertIsNotNone(self.db.opened_file)
        
        test_data = b'audio data'
        self.db.write_data(test_data)
        
        if self.db.opened_file:
            self.db.opened_file.close()
        self.db.close_file()
        
        with open(os.path.join(self.test_dir, test_file), 'rb') as f:
            self.assertEqual(f.read(), test_data)

if __name__ == '__main__':
    unittest.main()