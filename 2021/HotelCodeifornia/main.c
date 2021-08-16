#include <openssl/rsa.h>
#include <openssl/crypto.h>
#include <openssl/sha.h>
#include <openssl/pem.h>
#include <openssl/bio.h>
#include <stdio.h>
#include <gmp.h>
#include <stdint.h>
#include <string.h>

int verify_sig(char* data, char* sigin) {

    // read RSA file
    FILE *f = fopen("pubkey.pem", "r");
    fseek(f, 0, SEEK_END);
    size_t size = (size_t)ftell(f);
    rewind(f);

    uint8_t *key = malloc(size);

    fread(key, sizeof(uint8_t), size, f);
    fclose(f);

    // read key
    BIO* bo = BIO_new(BIO_s_mem());
    BIO_write(bo, key, strlen(key));

    EVP_PKEY* pkey = 0;
    RSA* keypair;
    keypair = RSA_new();
    PEM_read_bio_RSA_PUBKEY(bo, &keypair, 0, 0);

    BIO_free(bo);

    uint8_t digest[SHA256_DIGEST_LENGTH];

    SHA256_CTX ctx;

    if (!SHA256_Init(&ctx) || !SHA256_Update(&ctx, data, strlen(data)) || !SHA256_Final(digest, &ctx)) {
        printf("Error verifying signature.");
        free(data);
        return 0;
    }

    mpz_t sig, e, n;
    mpz_inits(sig, e, n, NULL);

    mpz_set_str(sig, sigin, 16);
    mpz_set_str(e, BN_bn2hex(keypair->e), 16);
    mpz_set_str(n, BN_bn2hex(keypair->n), 16);

    mpz_powm(sig, sig, e, n);


    size_t bytes;
    uint8_t* export = mpz_export(NULL, NULL, 0, sizeof(uint8_t), 0, 0, sig);

    mpz_clears(sig, e, n, NULL);

    return strncmp((char*)export, digest, SHA256_DIGEST_LENGTH) == 0;
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("       Welcome to the Hotel Codeifornia\n");
    printf("Esteemed secure code execution service since 1969\n\n");
    printf("If you have a booking, please sign the guestbook below.\n");

    char code[255];
    printf("Enter code> ");
    fgets(code,255,stdin);
    code[strlen(code)-1] = '\0';

    char sig[1024];
    printf("And just sign here please, sir> ");
    fgets(sig,1024,stdin);
    sig[strlen(sig)-1] = '\0';

    if(verify_sig(code, sig)) {
        char exec[300];
        sprintf(exec, "python3 -c '%s'", code);
        printf("\n");
        system(exec);
    } else {
        printf("\nI'm sorry, sir, but you don't appear to be on the guestbook.\n");
    }
}
