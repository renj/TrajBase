// SlashBurn.cpp : 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include<string>
#include<iostream>
using namespace std;

#include "Utils.h"
#include "SlashBurn.h"

void message()
{
	//string sortedFileName, string degFileName, string outFile, float keepRatio, const int bufferSize
	cout << "1. Input file name" << endl ;
	cout << "2. Degree information file" << endl ;
	cout << "3. Output text file name" << endl ;
	cout << "4. K-hub to remove" << endl ;
	cout << "5. Buffer size(in MB)" << endl ;
	cout << "6. Block partition width" << endl ;
}

int main(int argc, char* argv[])
{
	if( argc != 7)
	{
		message();
		exit( -1);
	}
	//
	string sortedGraph = argv[ 1], degreeInfo = argv[ 2], outputFile = argv[ 3] ;

	int K =  Utils::toInt( argv[ 4]), bufferMB = Utils::toInt( argv[ 5]), blockWidth = Utils::toInt( argv[ 6]);

	//
	SlashBurn sb ;
	float time = sb.Start( sortedGraph, degreeInfo, outputFile, bufferMB * 1024 * 1024, K, blockWidth) ;

	cout << "Slashburn running time:" << time/1000 << "(s)" <<endl ;
	cout << "Nonempty blocks count:" << sb.nonEmptyBlockCount() << endl ;
	cout << "Bits per edge:" << sb.bitsPerEdge() << endl ;
	
	return 0;
}

