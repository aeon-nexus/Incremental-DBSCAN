from cluster import *
from pylab import *

class incdbscanner:
    
    dataSet = []
    count = 0
    visited = []
    curCores = []
    newCores = []
    Clusters = []
    Noise = 0
    num = 0
    
    def __init__(self):
        self.Noise = cluster('Noise')
    def incdbscan(self,D,eps,MinPts):
        #self.dataSet = D
        Noisepoints = []
        figure(1)
        title(r'INCREMENTAL DBSCAN Algorithm', fontsize=18)
        xlabel(r'Dim 1',fontsize=17)
        ylabel(r'Dim 2', fontsize=17)
        
        for point in D:
            self.dataSet.append(point)
            self.incrementalAdd(point,eps,MinPts)
            for core in self.newCores:
                if core not in self.curCores:
                    self.curCores.append(core)
        for clust in self.Clusters:
            plot(clust.getX(),clust.getY(),'o',label=clust.name)
            hold(True)
        print("Noise \n")
        print(self.Noise.getPoints())
        for noisep in self.Noise.getPoints():
            Noisepoints.append(noisep)
        for pts in Noisepoints:
            print("\nNoise:"+str(Noisepoints))
            print("\nPoint:"+str(pts))
            for clust in self.Clusters:
                print("Cluster Points ")
                clust.printPoints()
                if clust.has(pts):
                    print("\n Point to REMOVE"+str(pts))
                    self.Noise.remPoint(pts)
        print("Noise 2 \n")
        print(self.Noise.getPoints())
        if len(self.Noise.getPoints()) > 0:
            plot(self.Noise.getX(),self.Noise.getY(),'o',label='Noise')
        hold(False)
        #legend(loc='lower left')
        grid(True)
        margins(0.05)
        show()
        while(True):
            figure(2)
            clf()
            title(r'INCREMENTAL DBSCAN After Deletion', fontsize=18)
            xlabel(r'Dim 1',fontsize=17)
            ylabel(r'Dim 2', fontsize=17)
            print("Enter point to delete")
            xValue = input('Enter X Value')
            yValue = input('Enter Y Value')
            #deletePoints = list(self.Clusters[2].getPoints())
            #for pts in deletePoints:
            #    self.incrementalDelete(pts,eps,MinPts)
            self.incrementalDelete([xValue,yValue],eps,MinPts)        
            for clust in self.Clusters:
                clust.printPoints()
                plot(clust.getX(),clust.getY(),'o',label=clust.name)
                hold(True)
            if len(self.Noise.getPoints()) > 0:
                self.Noise.printPoints()
                plot(self.Noise.getX(),self.Noise.getY(),'o',label='Noise')
            hold(False)
            legend(loc='lower left')
            grid(True)
            margins(0.05)
            show()

    def expandCluster(self,point,NeighbourPoints,C,eps,MinPts):
        self.visited = []
        
        C.addPoint(point)
        
        for p in NeighbourPoints:
            if p not in self.visited:
                self.visited.append(p)
                np = self.regionQuery(p,eps)
                if len(np) >= MinPts:
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)
                    
            for c in self.Clusters:
                if not c.has(p):
                    if not C.has(p):
                        C.addPoint(p)
                        
            if len(self.Clusters) == 0:
                if not C.has(p):
                    C.addPoint(p)
                        
        self.Clusters.append(C)
        print("\n"+C.name+"\n")
        C.printPoints()
        
                    
                
                     
    def regionQuery(self,P,eps):
        result = []
        for d in self.dataSet:
            if (((d[0]-P[0])**2 + (d[1] - P[1])**2)**0.5) <= eps:
                result.append(d)
        return result

    def incrementalAdd(self,p,eps,Minpts):
        self.num = self.num + 1
        print("\nADDING point "+str(self.num))
        self.visited = []
        self.newCores = []
        UpdSeedIns = []
        foundClusters = []
        NeighbourPoints = self.regionQuery(p,eps)
        if len(NeighbourPoints) >= Minpts:
            self.newCores.append(p)
        self.visited.append(p)
        for pt in NeighbourPoints:
            if pt not in self.visited:
                self.visited.append(pt)
                np = self.regionQuery(pt,eps)
                if len(np) >= Minpts:
                    for n in np:
                        if n not in NeighbourPoints:
                            NeighbourPoints.append(n)
                    if pt not in self.curCores:
                        self.newCores.append(pt)
        for core in self.newCores:
            corehood = self.regionQuery(core,eps)
            print("the corehood is:", corehood)
            for elem in corehood:
                print("The Minpts are:", Minpts)
                print(self.regionQuery(elem, eps))
                if self.regionQuery(elem, eps) >= Minpts:

                    if elem not in UpdSeedIns:
                        UpdSeedIns.append(elem)
        if len(UpdSeedIns) < 1:
            self.Noise.addPoint(p)
        else:
            findCount = 0
            for seed in UpdSeedIns:
                for clust in self.Clusters:
                    if clust.has(seed):
                        findCount += 1
                        if clust.name not in foundClusters:
                            foundClusters.append(clust.name)
                            break
            if len(foundClusters) == 0:
                name = 'Cluster' + str(self.count)
                C = cluster(name)
                self.count += 1
                self.expandCluster(UpdSeedIns[0],self.regionQuery(UpdSeedIns[0],eps),C,eps,Minpts)
            elif len(foundClusters) == 1:
                originalCluster = -1
                newCluster = -1
                for c in self.Clusters:
                    if c.name == foundClusters[0]:
                        originalCluster = c
                        newCluster = c
                newCluster.addPoint(p)
                if len(UpdSeedIns) > findCount:
                    for seed in UpdSeedIns:
                        if not newCluster.has(seed):
                            newCluster.addPoint(seed)
                self.Clusters.remove(originalCluster)
                self.Clusters.append(newCluster)
            else:
                masterCluster = -1
                originalCluster = -1
                for c in self.Clusters:
                    if c.name == foundClusters[0]:
                        masterCluster = c
                        originalCluster = c
                for clusname in foundClusters:
                    for clus in self.Clusters:
                        if clus.name == clusname:
                            for cluspoints in clus.getPoints():
                                if not masterCluster.has(cluspoints):
                                    masterCluster.addPoint(cluspoints)
                if len(UpdSeedIns) > findCount:
                    for seed in UpdSeedIns:
                        if not masterCluster.has(seed):
                            masterCluster.addPoint(seed)
                self.Clusters.remove(originalCluster)
                self.Clusters.append(masterCluster)
    
    def incrementalDelete(self,p,eps,Minpts):
        print("Point to Delete: ",str(p))
        self.newCores = []
        obsoleteCores = []
        UpdSeedDel = []
        Neighbourhood = self.regionQuery(p,eps)
        Neighbourhood.remove(p)
        self.dataSet.remove(p)
        if p in self.curCores:
            self.curCores.remove(p)
            obsoleteCores.append(p)
        for core in self.curCores:
            np = self.regionQuery(core,eps)
            if len(np) >= Minpts:
                self.newCores.append(core)
            else:
                obsoleteCores.append(core)    
        for core in obsoleteCores:
            np = self.regionQuery(core,eps)
            for point in np:
                if len(self.regionQuery(point,eps)) >= Minpts and cmp(point,p) != 0:
                    UpdSeedDel.append(point)
        print("\nUpdSeedDel:"+str(UpdSeedDel)+"\nCurCores:"+str(self.curCores)+"\nNewCores:"+str(self.newCores))
        if len(UpdSeedDel) <= 0:
            removePts = []
            for pt in Neighbourhood:
                if len(self.regionQuery(pt,eps)) < Minpts:
                    removePts.append(pt)
            for clust in self.Clusters:
                if clust.has(p):
                    clust.remPoint(p)
                    if len(clust.getPoints()) == 0:
                        self.Clusters.remove(clust)
                    else:
                        if len(Neighbourhood) == len (removePts):
                            for poin in clust.getPoints():
                                self.Noise.addPoint(poin)
                            self.Clusters.remove(clust)
                        else:
                            for poin in removePts:
                                clust.remPoint(poin)
                                self.Noise.addPoint(poin)                        
                    break        
            if self.Noise.has(p):
                self.Noise.remPoint(p)
        else:
            directlyConnected = True
            np = self.regionQuery(UpdSeedDel[0],eps)
            for Seed in UpdSeedDel:
                if Seed not in np:
                    directlyConnected = False 
            if directlyConnected:
                print("Procedure Reached")
                for point in Neighbourhood:
                    isNoise = True
                    neighbour = self.regionQuery(point,eps)
                    for pt in neighbour:
                        if pt in self.newCores:
                            isNoise = False
                            break
                    if isNoise:
                        print("\nFound Noise:", str(point))
                        for clust in self.Clusters:
                            if clust.has(point):
                                clust.remPoint(point)
                                if len(clust.getPoints()) == 0:
                                    self.Clusters.remove(clust)
                                break
                        if not self.Noise.has(point):
                            self.Noise.addPoint(point)
                for clust in self.Clusters:
                    if clust.has(p):
                        clust.remPoint(p)
                        if len(clust.getPoints()) == 0:
                            self.Clusters.remove(clust)
                        break
            else:
                C = -1
                self.visited = []
                visitedSeeds = []
                newCluster = -1
                for clust in self.Clusters:
                    if clust.has(p):
                        C=clust
                        break
                if C != -1:    
                    self.Clusters.remove(C)
                    for seed in UpdSeedDel:
                        neighbour = []
                        if seed not in visitedSeeds:
                            name = 'Cluster' + str(self.count)
                            self.count += 1
                            newCluster = cluster(name)
                            visitedSeeds.append(seed)
                            if seed not in self.visited:
                                self.visited.append(seed)
                            newCluster.addPoint(seed)
                            neighbour = self.regionQuery(seed,eps)
                            for pt in neighbour:
                                if pt not in self.visited:
                                    self.visited.append(pt)
                                if pt in UpdSeedDel:
                                    if pt not in visitedSeeds:
                                        visitedSeeds.append(pt)
                                np =  self.regionQuery(pt,eps)
                                if len(np) >= Minpts:
                                    for poin in np:
                                        if poin not in self.visited:
                                            neighbour.append(poin)
                                if not newCluster.has(pt):
                                    newCluster.addPoint(pt)
                            if len(visitedSeeds) == len(UpdSeedDel):
                                self.Clusters.append(newCluster)
                                break
                            else:
                                self.Clusters.append(newCluster)
        self.curCores = list(self.newCores)
