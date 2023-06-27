import socket           # socket import

server_IP='127.0.0.1'   # Local Host IP 주소
server_PORT=1234        # 임의의 PORT 번호

server_sckt=socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# client socket 생성 : IPV4, TCP, socket 사용
server_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# server socket의 옵션 설정
server_sckt.bind((server_IP, server_PORT))
# server socket에 IP address와 PORT를 bind
server_sckt.listen(5)
# 5개의 대기열을 갖도록 인자를 넣어 listen
server_fd, client_addr = server_sckt.accept()
# client의 connect를 받아들임
# client와 연결할 socket의 file discriptor와 client의 IP, PORT를 반환 및 저장

print("Server Connected at:",client_addr)
# 연결한 Client의 주소 표시

server_mem={}
# data 저장에 사용할 dictionary 설정

while True:     # 무한 루프를 통해 지속적인 통신
    received_data = server_fd.recv(1024).decode('utf-8', 'strict')  # 받은 data를 received_data에 저장
    data = received_data.split(",") # ','를 기준으로 나눠 data에 저장
    print("Data received")          # data를 성공적으로 받았음을 출력


    data_type = data[0]             # 이름의 직관성을 높이기 위해 data_type에 저장
    
    if data_type.upper() not in ["LIST", "CLOSE"]:           # data_type이 LIST와 CLOSE가 아니면
        data_key = data[1]          # data_key를 저장 (LIST는 key, value 값이 없어 오류가 발생)
    else:                           # data_type이 LIST면
        data_key = ' '              # 오류가 나지 않도록 설정

    if data_type.upper()=="PUT":            # data_type이 PUT이면
        data_value = data[2]        # data_value 저장 (PUT만 value를 사용하므로 나머지는 오류가 발생)
    else:                           # data_type이 PUT이 아니면
        data_value = ' '            # 오류가 나지 않도록 설정
        len_key = len(server_mem.keys())   # 비교에 사용할 key 길이를 변수로 저장

    if data_type.upper()=="CLOSE":          # CLOSE면
        break                       # LOOP 종료

    elif data_type.upper()=="PUT":          # PUT이면
        server_mem[data_key] = data_value  # KEY와 VALUE를 저장
        server_fd.send("Success!".encode('utf-8'))  # PUT을 성공했음을 Client에게 알림
        print("Data send\n")        # Data 전송에 성공했음을 알림

    elif data_type.upper()=="GET":          # GET이면
        if len_key:                 # key 값이 0이 아니면 (입력받았던 Data가 있으면)
            send_str=""             # 전송할 Data를 위한 문자열 생성
            for key in server_mem.copy().keys():   # server_mem에 저장된 key를 불러와서
                if data_key==key:                   # 입력 받은 key와 동일한지 비교
                    send_str=server_mem[key]       # 동일하면 key에 맞는 value를 문자열에 저장
            if len(send_str)==0:                    # 전송할 문자열이 비어있는경우
                server_fd.send("Not exist!".encode('utf-8'))    # 문자열이 존재하지 않음을 알림
            else:                                               # 문자열이 차 있는 경우
                server_fd.send(send_str.encode('utf-8'))        # 문자열을 보냄
        else:                                               # key가 0이라면
            server_fd.send("Not exist!".encode('utf-8'))    # 보낼 문자열이 없으므로 존재하지 않음을 알림

        print("Data send\n")            # Data 전송에 성공했음을 알림

    elif data_type.upper()=="DELETE":           # DELETE이면
        if len_key:                     # key 값이 0이 아니면 (입력받았던 Data가 있으면)
            for key in server_mem.copy().keys():   # server_mem에 저장된 key를 불러와서
                if data_key==key:                   # 입력 받은 key와 동일한지 비교
                    server_mem.pop(key)            # Data 제거
            if len_key==len(server_mem.keys()):    # data 제거되기 전과 제거된 후를 비교해서 제거된 값이 없는 경우
                server_fd.send("Not exist!".encode('utf-8'))    # 문자열이 존재하지 않음을 알림
            else:                                               # 제거된 경우
                server_fd.send("Success!".encode('utf-8'))      # 성공했음을 알림
        else:                                               # key가 0이라면
            server_fd.send("Not exist!".encode('utf-8'))    # 보낼 문자열이 없으므로 존재하지 않음을 알림

        print("Data send\n")            # Data 전송에 성공했음을 알림

    elif data_type.upper()=="LIST":             # LIST이면
        if len_key:                     # 입력받은 key 값이 0이 아니면 (입력받았던 Data가 있으면)
            send_str=""             # 전송할 Data를 위한 문자열 생성
            for key, value in server_mem.items():          # server_mem의 key값과 value 값을 차례대로 불러옴
                send_str+="{},{}\n".format(key, value)      # 전송할 문자열에 저장
            server_fd.send(send_str.encode('utf-8'))        # 문자열을 보냄
        else:                                               # data가 없다면
            server_fd.send("Not exist!".encode('utf-8'))    # 보낼 문자열이 없으므로 존재하지 않음을 알림

        print("Data send\n")            # Data 전송에 성공했음을 알림
    else:
        server_fd.send("Not Permitted Input".encode('utf-8'))

server_fd.close()
server_sckt.close()



