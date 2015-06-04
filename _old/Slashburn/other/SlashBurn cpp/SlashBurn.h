#ifndef _SLASH_BURN_HEAD_
#define _SLASH_BURN_HEAD_

#include <string>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <memory>
#include <iostream>
using namespace std ;

#include "Buffer.h"

class SlashBurn
{
	static const int LARGE_INT = (int)(((unsigned int)(~0)) >> 1 ) ;

	//The id-position mapping, by default -1
	int *_deg, *_idPos, *_posID, *_vGID, *_vHubID, **_pos ;
	int _vCount, _curHubCount, _curTailPos, _curGID  ;

	int _blockWidth, _blocksCount, *_blockCounter, _edgeCount ;

public:
	SlashBurn(void);
	~SlashBurn(void);

public:
	float Start( string inputFile, string degFile, string outputFile, const int bufferSize, const int K, const int blockWidth);

	int nonEmptyBlockCount();

	float bitsPerEdge();
private:
	//@function: Greedy selection K hub vertex
	//@params: buffer and in are used for scanning the buffer
	void HubSelection(Buffer &buffer, FILE *in, const int K);

	//@function: Find CC
	void FindCC( Buffer &buffer, FILE *in);
	void FindCC2( Buffer &buffer, FILE *in);

	//@function: Hub sort
	void HubSort();

	void Recode( FILE *in, FILE *out, Buffer &buffer);
private:
	//
	void Init(string degFile, const int blockWidth);

	//@function: Sort the degree vector with count sort
	void countSortDegree();

	//@function: Update the degree information for the vertex; If
	//@return: If the adjacent list of vid is not in memory,return false
	bool updateDeg( const int vid);

	//@function: Given the start of the buffer start, we build _pos(vid to its adjacent list) from it
	//@return: Return unconsumed count
	int buildPos( int *start, const int count);

	//@function: Move last count data(at buffer end) to the start of the buffer and keep them
	void consolidateBuffer( Buffer &buffer, const int count);

	//@function: Return if an id is a hub
	inline bool isHub( const int vid){
		return _idPos[ vid] < _curHubCount ;
	}
	inline bool isSpoke( const int vid){
		return _idPos[ vid] >= _curTailPos ;
	}

	//@function: Analyze current buffer to find CC
	bool findCC( const int id,int * markedID, bool * marked, bool * marked2, map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v, const int gid);

	//@function: Return if the id has been newly marked by gid
	bool markCC( const int id, bool * marked, map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v, const int gid);

	//@function: Combine the components
	void combineCC( bool * marked, const int count,map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v );
	void combineCC( const int vid, set<int> &ccMembers,set<int> &uniqueCC, bool * markedCC, bool * markedV
		, map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v);

	//@function: Set maximum conneced hub id for connected component
	void setMaxHubID();

	//@function: Return the size of each connected component
	int * getCCSize();

	//@function: Log information for evaluation
	void logEvalInfo(const int rowID, const int colID);
};
//Hub sort element
struct hsel{
	int hubID ;
	int size ;
	int gid ;
	int id ;
	hsel(const int h, const int s, const int g, const int i):hubID( h), size( s), gid( g), id(i){}
	bool operator > (const hsel & rhs) const{
		if( hubID == rhs.hubID ){
			if( size == rhs.size ){
				return gid > rhs.gid ;
			}
			return size > rhs.size ;
		}
		return hubID > rhs.hubID ;
	}	
};

//Secondary sort element
template<typename T1, typename T2>
struct ssElement{
	T1 k1 ;
	T2 k2 ;
	ssElement(T1 val1, T2 val2){
		k1 = val1 ;
		k2 = val2 ;
	}
	bool operator < (const ssElement<T1,T2> & rhs) const{
		if( k1 == rhs.k1)
			return k2 > rhs.k2 ;
		return k1 < rhs.k1 ;
	}
	bool operator > (const ssElement<T1,T2> & rhs) const{
		if( k1 == rhs.k1)
			return k2 < rhs.k2 ;
		return k1 > rhs.k1 ;
	}	
};
//Co-sort element
typedef ssElement<int,int> cosElement ;

template<typename T1, typename T2>
void coSort(T1 * val1, T2 * val2, const int count, bool ascend){
	vector< ssElement<T1,T2>> container ;
	for(int i = 0; i < count; ++i){
		container.push_back( ssElement<T1,T2>( val1[ i], val2[ i]));
	}
	if( ascend){
		sort( container.begin(), container.end(), less< ssElement<T1,T2>>());
	}else{
		sort( container.begin(), container.end(), greater< ssElement<T1,T2>>());
	}
	
	for(int i = 0; i < count; ++i){
		val1[ i] = container[ i].k1 ;
		val2[ i] = container[ i].k2 ;
	}
}

#endif