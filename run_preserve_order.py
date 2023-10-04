import preserve_order

def run_preserve_order_obstruct(gens,max_k,min_k=2,order=1,track_extra_elements = False,add_extra_products=False,count=False,Print=False, tree=False,zero_esp_sum=True,time=False):
    cone=True
    i=min_k
    file=open(str(gens)+'_'+str(max_k)+'_'+str(min_k)+'.txt','w')
    file.close()
    if time:
        from time import time
        T=[]
        T.append(time())
        

    while i<max_k+1 and cone:
        cone=preserve_order.preserve_order_obstruct(gens,i,i,i,i,order,track_extra_elements,add_extra_products,count, Print, tree, zero_esp_sum)
        file=open(str(gens)+'_'+str(max_k)+'_'+str(min_k)+'.txt','a')
        file.write('k='+str(i)+'; found pre-cone: '+str(cone))
        
        if time:
            T.append(time())
            file.write('; '+'run time='+' '+str(round(T[i-min_k+1]-T[i-min_k],2))+' seconds')
        file.write('\n')
        file.close()
        i+=1
        if zero_esp_sum:
            i+=1
         
    return cone
