################################################################################
#                                                                              #
#   original author = george phillips                                          #
#   email  = phillips@biochem.wisc.edu                                         #
#   ported to python / bug-fixed by tony kamenick 4/06                         #
#   program_name = struts.py                                                   #
#   version 0.6                                                                #
#   copyright reserved, 2005-2006                                              #
#                                                                              #
################################################################################

import sys,re,math

class monitors:

    def __init__(self,pdb,thresh,delta,type):
        self.pdb    = pdb
        self.thresh = thresh
        self.delta  = delta
        self.type   = type

    def getStruts(self):
        struts = []
        pdb_lines = self.pdb
        THRESH   = self.thresh
        DELTA    = self.delta
        
        # find all the CAlphas
        # need to know the size of the CAlpha array before we create it
        
        length = 0
        found = 0
        for line in pdb_lines:
            if(re.match("ATOM",line)):
                if(re.search(" "+self.type+" ",line)):
                    length+=1
                    found = 1

        if found == 0:
            return[]
        ca_array = [([[]]*6)]*length

        #populate CA array
        i=0
        for line in pdb_lines:
            if(re.match("ATOM",line)):
                if(re.search(" "+self.type+" ",line)):
                    ca_array[i] = ([float(line[30:38].strip()), # X
                                    float(line[38:46].strip()), # Y 
                                    float(line[46:54].strip()), # Z
                                    line[22:26].strip(),        # residue number
                                    line[21:22].strip(),        # chain ID
                                    (line[6:11].strip())])      # Atom S.N.
                    i+=1

        # Construct CAlpha distance matrix
        distance = [[]] * length
        taken    = [[]] * length
        for i in range(0,length):
            distance[i] = [[]]*length

        for k in range(0,length):
            taken[k] = [[]]*length

        count = 0
        j = 0
        i = 0
        for ca in ca_array:
            while j <= i:
                if i < length:
                    distance[i][j] = math.sqrt(
                                     math.pow((ca_array[i][0] - 
                                                        ca_array[j][0]),2)+ 
                                     math.pow((ca_array[i][1] - 
                                                        ca_array[j][1]),2)+ 
                                     math.pow((ca_array[i][2] - 
                                                        ca_array[j][2]),2))
                    distance[j][i]=distance[i][j]
                    taken[i][j] = 0
                    taken[j][i] = 0
                    d = i - j

                    if d <= 6 and ca_array[i][4] == ca_array[j][4]:
                        taken[i][j] = 2
                        taken[j][i] = 2
                j+=1    
            j=0
            i+=1

# Now connect atoms within threshold and farther than delta in the sequence
# first find the closest contacts and claim them, then use longer ones up 
# to the threshhold

        thr = int(THRESH) - 4
        while thr <= int(THRESH):
        # for(i=0; i <= length; i++)
            i = 0
            while i <= length:
                # for (j=0; j < i ; j++)
                for j in range(0,i):
                    if i < length:
                        if distance[i][j] <= thr:
                            if taken[i][j] == 0:
                                struts.append([ca_array[i],
                                              ca_array[j]]);
                                # for(k= i - DELTA ; k <= i+DELTA ; k++)
                                k = i - int(DELTA)
                                while k <= i+int(DELTA):
                                    # for(l= j - DELTA; l <= j+DELTA; l++)
                                    l = j - int(DELTA)
                                    while l<=j+int(DELTA):
                                        if k < length and l < length:
                                            if k >= 0 and l>=0 and taken[k][l] != 2:
                                                taken[l][k] = 1
                                                taken[k][l] = 1
                                        l+=1 
                                    l=0 

                                    k+=1 
                i+=1 
            j = 0
            thr+=1

# make sure N and C-termini of each chain ID have anchors within three a.a's
# of the ends. If not, add them finding the closest contact point.
# first need to get list of chain IDs and start/end points

        n = 0
        ID = [[]]*length
        begin = [[]]*length
        end   = [[]]*length
        ID[n]    = ca_array[n][4]
        begin[n] = 1
        end[n]   = 1
        i=0

        while i <= length:
            if i < length:
                curID = ca_array[i][4]
                if(curID == ID[n]):
                    end[n] = i
                else:
                    n+=1
                    begin[n] = i
                    ID[n]  = curID
                    end[n] = i
            else:
                n+=1
            i+=1

        k = 1
        iN = 0
        jN = 0
        iC=0
        jC=0
        while k < n:
            OKN = 0
            minN = 9999999
            i = 0
            while i <= length:
                j = begin[k]  
                while j <= begin[k] + 2:
                    if i < length and j < length:
                        if taken[i][j] != 2:
                            if taken[i][j] == 1:      
                                OKN = 1
                            if distance[i][j]<=minN:
                                iN = i
                                jN = j
                                minN = distance[i][j]              
                    j+=1
                j=0
                i+=1

            OKC = 0
            minC = 9999999
            i = 0
            while i <= length:
                j = end[k]-2
                while j <= end[k]:
                    if i < length and j < length:
                        if taken[i][j]!=2:
                            if taken[i][j] == 1:    
                                OKC = 1
                            if distance[i][j]<=minC:
                                iC=i
                                jC=j
                                minC=distance[i][j]
                    j+=1 
                j=0
                i+=1 

            if OKN == 1:
                struts.append([ca_array[iN],ca_array[jN]])
            if OKC == 1:
                struts.append([ca_array[iC],ca_array[jC]])
            k+=1
        return struts
