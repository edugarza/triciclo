import sys
from pyspark import SparkContext
sc = SparkContext()

def get_edges(line):
    edge = line.strip().split(',')
    n1 = edge[0]
    n2 = edge[1]
    if n1 < n2:
         return (n1,n2)
    elif n1 > n2:
         return (n2,n1)
    else:
        pass #n1 == n2       

def relation(tupla):
    union = []
    for i in range(len(tupla[1])):
        union.append(((tupla[0],tupla[1][i]),'exists'))
        for j in range(i+1,len(tupla[1])):
            if tupla[1][i] < tupla[1][j]:
                union.append(((tupla[1][i],tupla[1][j]),('pending',tupla[0])))
            else:
                union.append(((tupla[1][j],tupla[1][i]),('pending',tupla[0])))
    return union
    
def possible_cycles(tupla):
    return (len(tupla[1])>= 2 and 'exists' in tupla[1])
    
def triciclo(tupla):
    triple = []
    for pos in tupla[1]:
        if pos != 'exists':
            triple.append((pos[1],tupla[0][0], tupla[0][1]))
    return triple
    
def get_cicles(sc, files):
    rdd = sc.parallelize([])
    for file in files:
        file_rdd = sc.textFile(file)
        rdd = rdd.union(file_rdd)
    adj = rdd.map(get_edges).filter(lambda x: x is not None).distinct()
    connected = adj.groupByKey().mapValues(list).flatMap(relation)
    triciclos = connected.groupByKey().mapValues(list).filter(possible_cycles).flatMap(triciclo)
    print(triciclos.collect())
    return triciclos.collect()

"Ejecicio 2."
if __name__ == "__main__":
    lista = []
    if len(sys.argv) <= 2:
        print(f"Uso: python3 {0} <file>")
    else:
        for i in range(len(sys.argv)):
            if i != 0:
                lista.append(sys.argv[i])
        get_cicles(sc,lista)