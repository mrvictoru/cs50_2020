#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int main (int argc, string argv[]){

    if (argc != 2){
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0; i < strlen(argv[1]); i++){
        if(isalpha(argv[1][i])){
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    int key = atoi(argv[1]);

    //printf("key: %i\n", key);


    string ptext = get_string("plaintext: ");
    //printf("length: %i", (int)strlen(ptext));


    printf("ciphertext: ");
    char text;

    for (int j = 0; j < strlen(ptext); j++){
        if(isupper(ptext[j])){
            text = (((ptext[j]-65) + key)%26)+65;

            printf("%c", text);

        }else if (islower(ptext[j])){
            text = (((ptext[j]-97) + key)%26)+97;

            printf("%c", text);
        }else{
            printf("%c", ptext[j]);

        }
    }

    printf("\n");


    //return 0;
}