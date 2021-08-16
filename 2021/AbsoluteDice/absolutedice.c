#include "stdio.h"
#include "stdlib.h"

int _main(char *seedFile)
{
    struct data
    {
        int i;
        int computer;
        int correctGuesses;
        int guess;
        int seed;
        int guesshistory[32];
        char *sf;
    };

    struct data d = {.i = 0, .sf = seedFile};

    //char* sf = seedFile;

    printf("Welcome to the final boss fight of my new indie game, Solid Rook. Your goal - predict the same number as the
 final boss, Absolute Dice, 50 times in a row; she'll pick between 0 and 20.\n\n");

    //printf("Your turn, slick.\n");
    //printf("Maybe this turkey'll bring us some luck!\n");
    //printf("Baby needs a new pair of shoes!\n");

    while (1) {
        d.i = d.i + 1;
        // printf("%d", (int)sf);
        FILE *urandom = fopen(d.sf, "r");

        fread(&(d.seed), sizeof(int), 1, urandom);
        srand(d.seed);

        printf("Enter your guess> ");
        scanf("%d", &(d.guess));

        d.computer = rand() % 21;

        (d.guesshistory)[d.i % 33] = d.guess;

        if (d.guess == d.computer)
        {
            d.correctGuesses += 1;
            printf("Absolute Dice shrieks as your needle strikes a critical hit. (%d/50)\n", d.correctGuesses);
            if (d.correctGuesses > 50)
            {
                printf("Absolute Dice shrieks as you take her down with a final hit.");
                FILE *fptr;
                char c;

                fptr = fopen("flag.txt", "r");

                c = fgetc(fptr);
                while (c != EOF)
                {
                    printf("%c", c);
                    c = fgetc(fptr);
                }

                fclose(fptr);
            }
        }
        else
        {
            d.correctGuesses = 0;
            printf("Absolute Dice scores a hit on you! (She had %d, you said %d)\n", d.computer, d.guess);
        }
    }
}

int main()
{
    char urandom[] = "/dev/urandom";
    return _main((char *)(&urandom));
}
