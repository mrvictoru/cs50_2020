// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

#define MULTIPLIER (37)
#define DICTIONARY "dictionaries/large"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
// hash by first letter of the word
const unsigned int N = 1000;

int dsize = 0;

// Hash table
node *table[N] ;

bool check(const char *word);
unsigned int hash(const char *word);


int main(void){

    unsigned int w2 = hash("caterpillar");
    printf("w2: %i\n",w2);

    unsigned int w1 = hash("caterpillar");
    printf("w1: %i\n",w1);


    bool loaded = load(DICTIONARY);

    if(check("caterpillar")){
        printf("true\n");
    }else{
        printf("false\n");
    }

    unsigned int w3 = hash("caterpillar");
    printf("w1: %i\n",w3);



}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    //hash word
    //for ( ; *word; ++word) *word = tolower(*word);
    printf("word: %s\n",word);
    int path = hash(word);
    printf("path: %i\n",path);

    node *cursor;

    //point cursor to start of hash table
    cursor = table[path];

    //traverse list, use strcasecomp to check
    //use while loop to traverse
    while(strcasecmp(word,cursor->word) != 0){

        if(cursor->next == NULL){
            //printf("check: false\n");
            return false;
        }else{
            cursor = cursor -> next;
        }
    }

    return true;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    // the following has function multiplication method from http://www.cs.yale.edu/homes/aspnes/pinewiki/C(2f)HashTables.html

    unsigned int h = 0;

    //convert word to lower
    //and compute hash
    const int length = strlen(word);
    char* lower = (char*)malloc(length+1);

    for(int i = 0; i < length; i++){
        lower[i] = tolower(word[i]);
        h = h*MULTIPLIER + lower[i];
    }
    /* cast s to unsigned const char * */
    /* this ensures that elements of s will be treated as having values >= 0 */
    //free(lower);

    return h%N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    //open file

    FILE *f;
    f = fopen(dictionary, "r");
    //printf("opening file from %s\n",dictionary);

    if (!f){
        printf("Error opening dictionary in load\n");
        return false;
    }
    char word[LENGTH + 1];
    int link;
    int *p = &dsize;
    // use while loop to scan all the words (until EOF)
    while(fscanf(f, "%s", word) != EOF){
        node *w = malloc(sizeof(node));
        if (w == NULL){
            printf("Memory not allocated to word in load.\n");
            return false;
        }
        //printf("word: %s\n", word);
        strcpy(w->word, word);
        //printf("scanned word: %s\n", w->word);

        //hash
        link = hash(w->word);
        //printf("link :%i\n",link);

        //load onto the list
        if(table[link] == NULL){
            w->next = NULL;
            table[link] = w;
        }else{
            w->next = table[link];
            table[link] = w;
        }
        (*p)++;

    }

    fclose(f);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO

    return dsize;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    node *cursor = malloc(sizeof(node));
    node *temp = malloc (sizeof(node));

    if(cursor == NULL || temp == NULL){
        printf("cursor or temp memory\n");
        return false;
    }

    //to loop through the hash table
    for(int i = 0; i < N; i++){

        cursor = table[i];
        temp = cursor;

        do{
            cursor = cursor->next;
            free(temp);
            temp = cursor;
        }while(cursor->next != NULL);
    }

    free(cursor);
    return true;
}
