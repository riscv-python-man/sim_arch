#ifndef __SIM_FW_H__
#define __SIM_FW_H__

#include "sim_hw.h"

#define SIM_FW_INTVL (1000)



struct fw_private
{
	int amsdu_flag;
	int ampdu_flag;
	
};


void * sim_fw(void* para);

#endif

