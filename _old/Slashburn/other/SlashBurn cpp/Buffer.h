#ifndef _BUFFER_H_
#define _BUFFER_H_

class Buffer
{
private:
	int *_buffer ;
	int _bufferCount ;

	int _reservedCount ;
	int _usedCount ;

public:
	Buffer( const int bufferSize = 1024 * 64);
	~Buffer(void);

	//@function: Load the sorted adjacency list as much as possible
	int loadSortedGraph(FILE *in);

	//@function:
	void resetStatus();

	//@function: Get and set inner data fields
	inline void setReserved(const int val){
		_reservedCount = val ;
		if( _reservedCount > _usedCount){
			_usedCount = _reservedCount ;
		}
	}
	inline int getReserved(){
		return _reservedCount;
	}
	inline void setUsed(const int val){
		_usedCount = val ;
	}
	inline int getUsed(){
		return _usedCount ;
	}
	inline int* getBuffer(){
		return _buffer ;
	}
	inline int getBufferCount(){
		return _bufferCount ;
	}
};

#endif