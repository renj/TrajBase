#include <string>
#include <iostream>
#include <vector>
using namespace std;

#pragma pack (1)

#define u_8 char
#define u_16 unsigned short
#define u_32 unsigned int
#define u_64 unsigned long

//#define DEBUG
//#define MAIN
#define BOOST

#ifdef BOOST
#include <boost/python.hpp>
using namespace boost::python;
#endif

template<typename T>
struct Block{
	unsigned short key;
	T 	value;

	Block(){
		key = 0;
		value = 0;
	}
	Block(int k){
		if(k > 60000){
			cout << "Error: too big tid" << endl;
		}
		key = k;
		value = 0;
	}

	void Union(T v) {
		//cout << value << "\t" << v << endl;
		value = value | v;
		//cout << value << "\t" << v << endl;
	}
};

template<typename T>
struct CBitlist
{
    std::string msg;
    vector< vector< Block<T> > > data;
    int 		base;
    int 		num_cells;

    void Init(int n){
	    base = sizeof(T) * 8;
	    num_cells = n;
	    data.resize(n);
    }

    void Insert(int cid, int tid, int width){
    	/*
    	width = 0 ~ (base-1)
    	*/
    	//cout << cid << " " << tid << " " << width << " " << endl;
    	tid = int(tid/base);
    	if( data[cid].size() == 0 || data[cid].back().key != tid ){
    		Block<T> block = tid;
    		data[cid].push_back(block);
    		/*
    		cout << "Insert row" << cid << ",\tkey:" << data[cid].back().key
    			<< ",\tvalue:" << data[cid].back().value << endl;
    		*/
    	}
    	T v = 1;
    	v = v << width;
    	data[cid].back().Union(v);
    	//cout << "key = " << data[cid].back().key << "\t value = " << data[cid].back().value <<  endl;
    }

    void PrintInfo(){
		cout << "Base: " << base << ",\t#Cells:"
			<< num_cells << ",\t#Rows : " << data.size() << endl;
    }

    void PrintRow(int cell){
    	cout << "Row No.: " << cell << ",\t#Collumns: " << data[cell].size();
		if(data[cell].size() > 0){
			cout << "\tValue Size: " << sizeof(data[cell][0].value);
		}
		cout << endl;
    }

    vector<int> GetRow(int n){
    	vector<int> ret;
    	for(int i = 0; i < data[n].size(); i++){
    		int k = data[n][i].key*base;
    		T v = data[n][i].value;
    		//cout << "key: " << k << ",\tvalue:" << data[n][i].value << endl;
    		int idx = 1;
    		while(v != 0){
    			if(idx > base){
    				//cout << "Error: " << int(v) << endl;
    				break;
    			}
    			if((v & 1) == 1){
    				ret.push_back(k+idx-1);
    			}
    			v = (v >> 1);
    			idx += 1;
    		}
    	}
    	#ifdef DEBUG
    	for(int i = 0; i < ret.size(); i++){
    		cout << ret[i] << ",\t";
    	}
    	cout << endl;
    	#endif
    	return ret;
    }

    #ifdef BOOST
    list GetRowPy(int n){
    	if(n > data.size()){
    		cout << "Error: " << n << " out of " << data.size() << endl;
    	}
    	vector<int> v_ret = GetRow(n);
    	typename vector<T>::iterator iter;
    	list l_ret;
    	/*
    	for(iter = v_ret.begin(); iter != v_ret.end(); ++iter){
    		l_ret.append(*iter);
    	}
    	*/
    	for(int i = 0; i < v_ret.size(); i++){
    		l_ret.append(v_ret[i]);
    	}
    	return l_ret;
    }
    #endif

    int GetSize(){
    	for(int i = 0; i < num_cells; i++){
    		data[i].shrink_to_fit();
    	}


    	u_64 size = 0;
    	for(int i = 0; i < num_cells; i++){
    		size += sizeof(data[i][0])*data[i].capacity()*8;
    	}

    	u_64 data0_size = sizeof(data[0])*data.capacity()*8;

    	#ifdef DEBUG
    	cout << "1st capacity = " << data.capacity() << ",\t";
    	cout << "1st size = " <<  data0_size << ",\t";
    	cout << "nested size = " << size << endl;
    	#endif

    	return size + data0_size;
    }

    vector< vector< Block<T> > > bitlist() const {return data;}
};


template<typename T>
struct CBitlist_picklers: pickle_suite
{
	static boost::python::tuple
	getinitargs(CBitlist<T> const& w) {
		return boost::python::make_tuple(w.data);
	}
};

template<typename T>
void Test(T p){
	int base = sizeof(p)*8;
	cout << "Testing base = " << base << endl;

	CBitlist<T> bitlist;

	bitlist.Init(100);
	bitlist.Insert(99,12,0);
	bitlist.Insert(99,12,base-1);
	bitlist.Insert(99,13,7);
	bitlist.PrintInfo();
	bitlist.PrintRow(99);
	bitlist.GetRow(99);
	int size = bitlist.GetSize();
	cout << "Total size = " << size << endl;

	bitlist.Insert(0,12,0);
	bitlist.Insert(0,14,base-1);
	bitlist.Insert(0,13,7);
	bitlist.PrintInfo();
	bitlist.PrintRow(0);
	bitlist.GetRow(0);
	size = bitlist.GetSize();
	cout << "Total size = " << size << endl;

	cout << endl << endl;
	
}


#ifdef MAIN
int main()
{
	u_8 u8 = 1;
	u_16 u16 = 1;
	u_32 u32 = 1;
	u_64 u64 = 1;

	Block<u_8> b8;
	Block<u_16> b16;
	Block<u_32> b32;
	Block<u_64> b64;
	cout << sizeof(b8) << " " << sizeof(b16) << " " << sizeof(b32)
		<< " " << sizeof(b64) << endl;

	Test(u8);
	Test(u16);
	Test(u32);
	Test(u64);

	return 0;
}
#endif


#ifdef BOOST

BOOST_PYTHON_MODULE(CBitlist)
{
    class_< CBitlist<u_8> >("CBitlist_8")
        .def("Init", &CBitlist<u_8>::Init)
        .def("Insert", &CBitlist<u_8>::Insert)
        .def("PrintRow", &CBitlist<u_8>::PrintRow)
        .def("PrintInfo", &CBitlist<u_8>::PrintInfo)
        .def("GetSize", &CBitlist<u_8>::GetSize)
        .def("GetRowPy", &CBitlist<u_8>::GetRowPy)
        .def_readwrite("base", &CBitlist<u_8>::base)
        .enable_pickling()
        //.def_pickle(CBitlist_picklers<u_8>())
    ;
    class_< CBitlist<u_16> >("CBitlist_16")
        .def("Init", &CBitlist<u_16>::Init)
        .def("Insert", &CBitlist<u_16>::Insert)
        .def("PrintRow", &CBitlist<u_16>::PrintRow)
        .def("PrintInfo", &CBitlist<u_16>::PrintInfo)
        .def("GetSize", &CBitlist<u_16>::GetSize)
        .def("GetRowPy", &CBitlist<u_16>::GetRowPy)
        .def_readwrite("base", &CBitlist<u_16>::base)
        .def_pickle(CBitlist_picklers<u_16>())
        .enable_pickling()
    ;
    class_< CBitlist<u_32> >("CBitlist_32")
        .def("Init", &CBitlist<u_32>::Init)
        .def("Insert", &CBitlist<u_32>::Insert)
        .def("PrintRow", &CBitlist<u_32>::PrintRow)
        .def("PrintInfo", &CBitlist<u_32>::PrintInfo)
        .def("GetSize", &CBitlist<u_32>::GetSize)
        .def("GetRowPy", &CBitlist<u_32>::GetRowPy)
        .def_readwrite("base", &CBitlist<u_32>::base)
        .def_pickle(CBitlist_picklers<u_32>())
        .enable_pickling()
    ;
    class_< CBitlist<u_64> >("CBitlist_64")
        .def("Init", &CBitlist<u_64>::Init)
        .def("Insert", &CBitlist<u_64>::Insert)
        .def("PrintRow", &CBitlist<u_64>::PrintRow)
        .def("PrintInfo", &CBitlist<u_64>::PrintInfo)
        .def("GetSize", &CBitlist<u_64>::GetSize)
        .def("GetRowPy", &CBitlist<u_64>::GetRowPy)
        .def_readwrite("base", &CBitlist<u_64>::base)
        .def_pickle(CBitlist_picklers<u_64>())
        .enable_pickling()
    ;
}
#endif