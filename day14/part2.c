#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

const int PATTERN[6] = {
    0, 8, 4, 6, 0, 1
};

struct llist {
    int data;
    struct llist* next;
};

typedef struct llist llist_t;

void push_back(int* last, int el) {
    for (int i = 0; i < 6; ++i) {
        last[i] = last[i+1];
    }
    last[6] = el;
}

bool matches(int* last) {
    bool matched = true;
    for (int i = 0; i < 6; ++i) {
        if (last[i] != PATTERN[i]) {
            matched = false;
            break;
        }
    }
    if (matched) {
        return true;
    } else {
        for (int i = 1; i < 7; ++i) {
            if (last[i] != PATTERN[i-1]) {
                return false;
            }
        }
        return true;
    }
}

int main() {

    llist_t* curr_1 = malloc(sizeof(llist_t));
    llist_t* curr_2 = malloc(sizeof(llist_t));

    int last[7] = {-1, -1, -1, -1, -1, -1, -1};

    curr_1->data = 3;
    curr_2->data = 7;

    curr_1->next = curr_2;
    curr_2->next = curr_1;

    llist_t* tail = curr_2;

    unsigned long num_created = 2;
    
    while (1) {
        int b1 = curr_1->data;
        int b2 = curr_2->data;

        int dsum = b1 + b2;
        int unit = dsum % 10;
        int ten = dsum / 10;

        int digits[2] = {ten, unit};

        for (int i = 0; i < 2; ++i) {
            int digit = digits[i];
            if (i == 0 && digit == 0) {
                continue;
            }
            num_created++;
            push_back(last, digit);
            llist_t* new_node = malloc(sizeof(llist_t));
            new_node->data = digit;
            llist_t* old_next = tail->next;
            tail->next = new_node;
            new_node->next = old_next;
            tail = new_node;
        }

        for (int i = 0; i < b1 + 1; ++i) {
            curr_1 = curr_1->next;
        }
        
        for (int i = 0; i < b2 + 1; ++i) {
            curr_2 = curr_2->next;
        }

        if (num_created - 6 > 0) {
            if (matches(last)) {
                printf("Result: %i\n", num_created - 6);
                break;
            }
        }
    }
    return 0;
}

