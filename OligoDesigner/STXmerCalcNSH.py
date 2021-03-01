class STXCalcNSH:
    def __init__(self):
        pass
    '''This a Class that can calculate the NSH and LCS'''
    def lcs(self,first,second):  
        first_length = len(first)  
        second_length = len(second)  
        size = 0  
        x = 0  
        y = 0  
        matrix = [range(second_length) for x in range(first_length)]  
        #print matrix  
        for i in range(first_length):  
            for j in range(second_length):  
                #print i,j  
                if first[i] == second[j]:  
                    if i - 1 >= 0 and j - 1 >=0:  
                        matrix[i][j] = matrix[i-1][j-1] + 1  
                    else:  
                        matrix[i][j] = 1  
                    if matrix[i][j] > size:  
                        size = matrix[i][j]  
                        x = j  
                        y = i  
                else:  
                    matrix[i][j] = 0  
        #print matrix  
        #print size,x,y   
  
        return second[x-size+1:x+1] 
    ############################################
    def xmerCalc(self,Calc_Seq):
        from Bio.Seq import Seq
        from Bio.Alphabet import IUPAC
#########################QuantiMAT2.0 universal file#####################################################        
        uni_Aleader_seq1=Seq("AAAACGGTAACTTCTTTATGCTTTGACTCAG", IUPAC.unambiguous_dna)
        uni_Aleader_seq3=Seq("AGACAAGCTATTACCTGTATTTACCGAG", IUPAC.unambiguous_dna)
        uni_Aarms_seq1=Seq("ATCTCAGTCTCGTTAATGGATTCCT", IUPAC.unambiguous_dna)
        uni_Aarms_seq3=Seq("ACGCTATCTCTGTAGTTGATTCACT", IUPAC.unambiguous_dna)
        uni_AP_seq1=Seq("GATGTGGTTGTCGTACTT", IUPAC.unambiguous_dna)
        uni_AP_seq3=Seq("GATGTGGTTGTCGTACTT", IUPAC.unambiguous_dna)
        #uni_AP_5R_seq=Seq("TTAGGGGCGTGTTTCATT", IUPAC.unambiguous_dna)
        uni_PSCP_seq=Seq("CTCTTGGAAAGAAAGT", IUPAC.unambiguous_dna)
        
##############LCS#############
        Calc_Seq=Seq(Calc_Seq, IUPAC.unambiguous_dna).upper()
        x4merlcs_Aleader1=self.lcs(str(uni_Aleader_seq1),str(Calc_Seq))
        x4merlcs_Aleader3=self.lcs(str(uni_Aleader_seq3),str(Calc_Seq))
        x4merlcs_Aarms1=self.lcs(str(uni_Aarms_seq1),str(Calc_Seq))
        x4merlcs_Aarms3=self.lcs(str(uni_Aarms_seq3),str(Calc_Seq))
        x4merlcs_AP1=self.lcs(str(uni_AP_seq1),str(Calc_Seq))
        x4merlcs_AP3=self.lcs(str(uni_AP_seq3),str(Calc_Seq))
        x4merlcs_PSCP=self.lcs(str(uni_PSCP_seq),str(Calc_Seq))
###########Server as CE Probe Weighting Factor##########################
        WF_CEtoLeaders=3
        WF_CEtoAMParms=25
        WF_CEtoAP=15
        #WF_CEtoAP_5R=5
        WF_CEtoPSCP=0
###########Server as LE Probe Weighting Factor##########################
        WF_LEtoLeaders=0
        WF_LEtoAMParms=0
        WF_LEtoAP=0
        #WF_LEtoAP_5R=0
        WF_LEtoPSCP=6
############################################################################
        if len(x4merlcs_Aleader1) >=4:
            score_x4mer_Aleader1=[]
            data_Aleader={}
            i=0
            while(i<len(x4merlcs_Aleader1)-3):
                score_x4mer_Aleader1.append(self.x4merScore(x4merlcs_Aleader1[i:i+4]))
                i=i+1
            data_Aleader['score_x4mer_Aleader1']=score_x4mer_Aleader1
            NSH_Score_Aleader1_SACE=sum(data_Aleader['score_x4mer_Aleader1'])*WF_CEtoLeaders
            NSH_Score_Aleader1_SALE=sum(data_Aleader['score_x4mer_Aleader1'])*WF_LEtoLeaders
        else:
            NSH_Score_Aleader1_SACE=0
            NSH_Score_Aleader1_SALE=0
            
        if len(x4merlcs_Aleader3) >=4:
            score_x4mer_Aleader3=[]
            data_Aleader={}
            i=0
            while(i<len(x4merlcs_Aleader3)-3):
                score_x4mer_Aleader3.append(self.x4merScore(x4merlcs_Aleader3[i:i+4]))
                i=i+1
            data_Aleader['score_x4mer_Aleader3']=score_x4mer_Aleader3
            NSH_Score_Aleader3_SACE=sum(data_Aleader['score_x4mer_Aleader3'])*WF_CEtoLeaders
            NSH_Score_Aleader3_SALE=sum(data_Aleader['score_x4mer_Aleader3'])*WF_LEtoLeaders
        else:
            NSH_Score_Aleader3_SACE=0
            NSH_Score_Aleader3_SALE=0    
            
###############Aarms xmer Score############################################
        if len(x4merlcs_Aarms1) >=4:
            i=0
            score_x4mer_Aarms1=[]
            data_Aarms={}
            while(i<len(x4merlcs_Aarms1)-3):
                score_x4mer_Aarms1.append(self.x4merScore(x4merlcs_Aarms1[i:i+4]))
                i=i+1
            data_Aarms['score_x4mer_Aarms1']=score_x4mer_Aarms1
            NSH_Score_Aarms1_SACE=sum(data_Aarms['score_x4mer_Aarms1'])*WF_CEtoAMParms
            NSH_Score_Aarms1_SALE=sum(data_Aarms['score_x4mer_Aarms1'])*WF_LEtoAMParms
        else:
            NSH_Score_Aarms1_SACE=0
            NSH_Score_Aarms1_SALE=0
            
        if len(x4merlcs_Aarms3) >=4:
            i=0
            score_x4mer_Aarms3=[]
            data_Aarms={}
            while(i<len(x4merlcs_Aarms3)-3):
                score_x4mer_Aarms3.append(self.x4merScore(x4merlcs_Aarms3[i:i+4]))
                i=i+1
            data_Aarms['score_x4mer_Aarms3']=score_x4mer_Aarms3
            NSH_Score_Aarms3_SACE=sum(data_Aarms['score_x4mer_Aarms3'])*WF_CEtoAMParms
            NSH_Score_Aarms3_SALE=sum(data_Aarms['score_x4mer_Aarms3'])*WF_LEtoAMParms
        else:
            NSH_Score_Aarms3_SACE=0
            NSH_Score_Aarms3_SALE=0    
###############APs xmer Score##############################################
        if len(x4merlcs_AP1) >=4:
            i=0
            score_x4mer_AP1=[]
            data_AP={}
            while(i<len(x4merlcs_AP1)-3):
                score_x4mer_AP1.append(self.x4merScore(x4merlcs_AP1[i:i+4]))
                i=i+1
            data_AP['score_x4mer_AP1']=score_x4mer_AP1
            NSH_Score_AP1_SACE=sum(data_AP['score_x4mer_AP1'])*WF_CEtoAP
            NSH_Score_AP1_SALE=sum(data_AP['score_x4mer_AP1'])*WF_LEtoAP
        else:
            NSH_Score_AP1_SACE=0
            NSH_Score_AP1_SALE=0
###############AP_5Rs xmer Score##############################################
        if len(x4merlcs_AP3) >=4:
            i=0
            score_x4mer_AP3=[]
            data_AP={}
            while(i<len(x4merlcs_AP3)-3):
                score_x4mer_AP3.append(self.x4merScore(x4merlcs_AP3[i:i+4]))
                i=i+1
            data_AP['score_x4mer_AP3']=score_x4mer_AP1
            NSH_Score_AP3_SACE=sum(data_AP['score_x4mer_AP3'])*WF_CEtoAP
            NSH_Score_AP3_SALE=sum(data_AP['score_x4mer_AP3'])*WF_LEtoAP
        else:
            NSH_Score_AP3_SACE=0
            NSH_Score_AP3_SALE=0
##############PSCP x-mer Score###############################
##############PSCP x-mer Score###############################

        if len(x4merlcs_PSCP) >=4:
            i=0
            score_x4mer_PSCP=[]
            data_PSCP={}
            while(i<len(x4merlcs_PSCP)-3):
                score_x4mer_PSCP.append(self.x4merScore(x4merlcs_PSCP[i:i+4]))
                i=i+1
            data_PSCP['score_x4mer_PSCP']=score_x4mer_PSCP
            NSH_Score_PSCP_SACE=sum(data_PSCP['score_x4mer_PSCP'])*WF_CEtoPSCP
            NSH_Score_PSCP_SALE=sum(data_PSCP['score_x4mer_PSCP'])*WF_LEtoPSCP
        else:
            NSH_Score_PSCP_SACE=0
            NSH_Score_PSCP_SALE=0
#######END############
        Total_NSH_SACE1= NSH_Score_Aleader1_SACE+NSH_Score_Aarms1_SACE+NSH_Score_AP1_SACE+NSH_Score_PSCP_SACE
        Total_NSH_SALE1= NSH_Score_Aleader1_SALE+NSH_Score_Aarms1_SALE+NSH_Score_AP1_SALE+NSH_Score_PSCP_SALE
        Total_NSH_SACE3= NSH_Score_Aleader3_SACE+NSH_Score_Aarms3_SACE+NSH_Score_AP3_SACE+NSH_Score_PSCP_SACE
        Total_NSH_SALE3= NSH_Score_Aleader3_SALE+NSH_Score_Aarms3_SALE+NSH_Score_AP3_SALE+NSH_Score_PSCP_SALE
        return [Total_NSH_SACE1+Total_NSH_SACE3,Total_NSH_SALE3+Total_NSH_SALE3]
        
    def x4merScore(self,seq):
        SumAT=seq.count("A")+seq.count("T")
        SumGC=seq.count("G")+seq.count("C")
        Score=round((0.5*SumAT+1.0*SumGC)/4,3)
        return Score