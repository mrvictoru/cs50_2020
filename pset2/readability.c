#include <stdio.h>
#include <ctype.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int main(void){
    int letters = 0, words = 0, sentences = 0, L = 0, S = 0, index = 0;
    string sentence = get_string("Text: ");

    for(int i = 0; i < strlen(sentence); i++){
        if(isalpha(sentence[i])){
            letters ++;
        }
        if(i == 0){
            words ++;
        }else{
            if(isalpha(sentence[i]) && (isspace(sentence[i-1]) || sentence[i-1] == '"' || sentence[i-1] == (char)(39))){
            words ++;
            }
        }
        if((sentence[i] == '!' || sentence[i] == '?' || sentence[i] == '.') && (isspace(sentence[i+1]) || sentence[i+1] == '\0')){
            sentences ++;
        }

    }
    //printf("letters: %i \n", letters);
    //printf("words: %i \n", words);
    //printf("sentences: %i \n", sentences);

    if (words <= 100){
        L = (float) letters/words*100;
        S = (float) sentences/words*100;
    }else{
        L = letters/(words/100);
        S = sentences/(words/100);
    }

    index = (int) round(0.0588 * (float) L - 0.296 * (float) S - 15.8);

    //printf("L: %i ", L);
    //printf("S: %i ", S);
    //printf("index: %i \n", index);
    if (index > 16){
        printf("Grade 16+\n");
    }else if (index <= 1){
        printf("Before Grade 1\n");
    }else{
        printf("Grade %i\n", index);
    }

}



