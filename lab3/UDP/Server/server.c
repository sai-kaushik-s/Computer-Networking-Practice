#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <time.h>

#define PORT 9009
#define MAX 1024

struct message{
    int seq;
    char buffer[MAX];
    int size;
};

int main() {
	int serverSocket;
	char buffer[MAX];
	char fileName[MAX];
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
    socklen_t len = sizeof(clientAddr);

    memset(fileName, '\0', sizeof(fileName));
    recvfrom(serverSocket, fileName, sizeof(fileName), 0, (struct sockaddr *)&clientAddr, &len);
    printf("%s\n", fileName);

    FILE* fp = fopen(fileName, "wb");

    int b, i = 0, total = 0;
    struct message data;
    clock_t t = clock();
    while(1){
		i++;
		a: 
		n = recvfrom(serverSocket, &data, sizeof(data), 0, (struct sockaddr *)&clientAddr, &len);
		total += data.size;
		if(data.seq == -1) break;
		if(i != data.seq){
			sendto(serverSocket, "y", 1, 0, (struct sockaddr *)&clientAddr, len);
			goto a;
		}
		else sendto(serverSocket, "n", 1, 0, (struct sockaddr *)&clientAddr, len);
        fwrite(data.buffer, 1, data.size, fp);
    }
    t = clock() - t;
    double time = ((double)t)/CLOCKS_PER_SEC; 
    printf("File received..\nNumber of bytes transferred: %g MiB.\nTime taken to transfer the file: %f seconds.\n", (float)total / 1000000, time);

    fclose(fp);
	close(serverSocket);
	return 0;
}