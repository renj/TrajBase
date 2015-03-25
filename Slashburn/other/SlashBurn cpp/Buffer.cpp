#include "StdAfx.h"
#include "Buffer.h"

#include "StdAfx.h"
#include "Buffer.h"

#include<io.h>
#include<assert.h>
#include<memory>
#include<iostream>
#include<assert.h>

using namespace std; 


Buffer::Buffer( const int bufferSize)
{
	_bufferCount = bufferSize / sizeof(int) ;

	_buffer = new int[ _bufferCount] ;

	memset( _buffer, 0, _bufferCount * sizeof(int)) ;

	_reservedCount = _usedCount = 0 ;
}

Buffer::~Buffer(void)
{
	if( _buffer != NULL)
		delete[] _buffer ;
}

void Buffer::resetStatus()
{
	_usedCount = _reservedCount = 0 ;
}

//@function: Load the sorted adjacency list as much as possible
int Buffer::loadSortedGraph(FILE *in)
{
	int readCount = fread( _buffer + _reservedCount, sizeof( int), _bufferCount - _reservedCount, in) ;
	_usedCount += readCount ;

	return readCount ;
}