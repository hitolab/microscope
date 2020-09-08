# クライアントを作成
import socket
import time
import schedule
​
#ハッシュ関数
def addChecksom(a):
    sum = 0
    for i in a:
        sum = sum + i
    last_a = (sum % 256)
    last_a_str = hex(last_a)[-2]+hex(last_a)[-1]
    last_a_byte = last_a_str.encode('utf-8')
    delimiter_str = '\r\n'
    delimiter_byte = delimiter_str.encode('utf-8')
    return a+last_a_byte+delimiter_byte
​
def sendMessage(msg):
    s.sendall(msg)
    print("send:"+str(msg))
    data = s.recv(1024)
    print(repr(data))
​
def setIP(ip):
    msg = b'@00E01' + ip.encode('utf-8')
    msg = addChecksom(msg)
    sendMessage(msg)
​
def setSubnetMask(mask):
    msg = b'@00E02' + mask.encode('utf-8')
    msg = addChecksom(msg)
    sendMessage(msg)
​
def setGateway(ip):
    msg = b'@00E03' + ip.encode('utf-8')
    msg = addChecksom(msg)
    sendMessage(msg)
​
def setLightIntensity(val):
    msg = b'@00F' + val.encode('utf-8')
    msg = addChecksom(msg)
    sendMessage(msg)
​
def LightON():
    msg = b'@00L1'
    msg = addChecksom(msg)
    sendMessage(msg)
​
def LightOFF():
    msg = b'@00L0'
    msg = addChecksom(msg)
    sendMessage(msg)
​
def oneCycle():
    LightOFF()
    time.sleep(D)
    LightON()
​
# Parameters
D = 60 # 何秒Dにするか(ここをフィールド数に合わせて調整が必要)
schedule.every().hour.do(oneCycle)
​
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('192.168.0.2', 40001))
    setSubnetMask('255.255.255.0')
    setLightIntensity('105')
    start = time.time()
    while True:
        schedule.run_pending()
