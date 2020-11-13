#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <libgen.h>

#define MAX 1024
#define PORT 9009

int main(){
    int clientSocket = 0, n=0, b;
    char sendbuffer[MAX];

    struct sockaddr_in clientAddr;

    clientSocket = socket(AF_INET, SOCK_STREAM, 0);

    clientAddr.sin_family = AF_INET;
    clientAddr.sin_port = htons(PORT);
    clientAddr.sin_addr.s_addr = INADDR_ANY;

    b = connect(clientSocket, (struct sockaddr *)&clientAddr, sizeof(clientAddr));
    if (b == -1){
        printf("Could not connect to the server.\n");
        exit(EXIT_FAILURE);
    }
    char path[MAX];
    printf("Enter the path of the file you wish to send: ");
    scanf("%s", path);
    char *fileName = basename(path);

    send(clientSocket, fileName, strlen(fileName), 0);

    FILE *fp = fopen(path, "rb");
    if(fp == NULL){
        printf("File could not be opened.\n");
        exit(EXIT_FAILURE);
    }
    while((b = fread(sendbuffer, 1, sizeof(sendbuffer), fp)) > 0){
        send(clientSocket, sendbuffer, b, 0);
    }
    fclose(fp);
    printf("File transferred..\n");
    close(clientSocket);
    exit(EXIT_SUCCESS);
}