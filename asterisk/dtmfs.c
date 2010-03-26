#include <stdio.h>
#include <stdlib.h>


#define DKEY_LEN 2

struct dkey {
	char key[DKEY_LEN+1];
	struct dkey *last;
};


int dkey_push(struct dkey **p, char *key) {
	struct dkey *el;
	el = malloc(sizeof(*el));	
	if (!el) {
		return 0;
	}
	snprintf(el->key, DKEY_LEN+1, "%s", key);
	el->last = *p;
	*p = el;
	return 1;
}


int dkey_pop(struct dkey **p, char *key) {
	struct dkey *tmp;

	if(!*p) return 0;	
	tmp = (*p)->last;
	snprintf(key, DKEY_LEN+1, "%s", (*p)->key);
	free(*p);
	*p = tmp;
	return 1;
}

int main(int argc, char *argv[]) {

	struct dkey *la = NULL;
	struct dkey *lb = NULL;

	dkey_push(&la, "A1");	
	dkey_push(&la, "A2");	
	dkey_push(&la, "A3");	
	dkey_push(&lb, "B1");	
	dkey_push(&lb, "B2");	
	dkey_push(&lb, "B3");	

	char *k;
	while (dkey_pop(&la, k)) {
		if (!k) {
			break;
		}
		printf("A => %s\n", k);
	}
	while (dkey_pop(&lb, k)) {
		if (!k) {
			break;
		}
		printf("B => %s\n", k);
	}
	return 0;
}

