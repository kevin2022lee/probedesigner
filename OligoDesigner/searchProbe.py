
class NonNSHFilter:
    
    def __init__(self):  
        pass
    '''Nonnshfilter Class'''  
    def oligoTm(self,s):
        if len(s)!= 0:
            s=s.upper()
            acount=s.count('A')
            ccount=s.count('C')
            gcount=s.count('G')
            tcount=s.count('T')
            rcount=s.count('R') 
            ycount=s.count('Y')
            mcount=s.count('M')
            kcount=s.count('K')
            scount=s.count('S')
            wcount=s.count('W')
            hcount=s.count('H') 
            dcount=s.count('D')
            bcount=s.count('B')
            vcount=s.count('V') 
            ncount=s.count('N')
            if len(s)<14:
                TmValue=round(2*(acount+tcount+rcount+ycount+mcount+scount+hcount+dcount+ncount)+4*(gcount+ccount+rcount+ycount+kcount+wcount+bcount+vcount+ncount))
            else:
                TmValue=round(64.9+41*((gcount+ccount+rcount+ycount+mcount+kcount+scount+bcount+vcount+ncount-16.4)/len(s)))
        else:
            TmValue=0
        return TmValue

    def filterSequence(self,string,lower,upper):
        length=len(string)
        data_probe=[]
        probelist=[0]
        while(sum(data_probe)<length-35):
            data=[]
            data_tm=[]
            ns=string[sum(data_probe):]
            if len(ns)>10:
                for i in range(len(ns)):
                    data.append(ns[:i])
                for d in data:
                    data_tm.append(self.oligoTm(d))
                data_probe.append(self.search(data_tm,lower,upper))
            else:
                print "List index out of range"
####返回probedata############################################################
        for offset in range(0,len(data_probe)):
            probelist.append(sum(data_probe[0:offset+1]))
        return probelist

    def search(self,lst,m,n):
        def search_upper_bound(lst,key):

            low = 0
            high = len(lst)- 1
            if key > lst[high]  :
                return []
            if key <= lst[low]  :
                return lst
            while low < high : 
                mid = (low + high+1) // 2 
                if lst[mid] < key:
                    low = mid
                else:
                    high = mid - 1        
            if lst[low] <= key:    
                return lst[low+1:]

        def search_lower_bound(lst,key):

            low = 0
            high = len(lst)- 1
            if key <= lst[low]  :
                return []
            if key >= lst[high]  :
                return lst
            while low < high : 
                mid = (low + high ) // 2 
                if key < lst[mid]:
                    high = mid
                else:
                    low = mid +1  
            if key <=lst[low]:    
                return lst[:low]
        return lst.index(list(set(search_upper_bound(lst,m)) & set(search_lower_bound(lst,n)))[0])
