#include "../util/input.hpp"
#include "../util/stringextra.hpp"
#include <string>
#include <tuple>
#include <iostream>

int main() {
    // std::vector<int> input;

    // util::read_inputs(input, "input2.txt");
    
    std::string e = "1:2.2";
    std::string delim = ":";
    
    std::tuple<int, double> t = 
        util::string_split<int, double>(delim, e);


}
