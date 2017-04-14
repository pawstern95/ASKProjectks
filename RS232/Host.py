import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1
FRAME = 10

def delStartBit(word):
    return word[1:]

def delStopBits(word):
    return word[:-2]

def deleteFrames(char):
    char = delStartBit(char)
    char = delStopBits(char)
    return char

def divideString(string):
    chars = []
    for i in range(0, int(len(string) / FRAME)):
        char = 'f'
        for j in range(i * FRAME, i * FRAME + FRAME):
            char += str(string[j])
        chars.append(char[1:])
    return chars

def encodeMessage(string):
    chars = divideString(string)
    charsWithoutStartAndStopBits = []
    for c in chars:
        charsWithoutStartAndStopBits.append(deleteFrames(c))
    ints = []
    for c in charsWithoutStartAndStopBits:
        ints.append(int(c,2))
    encodedMessage = 's'
    for i in ints:
        encodedMessage += chr(i)
    return encodedMessage[1:]

def censor(sentence):
    badWords = ['karakan', 'piwo', 'wodka', 'Wojtek', 'stonoga', 'fajki', 'papierosy', 'lewak', 'lewactwo']
    for word in badWords:
        if word in sentence:
            sentence = sentence.replace(word, len(word) * '*')
    return sentence

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    frames = []
    while True:
        bit = conn.recv(BUFFER_SIZE)
        if not bit:
            break
        frames.append(int(bit))
    if frames != []:
        print(frames)
    encodedMessage = encodeMessage(frames)
    encodedMessage = censor(encodedMessage)
    if encodedMessage != '':
        print(encodedMessage)
    if encodedMessage == 'end':
        break
conn.close()


