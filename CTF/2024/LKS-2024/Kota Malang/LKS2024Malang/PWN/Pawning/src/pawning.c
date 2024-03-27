#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <time.h>

#define BUFFSIZE 16
int gift;

int get_random(){
	srand(time(0));
	return rand() % 417;
}

void helper()
{
		__asm__("popq %rdi\n\t"
			"ret\n\t");
}

int setup()
{


	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}

int game(){
	int guess = get_random();
	int res = 0;
	char buf[BUFFSIZE];
	printf("Guess the number? ");
	fgets(buf, BUFFSIZE, stdin);
	int ans = atoi(buf);
	if(!ans){
		printf("You wrong\n");
		exit(0);
	}
	else{
		if(ans == guess){
			printf("Congrats! Not bad!\n");
			res = 1;
		}
		else{
			printf("Oops soory, try again later\n");
		}
	}
	return res;
}

int main(int argc, char const *argv[])
{
	setup();
	char buf[0x100];
	int res = game();
	if(res){
		printf("Okay, You win, i will give you this: %p\n", &gift);
		printf("Any feedback? ");
		gets(buf);
	}
	else{
		printf("You lose! can you give some feedback please? ");
		fgets(buf, 0x100, stdin);
		printf("Thanks for your feedback, a loss is still a loss though xD\n");
	}
	printf("See yaa\n");
	return 0;
}