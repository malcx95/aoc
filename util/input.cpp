#include "input.hpp"
#include <iostream>
#include <fstream>
#include <streambuf>


std::string util::read_input_string(std::string file_name) {
    std::ifstream stream(file_name);
    std::string str;
    stream.seekg(0, std::ios::end);   
    str.reserve(stream.tellg());
    stream.seekg(0, std::ios::beg);

    str.assign((std::istreambuf_iterator<char>(stream)),
            std::istreambuf_iterator<char>());
    return str;
}


void util::read_file_lines(std::vector<std::string>& res,
        std::string file_name) {
    std::ifstream stream(file_name);
    std::string line;
    if (stream.is_open()) {
        while (std::getline(stream, line)) {
            res.push_back(line);
        }
        stream.close();
    } else {
        std::cout << "Unable to open file " << file_name << std::endl;
    }
}

void util::read_inputs(std::vector<int>& res, std::string file_name) {
    util::read_inputs<int>(res, file_name, [](const std::string& x) -> int
            { return std::stoi(x); });
}

void util::read_inputs(std::vector<double>& res, std::string file_name) {
    util::read_inputs<double>(res, file_name, [](const std::string& x) -> double 
            { return std::stod(x); });
}

