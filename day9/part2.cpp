#include <vector>
#include <deque>
#include <list>
#include <iostream>
#include <map>

using namespace std;

const long NUM_PLAYERS = 464;
const long HIGHEST = 71730*100;


int main() {
    
    map<long,long> scores;
    
    for (long i = 0; i < NUM_PLAYERS; ++i) {
        scores[i] = 0;
    }

    long current_marble_index = 0;
    long curr_player = 0;
    list<long> board;
    board.push_back(0);
    list<long>::iterator curr_pos = board.begin();
    long curr = 1;

    while (curr <= HIGHEST) {
        if ((curr % 23) == 0) {
            scores[curr_player + 1] += curr;
            long rem_index;
            if (current_marble_index - 7 < 0) {
                long t = 7 - current_marble_index;
                rem_index = board.size() - t;
                curr_pos = board.end();
                advance(curr_pos, -t);
            } else {
                rem_index = (current_marble_index - 7) % board.size();
                advance(curr_pos, -7);
            }
            long marble = *curr_pos;//board[rem_index];

            board.erase(curr_pos);
            advance(curr_pos, -1);
            advance(curr_pos, 1);
            current_marble_index = rem_index;
            scores[curr_player + 1] += marble;
        } else {
            if (current_marble_index == (board.size() - 1)) {
                curr_pos = board.begin();
                advance(curr_pos, 1);
                board.insert(curr_pos, curr);
                advance(curr_pos, -1);
                current_marble_index = 1;
            } else {
                advance(curr_pos, 2);
                board.insert(curr_pos, curr);
                advance(curr_pos, -1);
                current_marble_index = current_marble_index + 2;
            }
        }
        curr++;
        curr_player = ((curr_player + 1) % NUM_PLAYERS);
    }
    long max = 0;
    for (auto& x : scores) {
        if (x.second > max) {
            max = x.second;
        }
    }
    cout << max << endl;

}
