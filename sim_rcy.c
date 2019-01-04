#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <pthread.h>

#include "sim_main.h"
#include "sim_hw.h"
#include "sim_if.h"
#include "sim_rcy.h"
#include "sim_vmm.h"
int j = 0;
unsigned int rcy_process(struct hw_txds* qhdr)
{
	struct hw_txds* htxds = NULL;
	struct hw_rsc * hrsc = smain_get_soc_src();
	struct hw_fifo * cid_fifo = &hrsc->cid_fifo;

	int i = 0 ; 
	int n = 0 ; 
	unsigned long cid[HW_PKT_CID_MAX] = {0,};
	for (;;)
	{
		htxds = if_remove_node(qhdr);
		if(htxds != NULL)
		{
			n = htxds->pkt_info.cid_num;
			memcpy(cid,htxds->cid,n);
			for(i = 0; i < n ; i++)
			{
				vmm_fifo_in(cid_fifo,cid[i]);
			}
			
			++j;	
			if(j== 500)
			{	
				printf("rcy ok:i= %d thr= %f Mbps\n", j, ((float)j * VMM_BULK_DATA_LEN * 8) / (1024 * 1024) );
				j = 0;
			}
		}
		else
		{
			break;
		}
	}
}



void * sim_rcy(void* para)
{
	struct hw_rsc * hrsc = smain_get_soc_src();
	while(1)
	{	
		rcy_process(&hrsc->hw_txq_done_reg);

		usleep(smain_get_pri_order(thrd_rcy_eid));
	}
	return NULL; 

}
