import tkinter as tk
from functools import partial
from pydub import AudioSegment
import os
from pydub.playback import play


# Hàm bóp méo âm thanh
def distort_audio(audio, distortion_level=20):
    # Ví dụ: tăng volume để mô phỏng hiệu ứng bóp méo
    return audio + distortion_level


# Hàm phát âm thanh đã xử lý
def play_processed_audio(audio):
    play(audio)


# Hàm áp dụng hiệu ứng và phát âm thanh
def apply_effect_and_play(effect, sound_file):
    try:
        audio = AudioSegment.from_file(sound_file)
        if effect == 'speed_up':
            playback_speed = 1.5  # Giả định tốc độ phát là 50% nhanh hơn
            # Tính toán số lượng khung hình mới
            new_frame_rate = int(audio.frame_rate * playback_speed)
            # Áp dụng tốc độ phát mới
            audio = audio.set_frame_rate(new_frame_rate)
        elif effect == 'slow_down':
            playback_speed = 0.5  # Giả định tốc độ phát là 50% chậm lại
            new_frame_rate = int(audio.frame_rate * playback_speed)
            # Áp dụng tốc độ phát mới
            audio = audio.set_frame_rate(new_frame_rate)
        elif effect == 'distort':
            distortion_level = 30  # Giả định mức độ bóp méo
            audio = distort_audio(audio, distortion_level)

        play(audio)
    except Exception as e:
        print("Đã xảy ra lỗi:", e)


# Thiết lập đường dẫn FFmpeg
FFMPEG_BIN_DIR = r"C:\ffmpeg-master-latest-win64-gpl\bin"
AudioSegment.converter = os.path.join(FFMPEG_BIN_DIR, 'ffmpeg.exe')
AudioSegment.ffprobe = os.path.join(FFMPEG_BIN_DIR, 'ffprobe.exe')

# Giao diện người dùng
root = tk.Tk()
root.title("Advanced Sound Player")

# Đường dẫn tới tệp âm thanh - thay thế bằng đường dẫn thực tế của bạn
sound_file = r"C:\Users\ACER\Documents\Zalo Received Files\sound\wow-121578.mp3"

effects = ['speed_up', 'slow_down', 'distort']

for effect in effects:
    button = tk.Button(root, text=effect.replace('_', ' ').title(),
                       command=partial(apply_effect_and_play, effect, sound_file))
    button.pack(pady=5, padx=10, side='top', fill='x')

root.mainloop()
