#ifndef __SIM_HW_H__
#define __SIM_HW_H__

#include <pthread.h>

#define SIM_HW_INTVL 		(500)
#define HW_SOC_SRAM_MAX		(1024 * 128) 
#define HW_DEV_MAX      	(4)
#define HW_TXQ_MAX		(8)
#define HW_PKT_CID_MAX 		(8)

#define HW_IS_AMSDU  		(1)
#define HW_IS_NOT_AMSDU  	(0)
#define HW_AMSDU_NONE  		(0)
#define HW_AMSDU_STT  		(1)
#define HW_AMSDU_END  		(2)

#define HW_IS_AMPDU  		(1)
#define HW_IS_NOT_AMPDU  	(0)
#define HW_AMPDU_NONE  		(0)
#define HW_AMPDU_STT  		(1)
#define HW_AMPDU_END  		(2)

#define HW_EN_AMPDU  		(1)
#define HW_EN_AMSDU  		(1)
#define HW_DIS_AMPDU  		(0)
#define HW_DIS_AMSDU  		(0)



struct hw_irq_status{
	unsigned int tx_ok;
	unsigned int tx_fail;
	//T.B.D
};

struct hw_fifo{
	unsigned long* ebs_reg;
	unsigned int   esz_reg;
	unsigned int   emx_reg;	
	int            evld_reg;// valid fifo resource: in->evld--, out->evld++	
	unsigned int   ei_reg;
	unsigned int   eo_reg;
	unsigned int   ecb_reg;// combol ptr 
	pthread_mutex_t mutex;
};


struct pkt_info_bits
{
	unsigned long hmac_id:2,
		      qid:3,
		      amsdu:1, 
		      ampdu :1,
		      amsdu_agg_st:2,
		      ampdu_agg_st:2,
		      cid_num:4,
		      rsv:16;
};

struct hw_txds {
	struct pkt_info_bits pkt_info;		//enable or disable,ampdu or mpdu 
	struct hw_txds * txds_nxt;   		//have next txds or not
	struct hw_txds * txds_msdu;   		//have next txds or not
	struct hw_txds * txds_amsdu_sub;   	//have next txds or not
	struct hw_txds * txds_mpdu;   		//have next txds or not
	struct hw_txds * txds_ampdu_sub;   	//have next txds or not

	unsigned int txds_status;  			//ok or failed
	unsigned int tx_vct;    			//tx para for phy and rf
	unsigned int data_len; 			// data cell total (bytes)
	unsigned int rsv;   
	unsigned long cid[HW_PKT_CID_MAX];	// tx unit(mpdu) 
};

struct hw_agg_ctrl {

	unsigned int amsdu_ctrl :16,ampdu_ctrl :16;   
};

struct hw_rsc 
{
	struct hw_agg_ctrl  agg_ctrl;
	//hardware system irq reg

	struct hw_irq_status hw_irq_stu_reg;
	pthread_mutex_t hw_irq_stu_reg_mtex;

	//tx packet fifo bwtween vmm and if 
	struct hw_fifo pkt_fifo;

	//tx cell pool fifo amone vmm,if,rcy; 
	struct hw_fifo cid_fifo;

	//pkt q connect point
	struct hw_txds  hw_if_txq_reg;
	pthread_mutex_t hw_if_txq_mtex;

	struct hw_txds  hw_txq_msdu_reg[HW_DEV_MAX][HW_TXQ_MAX];
	pthread_mutex_t hw_txq_msdu_mtex[HW_DEV_MAX][HW_TXQ_MAX];

	struct hw_txds  hw_txq_mpdu_reg[HW_DEV_MAX][HW_TXQ_MAX];
	pthread_mutex_t hw_txq_mpdu_mtex[HW_DEV_MAX][HW_TXQ_MAX];

	struct hw_txds  hw_txq_done_reg;
	pthread_mutex_t hw_txq_done_mtex;

	//hardware rx path ctrl reg
	//T.B.D  

	unsigned char* hw_data_buf;// for data fifo
};


unsigned int hw_txq_to_phy(void);
struct hw_rsc * sim_hw_create_soc(unsigned int soc_type);
struct hw_rsc * sim_hw_destroy_soc(struct hw_rsc* soc_rsc);
void * sim_hw(void* para);

#endif
