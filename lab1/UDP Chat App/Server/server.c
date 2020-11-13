#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 9009
#define MAX 1024

int main() {
	int serverSocket;
	char recvMsg[MAX];
	char sendMsg[MAX];
	struct sockaddr_in serverAddr, clientAddr;
	
	if ((serverSocket = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
		printf("Socket could not be created.\n");
		exit(EXIT_FAILURE);
	}
	
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = INADDR_ANY;
	serverAddr.sin_port = htons(PORT);
	
	if (bind(serverSocket, (const struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0){
		printf("Could not bind with the client.\n");
		exit(EXIT_FAILURE);
	}
	
	int n;
    socklen_t len = sizeof(serverAddr);

    printf("Wait for the message from the client......\n\n");

    while(1){
        n = recvfrom(serverSocket, (char *)recvMsg, sizeof(recvMsg), 0, (struct sockaddr *) &clientAddr, &len);
        recvMsg[n] = '\0';
        printf("Client: %s\n", recvMsg);
        printf("Server: ");
        fgets(sendMsg, sizeof(sendMsg), stdin);
        sendto(serverSocket, (char *)sendMsg, sizeof(sendMsg), 0, (struct sockaddr *) &clientAddr, sizeof(clientAddr));
	}

	close(serverSocket);
	return 0;
}