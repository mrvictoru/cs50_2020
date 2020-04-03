#include <stdio.h>
#include <stdlib.h>


#define BLOCK 512


int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: recover [filename]\n");
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (!f){
        printf("error opening file\n");
        return 1;
    }

    int name_count = 0;

    char *filename = malloc(sizeof(char)*7);

    FILE *img = NULL;

    int size = sizeof(unsigned char);

    unsigned char *buffer = malloc(size*BLOCK);

    //read through block until it is smaller than block size
    while(fread(buffer,BLOCK,1,f) == 1){


        //check if it is start of jpg
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0){

            //if it is not the first img, close previous img
            if (name_count > 0){
                fclose(img);
            }

            //open img with name count
            sprintf(filename,"%03i.jpg", name_count);
            img = fopen(filename, "w");


            //if it fails to open
            if (img == NULL){
                fprintf(stderr, "Error with %s \n", filename);
                return 3;
            }
            //count up with name
            name_count++;
        }

        //if img open with no problem, write block
        if (img != NULL){
            fwrite(buffer,BLOCK,1,img);
        }


    }
    free(buffer);
    free(filename);
    fclose(f);
    fclose(img);
}
