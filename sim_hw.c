#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <pthread.h>

#include "sim_main.h"
#include "sim_hw.h"
#include "sim_if.h"

struct hw_rsc * sim_hw_create_soc(unsigned int soc_type)
{
	struct hw_rsc * ret_src  = 
		(struct hw_rsc * )malloc(sizeof(struct hw_rsc));
	memset(ret_src,0,sizeof(struct hw_rsc));
	return ret_src;
}

struct hw_rsc * sim_hw_destroy_soc( struct hw_rsc* soc_rsc )
{
	assert(soc_rsc);
        free(soc_rsc);	
}


unsigned int hw_process_by_q(struct hw_txds* qhdr)
{
	struct hw_rsc * hrsc = smain_get_soc_src();
	struct hw_txds* htxds = NULL;

	for (;;)
	{
		htxds = if_remove_node(qhdr);
		if(htxds != NULL)
		{
			//printf("send to phy ok...\n");
			if_add_node(&hrsc->hw_txq_done_reg,htxds);
		}
		else
		{
			break;
		}
	}
}

unsigned int hw_txq_to_phy(void)
{
	unsigned int hw_irq_status = 0;
	struct hw_rsc * hrsc = smain_get_soc_src();
	struct hw_txds* htxds = NULL;
	int i = 0;
	int j = 0;

	for(i = 0; i < HW_DEV_MAX; i++)	
	{
		for(j = 0; j < HW_TXQ_MAX; j++)
		{
			if(hrsc->hw_txq_mpdu_reg[i][j].txds_nxt != NULL)
			{
				hw_process_by_q(&hrsc->hw_txq_mpdu_reg[i][j]);		
			}
			else
			{
				//printf("%s(%d):mac[%d]q[%d] is null\n",__func__, __LINE__, i, j);
				continue;
			}

		}
	}
}


void * sim_hw(void* para)
{
   	while(1)
	{	
		hw_txq_to_phy();
		usleep(smain_get_pri_order(thrd_hw_eid));
	}
	return NULL; 

}


