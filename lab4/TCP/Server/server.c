#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/time.h>
#include <math.h>

#define MAX 1024
#define PORT 9009

int main(){

    int serverSocket, clientSocket, b, total = 0;
    struct sockaddr_in serverAddr, clientAddr;
	struct timeval start, end;

    char buffer[MAX];
    int num;

    serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    memset(&serverAddr, '0', sizeof(serverAddr));
    memset(buffer, '\0', sizeof(buffer));

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    if(bind(serverSocket, (struct sockaddr*)&serverAddr, sizeof(serverAddr))){
        printf("Could not bind the server..\n");
        exit(EXIT_FAILURE);
    }
    listen(serverSocket, 10);

    socklen_t len = sizeof(clientAddr);
    clientSocket = accept(serverSocket, (struct sockaddr*)&clientAddr, &len);

    char fileName[MAX];
    memset(fileName, '\0', sizeof(fileName));
    recv(clientSocket, fileName, sizeof(fileName), 0);
    printf("%s\n", fileName);

    FILE* fp = fopen(fileName, "wb");
	gettimeofday(&start, NULL);
    if(fp != NULL){
        while((b = recv(clientSocket, buffer, sizeof(buffer), 0)) > 0){
            total += b;
            fwrite(buffer, 1, b, fp);
        }
        fclose(fp);
    }
	gettimeofday(&end, NULL);
	double time = (double)(end.tv_usec - start.tv_usec) / 1000000 + (double)(end.tv_sec - start.tv_sec);
    printf("File received..\nNumber of bytes transferred: %g MiB.\nTime taken to transfer the file: %f seconds.\n", (float)total / 1000000, time);
    close(clientSocket);
    exit(EXIT_SUCCESS);
}