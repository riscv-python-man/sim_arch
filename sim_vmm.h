#ifndef __SIM_VMM_H__
#define __SIM_VMM_H__

#include "sim_hw.h"


#define VMM_BULK_DATA_LEN (4537)

unsigned long vmm_fifo_in( struct hw_fifo* fifo, unsigned long e);

unsigned long vmm_fifo_out(struct hw_fifo * fifo );

unsigned char * vmm_gen_data(unsigned int data_type, unsigned int data_len );

void vmm_destroy_data(unsigned char* buf);

unsigned long vmm_mk_pkt(unsigned char *buf, int buf_len);

void * sim_vmm(void* para);

#endif
