#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <pthread.h>

#include "sim_main.h"
#include "sim_if.h"
#include "sim_hw.h"
#include "sim_vmm.h"



void* if_add_node(struct hw_txds * txds_tail, struct hw_txds * htxds)
{
	struct hw_txds * tmp = txds_tail;
	struct hw_txds * last = tmp;
	assert(htxds);
	while(tmp)
	{
		last = tmp;
		tmp = tmp->txds_nxt;	
	}
	last->txds_nxt = htxds;	
}

struct hw_txds * if_remove_node(struct hw_txds * txds_head)
{
	struct hw_txds * a = NULL;
	struct hw_txds * b = NULL;
	struct hw_txds * ret = NULL;

	if(txds_head->txds_nxt != NULL)
	{
		 a = txds_head->txds_nxt;
		 b = a->txds_nxt;
		 txds_head->txds_nxt = b;
		 a->txds_nxt = NULL;
		 ret = a;
	}
	else
	{
		//printf("%s(%d): linker is empty\n", __func__, __LINE__);
		ret = NULL;
	}
	return ret;
}


void * sim_if(void* para)
{
	struct hw_rsc * hrsc = smain_get_soc_src();
	struct hw_fifo* pkt_fifo = &hrsc->pkt_fifo;
	struct hw_txds * htxds = NULL;

	while(1)
	{	
		htxds = (struct hw_txds*) vmm_fifo_out(pkt_fifo);
		if(htxds != NULL)
		{
			if_add_node(&hrsc->hw_if_txq_reg, htxds);	
			//printf("%s,add txds...\n", __func__);
		}
		else
		{
			//printf("%s, %d htxds is null ...\n", __func__, __LINE__);
		}
		usleep(smain_get_pri_order(thrd_if_eid));
	}
	return NULL; 

}
