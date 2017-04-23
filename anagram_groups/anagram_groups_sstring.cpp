#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <vector>
#include <iterator>

/* To match the Python version, I provide Mergesort just in case it's not allowed to use the built-in std::sort algorithm (or std::mergesort) 
Otherwise, just use "sorted" as provided further below.

To avoid making this file too big for what it is, I didn't create a class this time, and I just run it through a wordlist file as a proof of concept. Otherwise it would end up being 
mostly boilerplate instead of solving the actual problem.
*/


template<class Iter>
void merge(Iter begin, Iter midpoint, Iter end)
{
	using value_type = typename std::iterator_traits<Iter>::value_type;
	std::vector<value_type> tmp(std::make_move_iterator(begin), std::make_move_iterator(end));

	auto cursorLeftHalf = &tmp.front();
	auto cursorRightHalf = &tmp.front() + (midpoint - begin);

	auto const endLeftHalf = cursorRightHalf;
	auto const endRightHalf = std::next(&tmp.back());

	while (cursorLeftHalf != endLeftHalf && cursorRightHalf != endRightHalf)
	{
		if (*cursorRightHalf < *cursorLeftHalf)
		{
			*begin++ = std::move(*cursorRightHalf++);
		}
		else 
		{
			*begin++ = std::move(*cursorLeftHalf++);
		}
	}

	while (cursorLeftHalf != endLeftHalf)
	{
		*begin++ = std::move(*cursorLeftHalf++);
	}

	while (cursorRightHalf != endRightHalf)
	{
		*begin++ = std::move(*cursorRightHalf++);
	}
}

template<class Iter>
void mergesort(Iter begin, Iter end)
{
	if (begin != end) 
	{
		auto const midpoint = begin + (end - begin) / 2;
		if (end - midpoint > 1) // cannot be made tail-recursive anyway
		{
			mergesort(begin, midpoint);
			mergesort(midpoint, end);
		}
		merge(begin, midpoint, end);
	}
}

//--------------------------------

std::string sorted(const std::string& s)
{
	std::string output(s);

	//std::sort(output.begin(), output.end()); // remove comment and comment the following line to use the built-in "sort" instead
	mergesort(output.begin(), output.end());
	return output;
}

int main(void)
{
	//  unordered_map (C++11) as a hash map - indexed by anagram id 
	std::unordered_map<std::string, std::vector< std::string >> word_dic;

	//std::ifstream input_f("corncob_lowercase.txt");
	//std::string init("toes archaism charisma caiman ablest bleats stable tables maniac baker brake break");
    std::stringstream input_f ("toes archaism charisma caiman ablest bleats stable tables maniac baker brake break");
    input_f.seekp( input_f.str().size() );
    input_f << " nothing" << " stoe" << " abad" << " daba";
    std::cout << input_f.str() << std::endl;
    
//	for (std::string line; std::getline( input_f, line ); )
	for (std::string line; input_f >> line ; )
	{
		word_dic[sorted(line)].push_back(line);
	}

//	input_f.close();

	// Iterate and print keys and values of unordered_map
	for (const auto& n : word_dic)
	{
		if (n.second.size() > 1) // same rationale as in Python, only show groups with 2+ words
		{
			std::cout << "Key:[" << n.first << "] Anagrams:[";
			
			for (const auto& i : n.second)
			{
				std::cout << " \"" << i << "\" ";
			}
			
			/* this range iterator loop is equivalent to this: 
			>>>>>
			std::vector< std::string >::const_iterator it = n.second.begin();
			while (it != n.second.end())
			{
				std::cout << " \"" << *it << "\" ";
				++it;
			}
			<<<<<
			*/
			std::cout << "]\n";

		}
	}


	return 0;
}