import tkinter as tk
from functools import partial
from pydub import AudioSegment
from pydub.playback import play
import os

# Cấu hình đường dẫn FFmpeg
FFMPEG_BIN_DIR = r"C:\ffmpeg-master-latest-win64-gpl\bin"
AudioSegment.converter = os.path.join(FFMPEG_BIN_DIR, 'ffmpeg.exe')
AudioSegment.ffprobe = os.path.join(FFMPEG_BIN_DIR, 'ffprobe.exe')

def distort_audio(audio, distortion_level=20):
    return audio + distortion_level

def reverse_audio(audio):
    return audio.reverse()

def fade(audio, fade_in=2000, fade_out=2000):
    return audio.fade_in(fade_in).fade_out(fade_out)

def low_pass_filter(audio, cutoff=3000):
    return audio.low_pass_filter(cutoff)

def high_pass_filter(audio, cutoff=3000):
    return audio.high_pass_filter(cutoff)

def apply_effect_and_play(effect_func, *args, **kwargs):
    try:
        audio = AudioSegment.from_file(sound_file)
        processed_audio = effect_func(audio, *args, **kwargs)
        play(processed_audio)
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

def echo(audio, delay=900, decay=0.5, repetitions=3):
    output = audio
    for i in range(1, repetitions + 1):
        # Tính toán giảm âm lượng cho mỗi lần lặp
        decibel_reduction = -decay * i * 10  # Giảm âm lượng theo dB, giả sử decay là một tỷ lệ giảm âm lượng linh hoạt
        echo_segment = audio.apply_gain(decibel_reduction)
        # echo_segment = audio - decibel_reduction # Cách thay thế nếu bạn không muốn sử dụng apply_gain
        output = output.overlay(echo_segment, position=delay * i)
    return output


# def flanger(audio, delay_ms=5, repetitions=20):
#     # Tạo một bản sao của đoạn âm thanh ban đầu
#     output = audio
#     # Áp dụng hiệu ứng overlay với một độ trễ nhỏ để tạo ra hiệu ứng "flanger-like"
#     for i in range(1, repetitions + 1):
#         segment = audio[0:-i*delay_ms].fade_in(50).fade_out(50)
#         output = output.overlay(segment, position=i*delay_ms)
#     return output

def merge_audio_segments(audio_path1, audio_path2):
    try:
        # Tải đoạn âm thanh thứ nhất
        audio1 = AudioSegment.from_file(audio_path1)
        # Tải đoạn âm thanh thứ hai
        audio2 = AudioSegment.from_file(audio_path2)
        # Ghép hai đoạn âm thanh
        combined_audio = audio1 + audio2
        # Chơi đoạn âm thanh kết quả
        play(combined_audio)
    except Exception as e:
        print(f"Đã xảy ra lỗi khi ghép âm thanh: {e}")

sound_file = r"C:\Users\ACER\Documents\Zalo Received Files\sound\8d82b5_Tom_Scream_Sound_Effect.mp3"
sound_file2 = r"C:\Users\ACER\Documents\Zalo Received Files\sound\echo-pop-5-189795.mp3"
# Cấu trúc dữ liệu quản lý hiệu ứng
effects = {
    'Fade In/Out': partial(fade, fade_in=2000, fade_out=2000),
    'Reverse': reverse_audio,
    'Distort': partial(distort_audio, distortion_level=30),
    'Low Pass Filter': partial(low_pass_filter, cutoff=3000),
    'High Pass Filter': partial(high_pass_filter, cutoff=3000),
    'Echo': partial(echo, delay=900, decay=0.5, repetitions=3),
    # 'Flanger': partial(flanger, delay=1, depth=2, rate=1, feedback=0.5)
}

root = tk.Tk()
root.title("Advanced Sound Player")

for effect_name, effect_func in effects.items():
    button = tk.Button(root, text=effect_name,
                       command=partial(apply_effect_and_play, effect_func))
    button.pack(pady=5, padx=10, side='top', fill='x')

merge_play_button = tk.Button(root, text="Merge and Play",
                              command=lambda: merge_audio_segments(sound_file, sound_file2))
merge_play_button.pack(pady=5, padx=10, side='top', fill='x')
root.mainloop()
