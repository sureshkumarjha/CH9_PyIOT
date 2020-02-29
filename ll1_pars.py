productions = ['A->C','B->d','C->h']
first_list = []
follow_list = [['$']]
distinct_elements = []

for h in productions:
    list_n = h.split('->')
    distinct_elements.append(list_n[0])

print(distinct_elements)

def find_first(production,i,first,element):
    lister = production.split('->')
    lister_1 = list(lister[1])
    
    j = lister_1[0]
    if j.isupper() == False and j == element:
        first.append(j)
    elif i < len(productions)-1:
        print(i)
        find_first(productions[i+1],i+1,first,lister[0])
    else:
        print("done")

def find_follow(production,i,follow,element):
    lister = production.split('->')
    lister_1 = list(lister[1])
    
    
    

def run(productions):
    for j in range(len(productions)):
        r = 0
        i = 0
        first = []
        find_first(productions[j],i,first,distinct_elements[j])
        first_list.append(first)
    print(first_list)
        
            
run(productions)      


            
                


            
