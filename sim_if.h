#ifndef __SIM_IF_H__
#define __SIM_IF_H__

#include "sim_hw.h"


#define SIM_IF_INTVL (800)
void * sim_if(void* para);

void* if_add_node(struct hw_txds * txds_tail, struct hw_txds * htxds);

struct hw_txds * if_remove_node(struct hw_txds * txds_head);
#endif

