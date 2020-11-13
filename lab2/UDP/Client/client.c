#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 9009
#define MAX 1024

int main(){
	int clientSocket;
	char recvMsg[MAX], Q1[MAX], Q2[MAX], A1[MAX], A2[MAX];
	char sendMsg[3];
	struct sockaddr_in serverAddr;

	if ((clientSocket = socket(AF_INET, SOCK_DGRAM, 0)) < 0){
		printf("Socket could not be created.\n");
		exit(EXIT_FAILURE);
	}

	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
	serverAddr.sin_addr.s_addr = INADDR_ANY;

    socklen_t len = sizeof(serverAddr);
    int a, b, n;
    char hello[] = "Hello server";
    sendto(clientSocket, (char *)hello, sizeof(hello), 0, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

	while(1){
        n = recvfrom(clientSocket, (char *)recvMsg, sizeof(recvMsg), 0, (struct sockaddr *) &serverAddr, &len);
        printf("%s", recvMsg);
        scanf("%s", sendMsg);
        if(!strncmp(sendMsg, "out", 3))
            break;
        sendto(clientSocket, (char *)sendMsg, sizeof(sendMsg), 0, (struct sockaddr *) &serverAddr, sizeof(serverAddr));
        getchar();

        n = recvfrom(clientSocket, (char *)Q1, sizeof(Q1), 0, (struct sockaddr *) &serverAddr, &len);
        printf("\n%s", Q1);

        if(Q1[6] == 'a')
            continue;

        scanf("%s", A1);
        sendto(clientSocket, (char *)A1, sizeof(A1), 0, (struct sockaddr *) &serverAddr, sizeof(serverAddr));
        getchar();

        n = recvfrom(clientSocket, (char *)Q2, sizeof(Q2), 0, (struct sockaddr *) &serverAddr, &len);
        printf("%s", Q2);
        scanf("%s", A2);
        sendto(clientSocket, (char *)A2, sizeof(A2), 0, (struct sockaddr *) &serverAddr, sizeof(serverAddr));
        getchar();

        n = recvfrom(clientSocket, (char *)recvMsg, sizeof(recvMsg), 0, (struct sockaddr *) &serverAddr, &len);
        recvMsg[n] = '\0';
        printf("%s\n\n", recvMsg);
    }
	close(clientSocket);
	return 0;
}