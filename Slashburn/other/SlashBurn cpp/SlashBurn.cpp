#include "StdAfx.h"
#include "SlashBurn.h"
#include "Utils.h"
#include "runtimecounter.h"

SlashBurn::SlashBurn(void)
{
	 _vCount = _curHubCount = _curGID = _curTailPos = 0 ;
	 _deg = _idPos = _posID = _vGID = _vHubID = _blockCounter = NULL ;
	 _pos = NULL ;
	 _blockWidth = _blocksCount = _edgeCount = 0 ;
}

SlashBurn::~SlashBurn(void)
{
	if( _deg)
		delete [] _deg;
	if( _idPos)
		delete [] _idPos;
	if( _posID)
		delete [] _posID;
	if( _pos)
		delete [] _pos ;
	if( _blockCounter)
		delete [] _blockCounter ;
}
float SlashBurn::Start( string inputFile, string degFile, string outputFile, const int bufferSize, const int K, const int blockWidth)
{
	FILE *in = Utils::openFile( inputFile.c_str(), "rb");
	FILE *out = Utils::openFile( outputFile.c_str(), "wt");

	Init( degFile, blockWidth);

	Buffer buffer( bufferSize);

	Runtimecounter rt ;
	float selTime = 0, ccTime = 0, sortTime = 0, recodeTime = 0, tTime = 0 ;
	int iter = 0 ;
	while( _curTailPos - _curHubCount > K ){

		cout << "Slashburn iteration:" << ++iter << endl ;
		
		rt.start();
		HubSelection( buffer, in, K) ;
		rt.stop();
		selTime += rt.GetRuntime() ;
		tTime += rt.GetRuntime() ;

		rt.start();
		FindCC( buffer, in) ;
		rt.stop();
		ccTime += rt.GetRuntime() ;
		tTime += rt.GetRuntime() ;

		rt.start();
		HubSort();
		rt.stop();
		sortTime += rt.GetRuntime() ;
		tTime += rt.GetRuntime() ;

	}
	rt.start();
	Recode( in, out, buffer) ;
	rt.stop();
	recodeTime += rt.GetRuntime() ;
	tTime += rt.GetRuntime() ;

	fclose( in), fclose( out);

	cout << "Hub set selection time:" << selTime/1000 << "(s)" << endl ;
	cout << "Connected component finding time:" << ccTime/1000 << "(s)" << endl ;
	cout << "Hub sort time:" << sortTime/1000 << "(s)" << endl ;
	cout << "Recode time:" << recodeTime/1000  << "(s)" << endl ;

	return tTime ;
}

void SlashBurn::Init(string degFile, const int blockWidth)
{
	FILE *in = Utils::openFile( degFile.c_str(), "rb");
	fread( &_vCount, sizeof(int), 1, in);
	
	_deg = new int[ _vCount] ;
	fread( _deg, sizeof(int), _vCount, in);
	fclose( in) ;

	_pos = new int*[ _vCount] ;
	memset( _pos, NULL, sizeof( int*) * _vCount) ;

	_idPos = Utils::createIncreamental( _vCount);
	_posID = Utils::createIncreamental( _vCount);

	//Allocate memory
	_vGID = new int[ _vCount] ; memset( _vGID, 0, sizeof(int) * _vCount);
	_vHubID = new int[ _vCount] ; memset( _vHubID, 0, sizeof(int) * _vCount);

	_blockWidth = blockWidth ; _blocksCount = ( _vCount + blockWidth - 1) / blockWidth ;
	_blockCounter = new int[ _blocksCount * _blocksCount] ; memset( _blockCounter, 0, sizeof( int) * _blocksCount * _blocksCount );

	_curTailPos = _vCount ;
}


//@function: Greedy selection K hub vertex
void SlashBurn::HubSelection(Buffer &buffer, FILE *in, const int K)
{
	//Current selected hub vertex count, stop until selectedCount = K
	int selectedCount = 0 ;

	int *degCpy = new int[ _curTailPos] ;
	
	while( selectedCount < K ){
		//Sort and permutate the vertex sequence
		countSortDegree();

		//Optimization: Track previous vertex degree
		memcpy( degCpy + _curHubCount, _deg + _curHubCount, sizeof( int) * ( _curTailPos - _curHubCount)) ;

		int restCount = K - selectedCount;

		for( int i = 0; i < restCount; ++i){
			if( _deg[ _curHubCount] < degCpy[ _curHubCount + 1]){
				break ;
			}
			//Scan the memory until we can update the degree information
			if( ! updateDeg( _posID[ _curHubCount])){

				//Reset status to scan the file
				rewind( in); buffer.resetStatus();
				
				while( true){
					buffer.loadSortedGraph( in);
					int unConsumed = buildPos( buffer.getBuffer(), buffer.getUsed());
					if( updateDeg( _posID[ _curHubCount]) == true ){
						break ;
					}
					consolidateBuffer( buffer, unConsumed) ;
				}
			}
			_curHubCount += 1 ;
			selectedCount++ ;
		}
	}
	delete [] degCpy ;
}

//@function: Find CC
void SlashBurn::FindCC( Buffer &buffer, FILE *in)
{
	//Reset status to scan the file
	rewind( in); buffer.resetStatus();

	//
	bool * marked = new bool[ _vCount], *marked2 = new bool[ _vCount] ;
	int * markedID = new int[ _vCount];

	//vertex to connected component mapping, connected component members
	map< int, vector<int> *> v2cc, cc2v ;
	while( buffer.loadSortedGraph( in) != 0 ){
		
		memset( marked, false, sizeof( bool) * _vCount) ;
		memset( marked2, false, sizeof( bool) * _vCount) ;

		buildPos( buffer.getBuffer(), buffer.getUsed());
		
		int *start = buffer.getBuffer(), count = buffer.getUsed(), offset = 0;
		
		for(  ; offset < count - 2; ){
			//If the adjacent list is not all in the memory
			if( ( start[ offset + 1] + offset + 2 ) > count ){
				break ;
			}
			int vid = start[ offset], degree = start[ offset + 1] ;
			offset += ( degree + 2 ) ;
			
			if( isHub( vid) || isSpoke( vid)){
				continue ;
			}

			//Vertex id: start[ offset]
			if( !findCC( vid, markedID, marked, marked2, v2cc, cc2v, ++_curGID))
			{
				--_curGID ;
			}
		}
		consolidateBuffer( buffer, count - offset) ;
	}
	//Now combine the components
	combineCC( marked, _vCount, v2cc, cc2v);

	//Collect the maxium hub ID
	setMaxHubID();

	delete [] marked ;
	delete [] marked2 ;
	delete [] markedID ;
}
void SlashBurn::FindCC2( Buffer &buffer, FILE *in)
{
}

//@function: Hub sort
void SlashBurn::HubSort()
{
	int * size = getCCSize( );

	vector<hsel> result ;

	for(int i = _curHubCount; i < _curTailPos; ++i){ 
		result.push_back( hsel( _vHubID[ _posID[ i]], size[ _vGID[ _posID[ i]]],_vGID[ _posID[ i]], _posID[ i]));
	}
	sort( result.begin(), result.end(), greater<hsel>());
	//At last, update the id permutation
	int count = _curTailPos - _curHubCount, curPos = _curHubCount ;
	for(int i = 0; i < count; ++i, ++curPos)
	{
		_idPos[ result[ i].id] = curPos ;
		_posID[ curPos] = result[ i].id ;
	}
	_curTailPos = _curHubCount + result[ 0].size ;

	delete [] size ;
}
void SlashBurn::Recode( FILE *in, FILE *out, Buffer &buffer)
{
	rewind( in); buffer.resetStatus() ;
	while( buffer.loadSortedGraph( in) != 0 ){

		int *start = buffer.getBuffer(), count = buffer.getUsed(), offset = 0 ;
		for( ; offset < count - 2; ){
			//If the adjacent list is not all in the memory
			if( ( start[ offset + 1] + offset + 2 ) > count ){
					break ;
			}
			int id = start[ offset], deg = start[ offset + 1], *adjs = start + offset + 2 ;
			
			for(int i = 0; i < deg; ++i){
				logEvalInfo( _idPos[ id], _idPos[ adjs[ i]]) ; //Log information for evaluation
				fprintf( out, "%d %d\n", _idPos[ id], _idPos[ adjs[ i]]);
			}
			
			offset += ( deg + 2 ) ;
		}
		int reserved = count - offset ;
		memmove( start, start + offset, reserved * sizeof( int)) ;
		buffer.setReserved( reserved);
		buffer.setUsed( reserved) ;
	}
}

void SlashBurn::countSortDegree()
{
	//Count the degree
	map<int, vector<cosElement>*> bins ;
	for(int i = _curHubCount; i < _curTailPos; ++i){
		vector<cosElement> * theList = NULL ;
		map<int, vector<cosElement>*>::iterator iter = bins.find( _deg[ i]);
		if( iter == bins.end() ){
			theList = new vector<cosElement>();
			bins[ _deg[ i]] = theList ;
		}else{
			theList = iter->second ;
		}
		theList->push_back( cosElement( _deg[ i], _posID[ i]));
	}
	map<int, vector<cosElement>*>::reverse_iterator rit = bins.rbegin();
	for( int curPos = _curHubCount; rit != bins.rend(); ++rit){
		sort( rit->second->begin(), rit->second->end(), greater<cosElement>());

		int degree = rit->first ;
		vector<cosElement>::iterator iterEnd = rit->second->end() ;
		for(vector<cosElement>::iterator vit = rit->second->begin(); vit != iterEnd; ++vit){
			_deg[ curPos] = degree ;
			_posID[ curPos] = vit->k2 ;
			_idPos[ vit->k2] = curPos ;
			curPos++ ;
		}
		delete rit->second ;
	}
}

//@function: Update the degree information for the vertex; If
//@return: If the adjacent list of vid is not in memory,return false
bool SlashBurn::updateDeg( const int vid)
{
	if( _pos[ vid] == NULL)
		return false ;

	int count = *(_pos[ vid] + 1), *pos = _pos[ vid] + 2;
	for( int i = 0; i < count; ++i)
	{
		_deg[ _idPos[ pos[ i]]]-- ;
	}
	return true ;
}

//@function: Given the start of the buffer start, we build _pos(vid to its adjacent list) from it
//@return: Return unconsumed count
int SlashBurn::buildPos( int *start, const int count)
{
	memset( _pos, NULL, sizeof( int) * _vCount) ;
	int offset = 0 ;

	for( ; offset < count - 2; ){
		//If the adjacent list is not all in the memory
		if( ( start[ offset + 1] + offset + 2 ) > count ){
			break ;
		}
		_pos[ start[ offset]] = start + offset ;
		offset += start[ offset + 1] + 2;
	}
	return count - offset ;
}

//@function: Move last count data(at buffer end) to the start of the buffer and keep them
void SlashBurn::consolidateBuffer( Buffer &buffer, const int count)
{
	int * dst = buffer.getBuffer(), * src = buffer.getBuffer() + buffer.getUsed() - count ;
	memmove( dst, src, sizeof( int) * count ) ;
	buffer.setReserved( count) ;
	buffer.setUsed( count) ;
}



//@function: Analyze current buffer to find CC
bool SlashBurn::findCC( const int id,int * markedID, bool * marked, bool * marked2, map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v, const int gid)
{
	int markedCount = 0, totalCount = 1 ; 
	markedID[ 0] = id ;

	for( int scanned = 0; scanned < totalCount; ++scanned){
		//If its adjacent list has been added previously, then continue
		if( markCC( markedID[ scanned], marked, v2cc, cc2v, gid) == false )
			continue ;
		markedCount++ ;

		//If no adjacent list for current id, then continue
		if( _pos[ markedID[ scanned]] == NULL )
			continue ;

		int degree = *( _pos[ markedID[ scanned]] + 1 ), *adjs =_pos[ markedID[ scanned]] + 2 ;

		for(int i = 0; i < degree; ++i){
			if( isHub( adjs[ i])){
				if( _vHubID[ markedID[ scanned]] < _idPos[ adjs[ i]]){
					_vHubID[ markedID[ scanned]] = _idPos[ adjs[ i]] ;
				}
			}else{
				if( marked2[ adjs[ i]] == false){
					markedID[ totalCount++] = adjs[ i] ;
					marked2[ adjs[ i]] = true ;
				}
			}
		}
	}
	/*
	//In order to remove tail recursive call
	int degree = *( _pos[ id] + 1 ), *adjs =_pos[ id] + 2 ;
	for(int i = 0; i < degree; ++i){
		if( isHub( adjs[ i])){
			if( _vHubID[ id] < _idPos[ adjs[ i]]){
				_vHubID[ id] = _idPos[ adjs[ i]] ;
			}
		}else{
			findCC( adjs[ i], marked, v2cc, cc2v, gid);
		}
	}*/
	return markedCount != 0 ;
}
//@function: Return if the id has been newly marked by gid
bool SlashBurn::markCC( const int id, bool * marked, map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v, const int gid)
{
	if( marked[ id])
		return false;

	map< int, vector<int> *>::iterator vcIter = v2cc.find( id) ,cvIter = cc2v.find( gid) ;
	vector<int> *vVec = NULL, *cVec = NULL;
	if( vcIter == v2cc.end() ){
		vVec = new vector<int>() ;
		v2cc[ id] = vVec ;
	}else{
		vVec = v2cc[ id] ;
	}
	if( cvIter == cc2v.end() ){
		cVec = new vector<int>() ;
		cc2v[ gid] = cVec ;
	}else{
		cVec = cc2v[ gid] ;
	}
	marked[ id] = true ; vVec->push_back( gid); cVec->push_back( id) ;

	return true ;
}

//@function: Combine the components
void SlashBurn::combineCC( bool * marked, const int count, map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v )
{
	memset( marked, false, sizeof( bool) * count) ;
	
	bool * markedCC = new bool[ ++_curGID] ;
	memset( markedCC, false, sizeof( bool) * _curGID) ;

	_curGID = 0 ;

	while( v2cc.size() != 0 ){
		//Find unique CC labels first
		set<int> uniqueCC, ccMembers ;
		combineCC( v2cc.begin()->first, ccMembers, uniqueCC, markedCC, marked, v2cc, cc2v);

		int CCID = ++_curGID ;
		//Delete CC info
		for(set<int>::iterator ccIter = uniqueCC.begin(); ccIter != uniqueCC.end(); ++ ccIter){
			markedCC[ *ccIter] = false ;
			delete cc2v[ *ccIter];
			cc2v.erase( *ccIter);
		}
		//Delete vertex info
		for(set<int>::iterator vIter = ccMembers.begin(); vIter != ccMembers.end(); ++ vIter){
			marked[ *vIter] = false ;
			delete v2cc[ *vIter] ;
			v2cc.erase( *vIter);
			_vGID[ *vIter] = CCID;
		}
	}
	delete [] markedCC ;
}
void SlashBurn::combineCC( const int vid, set<int> &ccMembers,set<int> &uniqueCC, bool * markedCC, bool * markedV
		, map< int, vector<int> *> &v2cc, map< int, vector<int> *> &cc2v)
{
	if( markedV[ vid])
		return ;
	markedV[ vid] = true ;
	ccMembers.insert( vid) ;

	vector<int> * ccs = v2cc[ vid] ;
	for(vector<int>::iterator ccIter = ccs->begin(); ccIter != ccs->end(); ++ccIter){
		//If the connected component has been analyzed
		if( markedCC[ *ccIter]){
			continue ;
		}else{
			markedCC[ *ccIter] = true ;
			uniqueCC.insert( *ccIter);

			vector<int> * vs = cc2v[ *ccIter] ;
			for(vector<int>::iterator vIter = vs->begin(); vIter != vs->end(); ++vIter){
				combineCC( *vIter, ccMembers, uniqueCC, markedCC, markedV, v2cc, cc2v);
			}
		}
	}
}
//@function: Set maximum conneced hub id for connected component
void SlashBurn::setMaxHubID()
{
	//Update the maximum conneced hub vertex for group
	int * gHub = new int[ ++_curGID] ;
	memset( gHub, 0, sizeof( int) * _curGID) ;

	for(int i = _curHubCount; i < _curTailPos; ++i){
		if( gHub[ _vGID[ _posID[ i]]] < _vHubID[ _posID[ i]] ){
			gHub[ _vGID[ _posID[ i]]] = _vHubID[ _posID[ i]] ;
		}
	}
	for(int i = _curHubCount; i < _curTailPos; ++i){
		_vHubID[ _posID[ i]] = gHub[ _vGID[ _posID[ i]]] ;
	}
	delete [] gHub ;
}

//@function: Return the size of each connected component
int * SlashBurn::getCCSize()
{
	int * size = new int[ ++_curGID];
	memset( size, 0, sizeof(int) * _curGID) ;
	for(int i = _curHubCount; i < _curTailPos; ++i){
		size[ _vGID[ _posID[ i]]] ++ ;
	}
	return size ;
}

int SlashBurn::nonEmptyBlockCount()
{
	int total = _blocksCount * _blocksCount, count = 0 ;
	for(int i = 0; i < total; ++i){
		if( _blockCounter[ i] != 0)
			count++;
	}
	return count ;
}

#include <math.h>

float log2( float val){
	return log10f( val)/ log10f( 2.0f) ;
}
float SlashBurn::bitsPerEdge()
{
	float b = (float)_blockWidth, n = (float)_vCount ;
	float meta = nonEmptyBlockCount() * 2 * log2( n / b) ;

	float infoSize = 0, bs = b * b ;
	int total = _blocksCount * _blocksCount;
	for(int i = 0; i < total; ++i){
		if( _blockCounter[ i] == 0)
			continue;
		float p = _blockCounter[ i] / bs ;
		infoSize += ( p * log2( 1 / p ) + ( 1 - p ) * log2( 1 / ( 1 - p )));
	}
	float ret = meta + bs * infoSize ;
	return ret / _edgeCount;
}

//@function: Log information for evaluation
void SlashBurn::logEvalInfo(const int rowID, const int colID)
{
	int row = rowID / _blockWidth , col = colID / _blockWidth;
	_blockCounter[ row * _blocksCount + col]++ ;

	_edgeCount++ ;
}