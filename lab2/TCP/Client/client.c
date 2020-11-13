#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<netinet/in.h>
#include<unistd.h>
#include<string.h>
#include<arpa/inet.h>

#define MAX 1024
#define PORT 9007

int main(){
	int client_socket, sin_size;
	char buf[MAX], result[MAX];
	int n, operation, num1, num2;
	struct sockaddr_in server_address;

	if((client_socket = socket(AF_INET, SOCK_STREAM, 0)) == -1){
		printf("Socket could not be created.\n");
		exit(EXIT_FAILURE);
	}

	struct sockaddr_in localaddr;
	localaddr.sin_family = AF_INET;
	localaddr.sin_addr.s_addr = inet_addr("192.168.1.4");
	localaddr.sin_port = 0;  // Any local port will do
	bind(client_socket, (struct sockaddr *)&localaddr, sizeof(localaddr));

	server_address.sin_family = AF_INET;
	server_address.sin_port = htons(PORT);
	server_address.sin_addr.s_addr = inet_addr("192.168.1.105");

	sin_size = sizeof(struct sockaddr_in);

	if(connect(client_socket, (struct sockaddr *)&server_address, sin_size) != 0){
        printf("Connection failed as the server is busy.\n");
        exit(EXIT_FAILURE);
    }

	while(1){
		memset(&buf, 0, sizeof(buf));
		n = recv(client_socket, buf, MAX, 0);
		printf("%s", buf);

		scanf("%d", &operation);
		send(client_socket, &operation, sizeof(int), 0);

		if(operation == 5)
			break;
        
		memset(&buf, 0, sizeof(buf));
		n = recv(client_socket, buf, MAX, 0);
		printf("\n%s", buf);

        if(buf[6] == 'a')
            continue;

		scanf("%d", &num1);
		send(client_socket, &num1, sizeof(int), 0);

		memset(&buf, 0, sizeof(buf));
		n = recv(client_socket, buf, MAX, 0);
		printf("%s", buf);

		scanf("%d", &num2);
		send(client_socket, &num2, sizeof(int), 0);
		
		recv(client_socket, result, strlen(result), 0);
		printf("%s", result);
    }
    close(client_socket);

	exit(EXIT_SUCCESS);
}