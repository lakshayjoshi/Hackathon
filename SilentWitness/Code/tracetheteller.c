#include <stdio.h> 
#include <string.h> 

int main(void) { 
   char buf[128]; 
   printf("Enter password: "); 
   if (fgets(buf, sizeof(buf), stdin) == NULL) return 0; 
   buf[strcspn(buf, "\n")] = 0; 
   if (strcmp(buf, "secret123") == 0) { 
      printf("CTFEYDSCI{51l3ntW1tn355_success_p455}\n"); 
   } else { 
      printf("wrong password...try again\n"); 
   } 
   return 0; 
}
