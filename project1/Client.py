import socket           # socket import

server_IP='127.0.0.1'   # Local Host IP 주소
server_PORT=1234        # 임의의 PORT 번호

client_sckt=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# client socket 생성 : IPV4, TCP, socket 사용
client_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server socket의 옵션 설정
client_sckt.connect((server_IP, server_PORT))
# 해당 IP Address와 PORT Number에 연결

while True:     # 무한 루프를 통해 지속적인 통신
    data=input()                                # data를 입력 받는다
    client_sckt.send(data.encode('utf-8'))      # data를 encoding하여 server로 전송한다

    if data.upper()=="CLOSE":                           # 입력 받은 data가 CLOSE 
        print("Close Connect")                  # 연결을 종료한다는 메세지 출력
        break                                   # 무한 루프를 빠져나간다
    else:                                       # 입력 받은 data가 CLOSE가 아니라면
        print("Data send")                      # 데이터 전송 완료를 출력

    recieve_data=client_sckt.recv(1024).decode('utf-8')    # 서버로부터 받은 data를 저장
    print("{}\n".format(recieve_data))                     # 서버로부터 받은 data를 출력

client_sckt.close()             # client의 socket를 종료한다