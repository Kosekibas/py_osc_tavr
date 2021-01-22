from array import *

n=1
m=2
dict_sample = {}
style = {
    'pbChannels':{},
    'pcrColor':{},
    'piLineWidth':{},
    'piLineStyle':{}
}
                        # ar>>pView->pCustomPD[i].pbChannels[j]; 1b
                        # ar>>pView->pCustomPD[i].pcrColor[j];    4b
                        # ar>>pView->pCustomPD[i].piLineWidth[j]; 4b
                        # ar>>pView->pCustomPD[i].piLineStyle[j]; 4b
for nn in range(n):
    # dict_sample[nn]={}
    for mm in range(m):
        dict_sample[nn]=style
        
        dict_sample[nn]['pbChannels'][mm]=nn+mm+1
        dict_sample[nn]['pcrColor'][mm]=nn+mm+2
        dict_sample[nn]['piLineWidth'][mm]=nn+mm+3
        dict_sample[nn]['piLineStyle'][mm]=nn+mm+4
        print(  'nn=',nn,
                'mm=',mm, 
                'pbChannels',(dict_sample[nn]['pbChannels'][mm]),
                'pcrColor', dict_sample[nn]['pcrColor'][mm],
                'piLineWidth', dict_sample[nn]['piLineWidth'][mm],
                'piLineStyle', dict_sample[nn]['piLineStyle'][mm] 
                )

print (dict_sample)
print('1/2/ piLineStyle=',dict_sample[0]['piLineStyle'][1])