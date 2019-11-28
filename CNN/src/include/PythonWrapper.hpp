/** File name: PythonWrapper.hpp
 *  Author(s): Milosz Filus
 *
 * History of changes
 *
 * Version      Author      Change
 * v1           Milosz      Initial
 * ***********************************
**/


#ifndef __PYTHON_WRAPPER_HPP__
#define __PYTHON_WRAPPRE_HPP__
#include <boost/python/tuple.hpp>


boost::python::tuple cnn(boost::python::object& imagePath, boost::python::dict& optionDict);


#endif
