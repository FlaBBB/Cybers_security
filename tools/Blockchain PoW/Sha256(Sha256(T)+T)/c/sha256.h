#include <stdio.h>
#include <string.h>
#include "sha256-x86.h"

struct init_sha256_state
{
    uint32_t state[8];
    uint32_t length;
    uint8_t  buffer[64];
    uint8_t  buffer_length;
};

void init_sha256(struct init_sha256_state* state)
{
    state->state[0] = 0x6a09e667;
    state->state[1] = 0xbb67ae85;
    state->state[2] = 0x3c6ef372;
    state->state[3] = 0xa54ff53a;
    state->state[4] = 0x510e527f;
    state->state[5] = 0x9b05688c;
    state->state[6] = 0x1f83d9ab;
    state->state[7] = 0x5be0cd19;
    state->length = 0;
    state->buffer_length = 0;
}

void update_sha256(struct init_sha256_state* state, const uint8_t* data, uint32_t length)
{
    while (length > 0) {
        uint32_t copy_length = 64 - state->buffer_length;
        if (copy_length > length) {
            copy_length = length;
        }
        memcpy(state->buffer + state->buffer_length, data, copy_length);
        state->buffer_length += copy_length;
        data += copy_length;
        length -= copy_length;
        if (state->buffer_length == 64) {
            sha256_process_x86(state->state, state->buffer, 64);
            state->length += 64;
            state->buffer_length = 0;
        }
    }
}

void finish_sha256(struct init_sha256_state* state, uint8_t* hash)
{
    uint64_t bit_length = state->length * 8 + state->buffer_length * 8;
    state->buffer[state->buffer_length++] = 0x80;
    if (state->buffer_length > 56) {
        memset(state->buffer + state->buffer_length, 0, 64 - state->buffer_length);
        sha256_process_x86(state->state, state->buffer, 64);
        state->buffer_length = 0;
    }
    memset(state->buffer + state->buffer_length, 0, 56 - state->buffer_length);
    state->buffer_length = 56;
    state->buffer[63] = (bit_length >> 0) & 0xFF;
    state->buffer[62] = (bit_length >> 8) & 0xFF;
    state->buffer[61] = (bit_length >> 16) & 0xFF;
    state->buffer[60] = (bit_length >> 24) & 0xFF;
    state->buffer[59] = (bit_length >> 32) & 0xFF;
    state->buffer[58] = (bit_length >> 40) & 0xFF;
    state->buffer[57] = (bit_length >> 48) & 0xFF;
    state->buffer[56] = (bit_length >> 56) & 0xFF;
    sha256_process_x86(state->state, state->buffer, 64);
    for (int i = 0; i < 8; i++) {
        hash[i * 4 + 0] = (state->state[i] >> 24) & 0xFF;
        hash[i * 4 + 1] = (state->state[i] >> 16) & 0xFF;
        hash[i * 4 + 2] = (state->state[i] >> 8) & 0xFF;
        hash[i * 4 + 3] = (state->state[i] >> 0) & 0xFF;
    }
}