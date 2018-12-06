#ifndef INPUT_H
#define INPUT_H

#include <string>
#include <vector>
#include <functional>
#include <tuple>

namespace util {

/*
 * Reads input from file name and returns everything as a string.
 */
std::string read_input_string(std::string file_name);

/*
 * Reads each string line of a file and puts it in a given vector.
 */
void read_file_lines(std::vector<std::string>& res, std::string file_name);

/*
 * Reads input from file where each entry is on it's own line and 
 * casts it to the given type.
 */
template<typename T>
void read_inputs(std::vector<T>& res, std::string file_name, std::function<T(const std::string&)> conv_fun);

/*
 * Reads input from file where each entry is on it's own line and 
 * casts it to int.
 */
void read_inputs(std::vector<int>& res, std::string file_name);

/*
 * Reads input from file where each entry is on it's own line and 
 * casts it to double.
 */
void read_inputs(std::vector<double>& res, std::string file_name);

/*
 * Reads input from file where each entry is on it's own line and 
 * casts it to tuples.
 */
template <class... Ts>
void read_inputs(std::vector<std::tuple<Ts...>>& res, std::string file_name);

}


template<typename T>
void util::read_inputs(std::vector<T>& res, std::string file_name, std::function<T(const std::string&)> conv_fun) {
    std::vector<std::string> lines;
    util::read_file_lines(lines, file_name);
    
    for (auto& line : lines) {
        res.push_back(conv_fun(line));
    }
}


#endif /* ifndef INPUT_H */
