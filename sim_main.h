#ifndef __SIM_MAIN_H__
#define __SIM_MAIN_H__

#define hw_cell_sz  512
#define hw_cell_dp 128 
#define HW_PKT_FIFO_DEEP (64)

enum {
	thrd_vmm_eid,
	thrd_if_eid,
	thrd_fw_eid,
	thrd_hw_eid,
	thrd_rcy_eid,
	thrd_max_eid,
};

//soc sram for simualtion system
unsigned int  smain_get_pri_order(unsigned int thrd_eid);


struct hw_rsc* smain_get_soc_src(void);

#endif

