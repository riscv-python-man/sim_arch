#include "stdio.h"
#include "unistd.h"
#include "sim_main.h"
#include "sim_fw.h"
#include "sim_if.h"


void * sim_fw(void* para)
{
	struct hw_rsc * hrsc = smain_get_soc_src();
	struct hw_txds * txds = NULL;	
	int mac_id = 0;
	int qid = 0;

	while(1)
	{	
		//from hw_if_txq to make a msdu linker,the node could be amsdu or normal msdu.
		txds = if_remove_node(&hrsc->hw_if_txq_reg);
		if (txds != NULL)
		{
			mac_id = txds->pkt_info.hmac_id;
			qid = txds->pkt_info.qid;
			// system level amsdu functional config
			if(hrsc->agg_ctrl.amsdu_ctrl == HW_EN_AMSDU)
			{
				// to do agg amsdu, the amsdu node as a msdu node will be appended on hw_txq_msdu_reg
				if(txds->pkt_info.amsdu == HW_IS_NOT_AMSDU)
				{
					if_add_node(&hrsc->hw_txq_msdu_reg[mac_id][qid],txds);
				}
			}
			else if(hrsc->agg_ctrl.amsdu_ctrl == HW_DIS_AMSDU)
			{
				if_add_node(&hrsc->hw_txq_msdu_reg[mac_id][qid],txds);
				//printf("%s(%d): in tx msdu q\n", __func__, __LINE__);
			}
		}
		else
		{
			//printf("%s(%d): hw if txq txds null\n", __func__, __LINE__);
		}		

		//from msdu linker to make a mpdu linker: the mode could be ampdu or normal mpdu
		txds = if_remove_node(&hrsc->hw_txq_msdu_reg[mac_id][qid]);	
		if(txds != NULL)
		{
			mac_id = txds->pkt_info.hmac_id;
			qid = txds->pkt_info.qid;
			if(hrsc->agg_ctrl.ampdu_ctrl == HW_EN_AMPDU)
			{
				// to do ampdu and append the ampdu node on mpdu;
				if(txds->pkt_info.ampdu == HW_IS_NOT_AMPDU)
				{
					if_add_node(&hrsc->hw_txq_mpdu_reg[mac_id][qid],txds);
				}
			}
			else if(hrsc->agg_ctrl.ampdu_ctrl == HW_DIS_AMPDU)
			{
				if_add_node(&hrsc->hw_txq_mpdu_reg[mac_id][qid],txds);
				//printf("%s(%d): in tx mpdu q\n", __func__, __LINE__);
			}
		}
		else
		{
			//printf("%s(%d): hw txq msdu txds null\n", __func__, __LINE__);
		}		

// to process hw tx status;


		usleep(smain_get_pri_order(thrd_fw_eid));
	}
	return NULL; 
}
