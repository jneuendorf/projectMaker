#ifndef __MY_STRING__
#define __MY_STRING__ 1

#include "libs.h"

// determines max size of string
#define __MY_STRING__LENGTH_TYPE unsigned short




typedef struct String String;

struct String {
    // PRIVATE 'INSTANCE' PROPERTIES
    // __MY_STRING__LENGTH_TYPE    _free_space;

    // PUBLIC 'INSTANCE' PROPERTIES
    __MY_STRING__LENGTH_TYPE    length;
    char*                       chars;

    // 'INSTANCE' METHODS
    // String                      (*append)(String*, String*);
};




struct StringClass {
    String  (*new)(char*);
} StringClass;





String* string_create(char* chars);

String* string_append(String* this, String* string);

String* string_replace(String* this, String* find, String* replace);

#endif
