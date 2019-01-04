/*
the software is created by qinghua.zeng.
all of the rights are reserved.
started forn 2018-12-05 in shanghai.
*/

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include <pthread.h>

#include "sim_main.h"
#include "sim_vmm.h"
#include "sim_if.h"
#include "sim_fw.h"
#include "sim_hw.h"
#include "sim_rcy.h"
//vmm->if->fw->hw-rcy
static unsigned int g_pri[]={1,1,1,1,1};

struct hw_rsc* g_soc_rsc;

unsigned int  smain_get_pri_order(unsigned int thrd_eid)
{
	return g_pri[thrd_eid];
}	

void* (*thrd_exe[thrd_max_eid])(void* para) = {sim_vmm, sim_if, sim_fw, sim_hw, sim_rcy};	


struct hw_rsc* smain_get_soc_src(void)
{
	assert(g_soc_rsc);
	return g_soc_rsc;	
}

static int smain_crt_soc(void)
{
	int i = 0;
	int j = 0;
	int k = 0;
	int ret = 0;
	int total_dbuf_sz = 0;
	struct hw_rsc* soc_rsc = NULL;
	unsigned char* cell_id = NULL;
	struct hw_fifo* cid_fifo = NULL; 
	unsigned long * chk_cid = NULL; 
	//have a soc board here
	soc_rsc = sim_hw_create_soc(0);
	assert(soc_rsc);

	//init a system fifo
	soc_rsc->pkt_fifo.esz_reg = sizeof(unsigned long);	
	soc_rsc->pkt_fifo.evld_reg = 0;
        soc_rsc->pkt_fifo.emx_reg = HW_PKT_FIFO_DEEP ;	 
	soc_rsc->pkt_fifo.ei_reg = 0;	 
	soc_rsc->pkt_fifo.eo_reg = 0;	 
	soc_rsc->pkt_fifo.ecb_reg = 0;	 
	pthread_mutex_init(&soc_rsc->pkt_fifo.mutex,NULL);

	soc_rsc->pkt_fifo.ebs_reg = 
		(unsigned long*)malloc(sizeof(unsigned long)*soc_rsc->pkt_fifo.emx_reg);	
	assert(soc_rsc->pkt_fifo.ebs_reg);

	memset(soc_rsc->pkt_fifo.ebs_reg, 0, sizeof(unsigned long)* soc_rsc->pkt_fifo.emx_reg); 

	soc_rsc->cid_fifo.esz_reg = sizeof(unsigned long);
	soc_rsc->cid_fifo.evld_reg = 0;
	soc_rsc->cid_fifo.emx_reg = hw_cell_dp;
	soc_rsc->cid_fifo.ei_reg = 0; 
	soc_rsc->cid_fifo.eo_reg = 0;
	soc_rsc->cid_fifo.ecb_reg = 0;
	pthread_mutex_init(&soc_rsc->cid_fifo.mutex,NULL);

	soc_rsc->cid_fifo.ebs_reg = 
		(unsigned long*)malloc(sizeof(unsigned long)*soc_rsc->cid_fifo.emx_reg );
	assert(soc_rsc->cid_fifo.ebs_reg );	

	memset(soc_rsc->cid_fifo.ebs_reg,0,sizeof(unsigned long)*soc_rsc->cid_fifo.emx_reg);

	total_dbuf_sz += hw_cell_sz * (hw_cell_dp + 1);

	soc_rsc->hw_data_buf = (unsigned char*)malloc(total_dbuf_sz);
	assert(soc_rsc->hw_data_buf);
	memset(soc_rsc->hw_data_buf, 0, total_dbuf_sz);
	printf("(%s,%d): total data buf %d \n",__func__, __LINE__, total_dbuf_sz);	

	
	pthread_mutex_init(&soc_rsc->hw_irq_stu_reg_mtex,NULL);

	g_soc_rsc = soc_rsc;	

	//the cell id in fifo
	cid_fifo = &soc_rsc->cid_fifo;
	for(j = 0; j < soc_rsc->cid_fifo.emx_reg; j++)
	{
		cell_id = soc_rsc->hw_data_buf + j * hw_cell_sz;
		printf("cell_id 0x%lx\n", (unsigned long)cell_id);
		vmm_fifo_in(cid_fifo, (unsigned long)cell_id);
	}         	

	//check the cell id is unique

	chk_cid = soc_rsc->cid_fifo.ebs_reg;

	for(j = 0; j < soc_rsc->cid_fifo.emx_reg; j++)
	{
		//printf("cell_id 0x%lx\n",*(cid_fifo++));
		for (k = j+1; k <  soc_rsc->cid_fifo.emx_reg; k++)
		{
			if(*(chk_cid + j) == *(chk_cid+k))
			{
				printf("(%s,%d):cid_fifo init err\n", __func__, __LINE__);
				return 0;
			}
		}
	}         	

	soc_rsc->agg_ctrl.amsdu_ctrl = HW_DIS_AMSDU ;
	soc_rsc->agg_ctrl.ampdu_ctrl = HW_DIS_AMPDU ;	


	return ret=1;
}

int main()
{
	int i;
	pthread_t thread[thrd_max_eid];
	pthread_attr_t attr[thrd_max_eid];

	if(smain_crt_soc() == 0)
	{
		printf("%s,%d):create soc failed \n", __func__, __LINE__);
		return 0;
	}

	//printf("sz int %d, sz long %d, sz p %d\n", sizeof(int), sizeof(long), sizeof(int*));
	//start the system modules here
	for(i = 0; i < thrd_max_eid; i++ )
	{	
		pthread_attr_init(&attr[i]);
		pthread_attr_setscope(&attr[i], PTHREAD_SCOPE_SYSTEM);
		if(!pthread_create(&thread[i], &attr[i], thrd_exe[i], NULL))
		{
			//pthread_join(thread[i], NULL);
			printf("(%s,%d):create the thread ok\n", __func__, __LINE__);
		}
	}

	//the main thread will always run
	while(1);	

	return 0;

}

