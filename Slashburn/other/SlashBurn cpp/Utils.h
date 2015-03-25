#ifndef _UTILS_H_

#define _UTILS_H_


#include<iostream>
#include<string>

using namespace std;

class Utils
{
public:
	Utils(void);
	~Utils(void);

public:
	//@function: Open file, if unsuccesful, exit
	static FILE * openFile(const char *fileName, char *mode) ;

	//@function: Convert an integer to string
	static string toStr(const int val);
	
	//@function: check if a file exists
	static bool fileExists(string fileName);

	//@function: analyze the path
	static string checkPath(string path);

	//@function: New an array of size count and initiate the array from 0 by step
	static int * createIncreamental(const int count, const int from = 0, const int step = 1);

	//@function: Find the maximum value position
	static int maxValPos(int* buffer, int count);

	static int toInt(char *arg);

	//@function
	template<class T>
	static void sort( T *val, const int count, bool ascend);
	template<class T,class T2>
	static void sort( T *val, T2 *val2, const int count, bool ascend);
	template<class T,class T2,class T3>
	static void sort( T *val, T2 *val2,T3 *val3,const int count, bool ascend);
	template<class T>
	static int sortPos( T *val, const int count, bool ascend) ;
	//@function
	template<class T>
	static inline void swap(T * buffer, const int l, const int r)
	{
		T tmp = buffer[ l] ;
		buffer[ l] = buffer[ r] ;
		buffer[ r] = tmp ;
	}
};

template<class T>
void Utils::sort( T *val, const int count, bool ascend)
{
	for(int i =0; i < count; ++i)
	{
		int pos = sortPos( val + i, count - i, ascend) + i ;
		swap( val, pos, i) ;
	}
}
template<class T,class T2>
void Utils::sort( T *val, T2 *val2, const int count, bool ascend)
{
	for(int i =0; i < count; ++i)
	{
		int pos = sortPos( val + i, count - i, ascend) + i ;
		swap( val, pos, i) ;
		swap( val2, pos, i) ;
	}
}
template<class T,class T2,class T3>
void Utils::sort( T *val, T2 *val2,T3 *val3,const int count, bool ascend)
{
	for(int i =0; i < count; ++i)
	{
		int pos = sortPos( val + i, count - i, ascend) + i ;
		swap( val, pos, i) ;
		swap( val2, pos, i) ;
		swap( val3, pos, i) ;
	}
}

template<class T>
int Utils::sortPos( T *val, const int count, bool ascend)
{
	T theVal = val[ 0] ;
	int pos = 0 ;
	for(int i = 0; i < count; ++i)
	{
		( val[ i] < theVal ) == ascend ? theVal = val[ i], pos = i : true ;
	}
	return pos ;
}

#endif
