import win32pipe, win32file

class PipeServer():
    def __init__(self, pipeName):
        self.pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\\'+pipeName,
        win32pipe.PIPE_ACCESS_OUTBOUND,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None)

    #Carefull, this blocks until a connection is established
    def connect(self):
        print("connect start")
        win32pipe.ConnectNamedPipe(self.pipe, None)
        print("connect end")

    #Message without tailing '\n'
    def write(self, message):
        print("write start")
        win32file.WriteFile(self.pipe, message.encode()+b'\n')
        print("write end")

    def close(self):
        print("close start")
        win32file.CloseHandle(self.pipe)
        print("close end")

t = PipeServer("DMXServer")
t.connect()
t.write("Hello from Python :)")
t.write("Closing now...")
t.close()