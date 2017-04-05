import socket

def addStartBit(char):
    char = '0' + char
    return char

def addStopBits(char):
    char = char + '11'
    return char

def prepareFrames(sentence):
    frame = 'f'
    for char in sentence:
        char = bin(ord(char))[2:]
        #jeżeli liczba bitów znaku jest mniejsza niż 7 ( jak dla liter w ASCII),
        #to na początku dodaj tyle zer, aby było 7 bitów
        if len(char)<7:
            for i in range(0, 7-len(char)):
                char = '0' + char
        char = addStartBit(char)
        char = addStopBits(char)
        for c in char:
            frame += c
    return frame[1:]

# word = 'elo stej stony tige benc'
# frames = prepareFrames(word)
# print(frames)

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    message = input('Message: ')
    frames = prepareFrames(message)
    print(frames)
    for bit in frames:
        s.send(bit.encode(encoding='utf-8', errors='strict'))
    s.close()
    if message == 'end':
        break


