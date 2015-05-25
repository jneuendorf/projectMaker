#include "io.hpp"

string* read_textfile(string filename) {

    // ifstream in("templates/index.html");
    // s = new string((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    //
    // return &s


    std::ifstream is ("test.txt", std::ifstream::in);
     if (is) {
        // get length of file:
        is.seekg (0, is.end);
        int length = is.tellg();
        is.seekg (0, is.beg);

        char* buffer = new char[length];

        std::cout << "Reading " << length << " characters... ";
        // read data as a block:
        is.read (buffer,length);

        if (is) {
          std::cout << "all characters read successfully.";
        }
        else {
          std::cout << "error: only " << is.gcount() << " could be read";
        }
        is.close();

        string str = new string(buffer);

        // ...buffer contains the entire file...
        delete[] buffer;

        return &str;
     }

     return NULL;
}
