#ifndef _RUNTIMECOUNTER_H_
#define _RUNTIMECOUNTER_H_

 /*
 * runtimecounter.h
 *
 * 		Measure time of the program
 *      Author: Shumo Chu
 */



#include <time.h>
#include <windows.h>

/*
struct timeval{
long    tv_sec;         // seconds
long    tv_usec;        // microseconds
};
struct timezone{
int     tz_minuteswest; // minutes W of Greenwich
int     tz_dsttime;     // type of dst correction
};*/




class Runtimecounter{
public: //timezone tz;
	timeval t1;
	timeval t2;
	public:
		Runtimecounter();
		void start();
		void stop();
		float GetRuntime();
		float GetRuntimeusr();
		int gettimeofday(struct timeval *tp, void *tzp);
};

#endif /* _RUNTIMECOUNTER_H_ */
