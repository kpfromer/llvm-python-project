#include <stdio.h>
#include <stdlib.h>

int input() {
      int i;
  int parsed = scanf("%d", &i);
  if(parsed==0){
    printf("Unable to read input (expected integer)\n");
    exit(-1);
  }
  return i;
}

void print(int value) {
    printf("%d\n", value);
}