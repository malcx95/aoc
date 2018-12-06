#ifndef STRINGEXTRA_HPP
#define STRINGEXTRA_HPP

#include <tuple>
#include <string>
#include <iostream>

namespace util {

template<class T, class... Ts>
std::tuple<T, Ts...> string_split(std::string& delim, std::string& string);

}

// -------------------------------------------------------
// Template nonsense
template<typename T, typename... Ts>
std::tuple<T, Ts...> string_split_help(std::string& delim, std::string& string);

template<typename T>
std::tuple<T> string_split_help(std::string& string);

template<typename T, typename... Ts>
std::tuple<T, Ts...> util::string_split(std::string& delim, std::string& string) {
    return string_split_help<T, Ts...>(delim, string);
}

template<typename T, typename... Ts>
std::tuple<T, Ts...> string_split_help(std::string& delim, std::string& string) {
    size_t i = string.find(delim);
    if (i == std::string::npos) {
        std::cerr << "Could not find delimiter " 
            << delim << " in " << string << std::endl;
    }

    std::string first = string.substr(0, i);
    std::string rest = string.substr(i + delim.length(), string.length());

    std::tuple<T> first_tuple = string_split_help<T>(first);
    std::tuple<Ts...> second_tuple = string_split_help<Ts...>(delim, rest);
    return std::tuple_cat<T, Ts...>(first_tuple, second_tuple);
}

template <>
std::tuple<int> string_split_help(std::string& string) {
    return std::make_tuple<int>(std::stoi(string));
}

template <>
std::tuple<double> string_split_help(std::string& string) {
    return std::make_tuple<double>(std::stod(string));
}

template <>
std::tuple<std::string> string_split_help(std::string& string) {
    return std::make_tuple<std::string>(std::string(string));
}

#endif /* ifndef STRINGEXTRA_HPP */
