
%module norms_and_vecs

%{
#include "norms_and_vecs.h"
%}

%include <std_vector.i>
%include <std_map.i>

namespace std {
    %template(IntVector) vector<int>;
    %template(DoubleVector) vector<double>;
    %template(DoubleVectorVector) vector<vector<double>>;
    %template(DoubleMap) map<double, vector<vector<double>>>;
    %template(IntVectorVector) vector<vector<int>>;
}

%include "norms_and_vecs.h"

%inline %{
    PyObject* vectorToNestedList(std::vector<std::vector<double>> const& v) {
        PyObject* outer_list = PyList_New(v.size());
        for (int i = 0; i < v.size(); ++i) {
            PyObject* inner_list = PyList_New(v[i].size());
            for (int j = 0; j < v[i].size(); ++j) {
                PyList_SET_ITEM(inner_list, j, PyFloat_FromDouble(v[i][j]));
            }
            PyList_SET_ITEM(outer_list, i, inner_list);
        }
        return outer_list;
    }
%}

%typemap(out) std::vector<std::vector<double>> {
    $result = vectorToNestedList($1);
}

%typemap(in) std::vector<std::vector<double>> {
    PyObject* outer_list = PyList_Check($input) ? $input : nullptr;
    if (!outer_list) {
        PyErr_SetString(PyExc_TypeError, "Expected a list of lists.");
        return SWIG_ERROR;
    }

    std::vector<std::vector<double>> result;

    for (Py_ssize_t i = 0; i < PyList_Size(outer_list); ++i) {
        PyObject* inner_list = PyList_GetItem(outer_list, i);
        if (!PyList_Check(inner_list)) {
            PyErr_SetString(PyExc_TypeError, "Expected a list of lists.");
            return SWIG_ERROR;
        }

        std::vector<double> row;
        for (Py_ssize_t j = 0; j < PyList_Size(inner_list); ++j) {
            PyObject* item = PyList_GetItem(inner_list, j);
            if (!PyFloat_Check(item)) {
                PyErr_SetString(PyExc_TypeError, "Expected a list of lists of floats.");
                return SWIG_ERROR;
            }
            row.push_back(PyFloat_AsDouble(item));
        }

        result.push_back(row);
    }

    $1 = result;
}
