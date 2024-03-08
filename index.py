import tkinter as tk
from tkinter import simpledialog
from functools import partial
from pydub import AudioSegment
import os
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq

# Cấu hình đường dẫn FFmpeg
FFMPEG_BIN_DIR = r"C:\ffmpeg-master-latest-win64-gpl\bin"
AudioSegment.converter = os.path.join(FFMPEG_BIN_DIR, 'ffmpeg.exe')
AudioSegment.ffprobe = os.path.join(FFMPEG_BIN_DIR, 'ffprobe.exe')


def apply_effect_and_play(effect_func, *args, **kwargs):
    try:
        audio = AudioSegment.from_file(sound_file)
        processed_audio = effect_func(audio, *args, **kwargs)
        play(processed_audio)
        plot_frequency_response(processed_audio)
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")


def plot_frequency_response(audio_segment, title="Frequency Response"):
    # Chuyển đoạn âm thanh PyDub sang mảng numpy
    samples = np.array(audio_segment.get_array_of_samples())
    # FFT và tần số
    Y = fft(samples)
    freq = fftfreq(len(Y), 1 / audio_segment.frame_rate)

    plt.figure(figsize=(10, 5))
    plt.plot(freq, np.abs(Y))
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.xlim(0, audio_segment.frame_rate / 2)
    plt.show()


def choose_file():
    global sound_file
    # Mở hộp thoại chọn file và cập nhật biến sound_file với đường dẫn file được chọn
    file_path = filedialog.askopenfilename()
    if file_path:
        sound_file = file_path
        print(f"File được chọn: {sound_file}")


def distort_audio(audio, distortion_level=20):
    # Chuyển đoạn âm thanh PyDub sang mảng numpy
    samples = np.array(audio.get_array_of_samples())
    # Điều chỉnh kiểu dữ liệu để phù hợp với hàm tanh, tránh overflow
    float_samples = samples.astype(np.float32)
    # Áp dụng hàm tanh để tạo biến dạng
    # Các mẫu được chuẩn hóa và sau đó được nhân với 'distortion_level'
    # để điều chỉnh mức độ biến dạng
    distorted_samples = np.tanh(float_samples / np.max(np.abs(float_samples)) * distortion_level)
    # Chuẩn hóa các mẫu đã biến dạng về lại độ lớn ban đầu của mẫu âm thanh
    distorted_samples = distorted_samples * np.max(np.abs(samples))
    # Chuyển lại sang kiểu dữ liệu ban đầu
    distorted_samples = distorted_samples.astype(samples.dtype)
    # Tạo đoạn âm thanh PyDub mới từ các mẫu đã biến dạng
    distorted_audio = audio._spawn(distorted_samples.tobytes())

    return distorted_audio


def apply_distortion_with_custom_level():
    # Yêu cầu người dùng nhập mức độ biến dạng
    distortion_level = simpledialog.askinteger("Distortion", "Enter distortion level:", parent=root, minvalue=1,
                                               maxvalue=100)

    if distortion_level is not None:  # Kiểm tra xem người dùng có nhập giá trị hay không
        apply_effect_and_play(distort_audio, distortion_level=distortion_level)

def reverse_audio(audio):
    return audio.reverse()


def apply_fade():
    # Yêu cầu người dùng nhập thời gian fade in và fade out
    fade_in_time = simpledialog.askinteger("Input", "Fade in time (ms):", parent=root, minvalue=0, maxvalue=10000)
    fade_out_time = simpledialog.askinteger("Input", "Fade out time (ms):", parent=root, minvalue=0, maxvalue=10000)

    if fade_in_time is not None and fade_out_time is not None:
        # Gọi hàm apply_effect_and_play với hàm fade và các tham số vừa nhập
        apply_effect_and_play(fade, fade_in=fade_in_time, fade_out=fade_out_time)


def fade(audio, fade_in=2000, fade_out=2000):
    return audio.fade_in(fade_in).fade_out(fade_out)


low_pass_cutoff = 3000  # Giá trị mặc định
high_pass_cutoff = 3000  # Giá trị mặc định


def set_cutoff_frequency():
    global low_pass_cutoff, high_pass_cutoff
    low_pass_cutoff = simpledialog.askinteger("Low Pass Filter", "Enter cutoff frequency (Hz):", parent=root,
                                              minvalue=20, maxvalue=20000, initialvalue=3000)
    high_pass_cutoff = simpledialog.askinteger("High Pass Filter", "Enter cutoff frequency (Hz):", parent=root,
                                               minvalue=20, maxvalue=20000, initialvalue=3000)


def low_pass_filter(audio):
    global low_pass_cutoff
    return audio.low_pass_filter(low_pass_cutoff)


def high_pass_filter(audio):
    global high_pass_cutoff
    return audio.high_pass_filter(high_pass_cutoff)


def echo(audio, delay=900, decay=0.5, repetitions=3):
    output = audio
    for i in range(1, repetitions + 1):
        # Tính toán giảm âm lượng cho mỗi lần lặp
        decibel_reduction = -decay * i * 10  # Giảm âm lượng theo dB, giả sử decay là một tỷ lệ giảm âm lượng linh hoạt
        echo_segment = audio.apply_gain(decibel_reduction)
        # echo_segment = audio - decibel_reduction # Cách thay thế nếu bạn không muốn sử dụng apply_gain
        output = output.overlay(echo_segment, position=delay * i)
    return output


from pydub import AudioSegment
from pydub.playback import play
from tkinter import filedialog


def merge_audio_segments():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ Tkinter chính
    sound_files = filedialog.askopenfilenames(title="Chọn các tệp âm thanh để ghép")  # Cho phép chọn nhiều tệp
    if sound_files:
        try:
            combined_audio = None  # Khởi tạo biến để lưu trữ âm thanh ghép
            for sound_file in sound_files:
                # Tải đoạn âm thanh
                audio = AudioSegment.from_file(sound_file)

                # Yêu cầu người dùng nhập mức điều chỉnh âm lượng cho mỗi đoạn qua GUI
                adjustment = simpledialog.askfloat("Điều Chỉnh Âm Lượng",
                                                   f"Nhập mức điều chỉnh âm lượng cho {sound_file} (dB):",
                                                   parent=root)
                # Kiểm tra nếu người dùng nhấn Cancel
                if adjustment is None:
                    continue  # Bỏ qua đoạn này và tiếp tục với đoạn tiếp theo
                # Điều chỉnh âm lượng
                adjusted_audio = audio.apply_gain(adjustment)
                # Ghép âm thanh đã điều chỉnh vào đoạn tổng
                if combined_audio is None:
                    combined_audio = adjusted_audio
                else:
                    combined_audio += adjusted_audio
            if combined_audio:
                # Chơi đoạn âm thanh kết quả
                play(combined_audio)
                # Xuất đoạn âm thanh kết quả
                output_file = filedialog.asksaveasfilename(defaultextension='.mp3', title="Lưu tệp âm thanh")
                if output_file:
                    combined_audio.export(output_file, format='mp3')
        except Exception as e:
            print(f"Đã xảy ra lỗi khi điều chỉnh và ghép âm thanh: {e}")
        finally:
            root.destroy()  # Đóng cửa sổ Tkinter


def play_audio():
    try:
        audio = AudioSegment.from_file(sound_file)
        play(audio)
    except Exception as e:
        print(f"Error playing original audio: {e}")


# Cấu trúc dữ liệu quản lý hiệu ứng
effects = {
    'Reverse': reverse_audio,
    'Low Pass Filter': low_pass_filter,
    'High Pass Filter': high_pass_filter,
    'Echo': partial(echo, delay=900, decay=0.5, repetitions=3),
}

root = tk.Tk()
root.title("Advanced Sound Player")

choose_file_button = tk.Button(root, text="Choose File", command=choose_file)
# Đặt nút chọn file ở giữa bên phải của giao diện
choose_file_button.pack(pady=5, padx=10, side='right', fill='x')

play_original_button = tk.Button(root, text="Play Original", command=play_audio)
play_original_button.pack(pady=5, padx=10, side='bottom', fill='x')

fade_button = tk.Button(root, text="Custom Fade", command=apply_fade)
fade_button.pack(pady=5, padx=10, side='top', fill='x')

distort_button = tk.Button(root, text="Distort Custom Level", command=apply_distortion_with_custom_level)
distort_button.pack(pady=5, padx=10, side='top', fill='x')

for effect_name, effect_func in effects.items():
    button = tk.Button(root, text=effect_name,
                       command=partial(apply_effect_and_play, effect_func))
    button.pack(pady=5, padx=10, side='top', fill='x')

merge_play_button = tk.Button(root, text="Merge and Play",
                              command=lambda: merge_audio_segments())
merge_play_button.pack(pady=5, padx=10, side='top', fill='x')
root.mainloop()
