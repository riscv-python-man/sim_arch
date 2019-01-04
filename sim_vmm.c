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
#include <unistd.h>

#include "sim_main.h"
#include "sim_hw.h"
#include "sim_vmm.h"


unsigned char * vmm_gen_data(unsigned int data_type, unsigned int data_len )
{
	int i ; 
	unsigned char * buf = (unsigned char*)malloc(data_len);
	assert(buf);
	for(i = 0; i < data_len; i++)
	{
		*buf++ = i;
	}	
	return buf;
}

void vmm_destroy_data(unsigned char* buf)
{
	assert(buf);
	free(buf);
}

unsigned long vmm_fifo_in( struct hw_fifo* fifo, unsigned long e)
{
	unsigned long ret = 0;	
	//	printf("%s: eo %d, ei %d\n",__func__, fifo->eo_reg, fifo->ei_reg );
	assert(fifo);
	pthread_mutex_lock(&fifo->mutex);

	if(++fifo->ei_reg == fifo->emx_reg)
	{
		fifo->ei_reg  = 0;
	}

	if(fifo->eo_reg  == fifo->ei_reg)
	{
		//printf("%s(%d):fifo full... \n", __func__, __LINE__);
		ret = 1;
	}
	else
	{
		*(fifo->ebs_reg + fifo->ei_reg) = e;	
		fifo->evld_reg++;
	}	

         pthread_mutex_unlock(&fifo->mutex);
	return ret;   	
}

unsigned long vmm_fifo_out(struct hw_fifo * fifo )
{
	unsigned long ret = 0;	

	 assert(fifo);
         pthread_mutex_lock(&fifo->mutex);

	 if(++fifo->eo_reg == fifo->emx_reg)
	 {
		 fifo->eo_reg = 0;
	 }

	 if(fifo->eo_reg  ==  fifo->ei_reg)
	 {
		 //printf("%s(%d):fifo  empty... \n", __func__, __LINE__);
	 }
	 else
	 {
		 ret = *(fifo->ebs_reg + fifo->eo_reg);	
		 fifo->evld_reg--;
	 } 

	pthread_mutex_unlock(&fifo->mutex);
	return ret;   	
}



unsigned long vmm_mk_pkt( unsigned char* buf, int buf_len)
{
	struct hw_rsc * hrsc = smain_get_soc_src();
	struct hw_fifo * fifo = &hrsc->cid_fifo;
	struct hw_fifo * pkt_fifo = &hrsc->pkt_fifo;

	unsigned long  cid[8];
	struct hw_txds* htxds = NULL;
        int i = 0;
	int j = 0;
        int remain_len = buf_len;
	unsigned char * buf_cursor = buf;
	int cpy_len = 0; 
	int need_cell = 0;
	int valid_cell = 0;
	
	assert(buf_len >= sizeof(struct hw_txds));
	need_cell = (buf_len + hw_cell_sz -1) / hw_cell_sz;
	
        pthread_mutex_lock(&fifo->mutex);
	if(fifo->evld_reg  <  need_cell) 
	{
		pthread_mutex_unlock(&fifo->mutex);
		//printf("%s(%d):no enough cell..vld %d,need %d\n", __func__, __LINE__, fifo->evld_reg, need_cell);
		//usleep(10);
		return 1;
	}
	pthread_mutex_unlock(&fifo->mutex);
	
//	printf("valid num %d \n", fifo->evld_reg);

	cpy_len = remain_len < hw_cell_sz? remain_len:hw_cell_sz;
	while (remain_len > 0) 
	{
		cid[i] = vmm_fifo_out(fifo);
		if(cid[i] == 0)
		{
			//printf("waiting for cid...\n");
			continue;
		}	
		cpy_len = remain_len < hw_cell_sz? remain_len:hw_cell_sz;
		
//		printf("cid 0x%lx\n",cid[i]);

		memcpy((unsigned char*)cid[i], buf_cursor, cpy_len);
		remain_len -=  hw_cell_sz;
		buf_cursor += cpy_len;
//		printf("cursor %p, remain_len %d, cpy_len %d\n", buf_cursor, remain_len, cpy_len);

		i++;
	}

	htxds = (struct hw_txds*)cid[0];

        htxds->pkt_info.hmac_id = 0;
        htxds->pkt_info.qid = 0;
        htxds->pkt_info.amsdu = HW_IS_NOT_AMSDU ;
        htxds->pkt_info.ampdu =HW_IS_NOT_AMPDU  ;
 
	for(j = 0; j < i; j++)	
	{
		htxds->cid[j] = cid[j];
	}
	
        vmm_fifo_in(pkt_fifo, (unsigned long)htxds);

	printf("%s(%d): mk a pkt ok...\n", __func__, __LINE__);

	return 0;
}

unsigned char  src_buf[VMM_BULK_DATA_LEN] = {1,} ;
void * sim_vmm(void* para)
{
	int pkt_drop = 0;
	while(1)
	{       
		//src_buf = vmm_gen_data(0,VMM_BULK_DATA_LEN);	
		pkt_drop = vmm_mk_pkt(src_buf, VMM_BULK_DATA_LEN);
		if(pkt_drop)
		{
			//printf("%s(%d):pkt_drop...\n", __func__, __LINE__);
		}

	//	vmm_destroy_data(src_buf);
		usleep(smain_get_pri_order(thrd_vmm_eid));
	}

	return NULL; 
} 
