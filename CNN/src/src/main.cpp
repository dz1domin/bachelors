
/** File name: main.cpp
 *  Author(s): Milosz Filus
 *
 * History of changes
 *
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/

//file made only for testing, won't be compiled and assembled to .dll because of _WINDLL define

/**
TODO: ADD LINUX DEFINE
*/

#ifndef _WINDLL

//

#include <iostream>
#include <sstream>
#include "CNNBlurDetector.hpp"
#include <boost/any.hpp>
#include <boost/property_tree/json_parser.hpp>



int main(int argc, char* argv[])
{


	std::cout << "You can test module here" << std::endl;



	return 0;
}

#endif