import socket
import threading
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


def send_audio(client_socket):
    while True:
        audio_data = stream.read(CHUNK)
        client_socket.sendall(audio_data)


def receive_audio(client_socket):
    play_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    while True:
        try:
            data = client_socket.recv(CHUNK)
            if not data:
                break
            play_stream.write(data)
        except:
            break


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    send_thread = threading.Thread(target=send_audio, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_audio, args=(client_socket,))

    send_thread.start()
    receive_thread.start()


if __name__ == "__main__":
    start_client()