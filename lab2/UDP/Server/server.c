#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 9009
#define MAX 1024

int add(int a, int b){
    return a + b;
}

int sub(int a, int b){
    return a - b;
}

int mul(int a, int b){
    return a * b;
}

int divi(int a, int b){
    return a / b;
}

int main() {
	int serverSocket;
	char input[3], A1[MAX], A2[MAX], S[MAX], X[MAX], recvMsg[MAX];
    int a, b, output;
	struct sockaddr_in serverAddr, clientAddr;
	
	if ((serverSocket = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
		printf("Socket could not be created.\n");
		exit(EXIT_FAILURE);
	}
	
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = INADDR_ANY;
	serverAddr.sin_port = htons(PORT);
	
	if (bind(serverSocket, (const struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0){
		printf("Could not bind.\n");
		exit(EXIT_FAILURE);
	}
	
	int n;
    socklen_t len = sizeof(serverAddr);
    int (*fun_ptr_arr[])(int, int) = {add, sub, mul, divi};

    n = recvfrom(serverSocket, (char *)recvMsg, sizeof(recvMsg), 0, (struct sockaddr *) &clientAddr, &len);
    printf("Client: %s\n", recvMsg);
    char choice[] = "'add' for Addition\n'sub' for Subtraction\n'mul' for Multiplication\n'div' for Division\n'out' for Exit\nEnter your choice: ";
    char Q1[] = "Enter the first number: ";
    char Q2[] = "Enter the second number: ";

    while(1){
        sendto(serverSocket, (char *)choice, sizeof(choice), 0, (struct sockaddr *) &clientAddr, sizeof(clientAddr));
        n = recvfrom(serverSocket, (char *)input, sizeof(input), 0, (struct sockaddr *) &clientAddr, &len);

        if(!strncmp(input, "add", 3) || !strncmp(input, "sub", 3) || !strncmp(input, "mul", 3) || !strncmp(input, "div", 3)){
            char err[MAX];
            strcpy(err, "Enter a correct input...");
            sendto(serverSocket, (char *)err, sizeof(err), 0, (struct sockaddr *) &clientAddr, sizeof(clientAddr));
            continue;
        }

        sendto(serverSocket, (char *)Q1, sizeof(Q1), 0, (struct sockaddr *) &clientAddr, sizeof(clientAddr));
        n = recvfrom(serverSocket, (char *)A1, sizeof(A1), 0, (struct sockaddr *) &clientAddr, &len);
        a = atoi(A1);

        sendto(serverSocket, (char *)Q2, sizeof(Q2), 0, (struct sockaddr *) &clientAddr, sizeof(clientAddr));
        n = recvfrom(serverSocket, (char *)A2, sizeof(A2), 0, (struct sockaddr *) &clientAddr, &len);
        b = atoi(A2);

        switch (input[0]){
            case 'a': 
                n = 0;
                strcpy (X, "The sum of the two numbers is: ");
                break;
            case 's': 
                n = 1;
                strcpy (X, "The difference of the two numbers is: ");
                break;
            case 'm':
                n = 2;
                strcpy (X, "The product of the two numbers is: ");
                break;
            case 'd':
                n = 3;
                strcpy (X, "The quotient of the two numbers is: ");
                break;
        }
        output = (*fun_ptr_arr[n])(a, b);
        sprintf(S, "%d", output);
        char* ANS = strcat(X, S);
        sendto(serverSocket, (char *)ANS, strlen(ANS), 0, (struct sockaddr *) &clientAddr, sizeof(clientAddr));
	}

	close(serverSocket);
	return 0;
}