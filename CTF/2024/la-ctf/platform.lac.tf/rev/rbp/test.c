#include <unistd.h>
#include <stdio.h>

void my_function() {
    printf("Hello, world!\n");
}

int main() {
    // Get the page size
    long page_size = getpagesize();

    // Calculate the page-aligned address
    void *addr = (void *)((long)my_function & ~(page_size - 1));

    // Change the memory protections
    if (mprotect(addr, page_size, 3) == -1) { // 3 = PROT_READ | PROT_WRITE
        perror("mprotect");
        return 1;
    }

    my_function(); // Should segfault

    return 0;
}
