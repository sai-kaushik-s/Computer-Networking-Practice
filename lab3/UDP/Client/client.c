#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <libgen.h>
#include <time.h>

#define PORT 9009
#define MAX 1024

struct message{
    int seq;
    char buffer[MAX];
    int size;
};

int main(){
	int clientSocket;
    char buffer[MAX], check[1];
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

    char path[MAX];
    printf("Enter the path of the file you wish to send: ");
    scanf("%s", path);
    char *fileName = basename(path);
    printf("%s\n", fileName);

    sendto(clientSocket, fileName, strlen(fileName), 0, (struct sockaddr *)&serverAddr, len);

    FILE *fp = fopen(path, "rb");
    if(fp == NULL){
        printf("File could not be opened.\n");
        exit(EXIT_FAILURE);
    }
    int b;
    struct message data;
    data.seq = 0;
    clock_t t = clock();
    while(1){
        data.seq++;
        data.size = fread(data.buffer, 1, sizeof(data.buffer), fp);
        if(data.size == 0){
            data.seq = -1;
            sendto(clientSocket, &data, sizeof(data), 0, (struct sockaddr *)&serverAddr, len);
            break;
        }
        a: 
        sendto(clientSocket, &data, sizeof(data), 0, (struct sockaddr *)&serverAddr, len);
        recvfrom(clientSocket, check, 1, 0, (struct sockaddr *)&serverAddr, &len);
        if(strncmp(check, "y", 1) == 0) goto a;
    }
    t = clock() - t;
    double time = ((double)t)/CLOCKS_PER_SEC; 
    printf("Time taken to transfer the file: %f seconds.\n", time);
    printf("File transmitted..\n");
    fclose(fp);
	close(clientSocket);
	return 0;
}