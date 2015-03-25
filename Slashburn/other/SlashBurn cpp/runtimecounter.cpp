

#include "StdAfx.h"
#include "runtimecounter.h"

Runtimecounter::Runtimecounter(){
}

void Runtimecounter::start(){
	gettimeofday(&this->t1, NULL);
}

void Runtimecounter::stop(){
	gettimeofday(&this->t2, NULL);
}

float Runtimecounter::GetRuntime(){
	float t=(float)(t2.tv_sec-t1.tv_sec)*1000.0+(float)(t2.tv_usec-t1.tv_usec)/1000.0;
	return t;
}

int Runtimecounter::gettimeofday(struct timeval *tp, void *tzp)
{
    time_t clock;
    struct tm tm;
    SYSTEMTIME wtm;

    GetLocalTime(&wtm);
    tm.tm_year     = wtm.wYear - 1900;
    tm.tm_mon     = wtm.wMonth - 1;
    tm.tm_mday     = wtm.wDay;
    tm.tm_hour     = wtm.wHour;
    tm.tm_min     = wtm.wMinute;
    tm.tm_sec     = wtm.wSecond;
    tm. tm_isdst    = -1;
    clock = mktime(&tm);
    tp->tv_sec = clock;
    tp->tv_usec = wtm.wMilliseconds * 1000;

    return (0);
}