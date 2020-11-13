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
	char recvMsg[MAX];
	char sendMsg[MAX];
	struct sockaddr_in serverAddr;

	if ((clientSocket = socket(AF_INET, SOCK_DGRAM, 0)) < 0){
		printf("Socket could not be created.\n");
		exit(EXIT_FAILURE);
	}

	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
	serverAddr.sin_addr.s_addr = INADDR_ANY;

	int n;
    socklen_t len = sizeof(serverAddr);

	while(1){
        printf("Client: ");
        fgets(sendMsg, sizeof(sendMsg), stdin);
        if(sendMsg[0] == 'q' && sendMsg[1] == 'u' && sendMsg[2] == 'i' && sendMsg[3] == 't')
            break;
        sendto(clientSocket, (char *)sendMsg, sizeof(sendMsg), 0, (struct sockaddr *) &serverAddr, sizeof(serverAddr));

        n = recvfrom(clientSocket, (char *)recvMsg, sizeof(recvMsg), 0, (struct sockaddr *) &serverAddr, &len);
        recvMsg[n] = '\0';
        printf("Server: %s\n", recvMsg);
    }
    s: 
	close(clientSocket);
	return 0;
}