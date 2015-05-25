#include "my_string.h"


// PRIVATE
// String* string_extend(String* this) {
//     return this;
// }


// PUBLIC
// String string_create(char* chars) {
//     String res;
//     char* copy;
//
//     res.length = strlen(chars);
//
//     copy = (char*) calloc(res.length, 1);
//     memcpy(copy, chars, res.length);
//
//     res.chars = copy;
//
//     return res;
// }
String* string_create(char* chars) {
    String* res;
    char* copy;

    res = (String*) malloc(sizeof(String));

    res->length = strlen(chars);

    copy = (char*) malloc(res->length);
    memcpy(copy, chars, res->length);

    res->chars = copy;

    return res;
}


String* string_append(String* this, String* string) {
    char* new_address;
    __MY_STRING__LENGTH_TYPE new_length;

    new_length  = this->length + string->length;
    new_address = realloc(this->chars, new_length);

    if (new_address != NULL) {
        // new address was taken -> free old address
        if (new_address != this->chars) {
            free(this->chars);
        }
        memcpy(new_address + this->length, string->chars, string->length);
        this->length = new_length;
    }
    else {
        perror("Could not extend memory for string!");
    }

    return this;
}

String* string_replace(String* this, String* find, String* replace) {
    char* pchr;
    char* found;
    __MY_STRING__LENGTH_TYPE index;
    __MY_STRING__LENGTH_TYPE length;

    pchr    = this->chars;
    index   = 0;
    length  = this->length;

    found = strchr(this->chars, find);

    if (found != NULL) {
        
    }
    else {

    }

    // while (strcmp(pchr, find->chars) != 0) {
    //     ++index;
    //     ++pchr;
    // }
    //
    //
    //
    // while (index < length) {
    //     if (*pchr == *find) {
    //         // strcmp
    //     }
    //
    //     ++index;
    //     ++pchr;
    // }
}
