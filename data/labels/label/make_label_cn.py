# -*- coding: utf-8 -*-    
import os   

l=["车:car","行人:pedestrian","骑车:cyclist"]


def make_labels(s): 
    i = 0 
    for word in l:   
        os.system("convert -fill black -background white -bordercolor white -border 4  -font /usr/share/fonts/truetype/arphic/ukai.ttc -pointsize %d label:\"%s\" \"cn_%d_%d.png\""%(s,word,i,s/12-1)) 
        i = i + 1 

for i in [12,24,36,48,60,72,84,96]:
    make_labels(i)
