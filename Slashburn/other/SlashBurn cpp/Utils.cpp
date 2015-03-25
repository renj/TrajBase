#include "StdAfx.h"
#include "Utils.h"
#include <sstream>

#include <io.h>
#include <direct.h>

Utils::Utils(void)
{
}

Utils::~Utils(void)
{
}


FILE * Utils::openFile(const char *fileName, char *mode)
{
	FILE *file = fopen( fileName, mode) ;
	//if( fopen_s( &file, fileName, mode) != 0 )
	if( file == NULL )
	{
		cerr << "Cannot open file:" << fileName << endl ;
		exit(-1);
	}
	return file ;
}

string Utils::toStr(const int val)
{
	stringstream retStr ;
	retStr << val ;

	string value ;
	retStr >> value ;
	return value;
}

bool Utils::fileExists(string fileName)
{
	if ( _access( fileName.c_str(),6)==-1)
    {
		return false ;
    }
	return true ;
}
//@analyze the path
string Utils::checkPath(string path)
{
	if( path.length() == 0)
		return NULL ;

	char tail = path[ path.length() - 1] ;
	if( tail != '\\' && tail != '/')
	{
		path += "/" ;
	}
	if ( _access(path.c_str(),6)==-1)
    {
		_mkdir(path.c_str());
    }
	return path ;
}

//@function: New an array of size count and initiate the array from 0 by step
int * Utils::createIncreamental(const int count, const int from, const int step )
{
	int * ret = new int[ count] ;

	int cur = from ;
	for(int i = 0; i < count; ++i, cur += step)
	{
		ret[ i] = cur ;
	}
	return ret ;
}

int Utils::maxValPos(int* buffer, int count)
{
	int maxPos = 0 ;
	int maxVal = buffer[0] ;
	for(int i = 0; i < count; ++i)
	{
		buffer[i] > maxVal ? maxVal = buffer[i], maxPos = i : true ;
	}
	return maxPos ;
}

int Utils::toInt(char *arg)
{
	stringstream retStr( arg) ;
	int ret = 0 ;
	retStr >> ret ;
	return ret ;
}