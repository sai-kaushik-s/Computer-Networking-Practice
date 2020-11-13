#include<stdio.h>
#include<stdlib.h>
#include<sys/socket.h>
#include<sys/types.h>
#include<netinet/in.h>
#include<unistd.h>
#include<string.h>

#define MAX 1024
#define PORT 9007

int main()
{
	int serverSocket, clientSocket, len;
	char X[MAX], S[MAX];
	struct sockaddr_in serverAddr,  clientAddr;
	int n, operation, a, b, output;

	serverSocket = socket(AF_INET, SOCK_STREAM, 0);
	if(serverSocket == -1)
	{
		printf("\nSocket could not be created.\n");
		exit(EXIT_FAILURE);
	}

	serverAddr.sin_family = AF_INET;
	serverAddr.sin_port = htons(PORT);
	serverAddr.sin_addr.s_addr = INADDR_ANY;

	if( bind(serverSocket,  (const struct sockaddr *)&serverAddr, sizeof(serverAddr)) < 0)
	{
		printf("Could not bind to the client.\n");
		exit(EXIT_FAILURE);
	}

	listen(serverSocket, 10);

	len = sizeof(struct sockaddr_in);
	clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddr, &len);
        
    char choice[] = "\n\n'1' for Addition\n'2' for Subtraction\n'3' for Multiplication\n'4' for Division\n'5' for Exit\nEnter your choice: ";
    char Q1[] = "Enter the first number: ";
    char Q2[] = "Enter the second number: ";
    char err[] = "Enter a correct input...\n\n";

	while(1){
		n = send(clientSocket, choice, strlen(choice), 0);
		recv(clientSocket,  &operation, sizeof(int), 0);

		if(operation > 5 || operation < 1){
            send(clientSocket, (char *)err, sizeof(err), 0);
            continue;
		}

        if(operation == 5)
            break;

		n = send(clientSocket, Q1, strlen(Q1), 0);
		recv(clientSocket, &a, sizeof(int), 0);

		n = send(clientSocket, Q2, strlen(Q2), 0);
		recv(clientSocket, &b, sizeof(int), 0);

		switch(operation){
			case 1: output = a + b;
                    strcpy (X, "The sum of the two numbers is: ");
					break;

			case 2: output = a - b;
                    strcpy (X, "The difference of the two numbers is: ");
					break;

			case 3: output = a * b;
                    strcpy (X, "The product of the two numbers is: ");
					break;

			case 4: output = a / b;
                    strcpy (X, "The quotient of the two numbers is: ");
					break;
		}
        sprintf(S, "%d", output);
        char* ANS = strcat(X, S);
		send(clientSocket, ANS, strlen(ANS), 0);
    }
    close(clientSocket);
    close(serverSocket);

	return 0;
}