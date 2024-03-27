#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void spin_words(const char *sentence, char *result)
{
    const char *cur = sentence;
    int initial_idx = 0;
    int len_word = 0;
    int i = 0;
    int state = -1;

    while (*cur != 0)
    {
        if (*cur == ' ')
        {
            state = 0;
            if (len_word >= 5)
            {
                state = 1;
            }
            for (int j = initial_idx; initial_idx < i; initial_idx++)
            {
                result[initial_idx] = sentence[(initial_idx * (state * -2 + 1)) + (j + i - 1) * state ];
            }
            result[initial_idx] = ' ';
            initial_idx++;
            state = -1;
            len_word = 0;
        }
        else
        {
            len_word++;
        }
        i++;
        cur++;
    }
    state = 0;
    if (len_word >= 5)
    {
        state = 1;
    }
    for (int j = initial_idx; initial_idx < i; initial_idx++)
    {
        result[initial_idx] = sentence[(initial_idx * (state * -2 + 1)) + (j + i - 1) * state ];
    }
    result[i] = 0;
}

int main()
{
    char result[100];
    const char *input_sentence = "Hey Fellow Warrirors Hey Fellow Warrirors Hey Fellow Warrirors Hey Fellow Warrirors";
    clock_t start_time, end_time;
    double cpu_time_used;

    start_time = clock();
    for (int i = 0; i < 1000000; i++)
        spin_words(input_sentence, result);
    end_time = clock();
    cpu_time_used = ((double) (end_time - start_time)) / CLOCKS_PER_SEC;

    printf("Original Sentence: %s\n", input_sentence);
    printf("Spun Sentence: %s\n", result);
    printf("Time taken: %f seconds\n", cpu_time_used);

    return 0;
}