#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>
#include "aes.h"

int main() {
    FILE *fp;
    uint8_t* scratch = 0;
    
    char buff[64];
    fp = fopen("/home/ractf/flag.txt", "r");
    fgets(buff, 64, fp);
    fclose(fp);

    uint8_t keyfile[16];
    fp = fopen("/home/ractf/keyfile", "r");
    fread(keyfile, 16, 1, fp);
    fclose(fp);
    
    size_t padlen = ((strlen(buff)-1)|15)+1;

    scratch = (uint8_t*) malloc(1<<20);
    if (scratch != NULL) {
        strcpy(scratch, buff);
        
        struct AES_ctx ctx;
        struct timeval time;
        uint8_t key[16];
        uint8_t iv[16];
        gettimeofday(&time, NULL);
        srand((time.tv_sec*1000000) + time.tv_usec);
        for (int i = 0; i < 16; i++) {
            key[i] = (rand() % 256) ^ keyfile[i];
        }
        for (int i = 0; i < 16; i++) {
            iv[i] = rand() % 256;
        }
        for (int i = strlen(buff); i < padlen; i++) {
            scratch[i] = 0;
        }

        AES_init_ctx_iv(&ctx, key, iv);
        AES_CBC_encrypt_buffer(&ctx, scratch, padlen);
        memcpy(buff, scratch, padlen);
    }
    free(scratch);

    for (int i = 0; i < padlen; ++i) {
        printf("%02x", (uint8_t)buff[i]);
    }
    printf("\n");

    return 0;
}