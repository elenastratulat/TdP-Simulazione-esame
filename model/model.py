import copy
import itertools
from collections import defaultdict

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}
        self._artist = []
        self._bestPath = []


    def getPath(self, source):
        self._bestPath = []

        partial = [self._idMap[int(source)]]

        for _, v, data in self._graph.out_edges(self._idMap[int(source)], data=True):
            partial.append(v)

            self._ricorsione(partial, data["weight"])
            partial.pop()

        return self._bestPath

    def _ricorsione(self, partial,lastWeight):
        # update best solution
        if len(partial) > len(self._bestPath):
            self._bestPath = copy.deepcopy(partial)

        current = partial[-1]

        for _, successor, data in self._graph.out_edges(current, data=True):

            weight = data["weight"]

            # strictly decreasing weights
            if weight > lastWeight:

                # simple path
                if successor not in partial:
                    partial.append(successor)

                    self._ricorsione(partial, weight)

                    partial.pop()

    def buildGraph(self, genere):
        self._graph.clear()
        self._artist = DAO.getAllArtistsByGenre(genere)
        for a in self._artist:
            self._idMap[a.ArtistId] = a

        self._graph.add_nodes_from(self._artist)

        custom_artist_list = DAO.getCostumerArtistsCount(genere)

        # customerMap[cliente][artista] = brani acquistati
        customerMap = defaultdict(dict)
        artist_popularity= defaultdict(int)
        for customer_id, artist_id, ntracks in custom_artist_list:
            customerMap[customer_id][artist_id] = ntracks
            artist_popularity[artist_id] += ntracks

        # arco tra A e B se almeno un cliente ha comprato da entrambi
        for customer_id, artisti in customerMap.items():
            for idA, idB in itertools.combinations(artisti.keys(), 2):
                if idA not in self._idMap or idB not in self._idMap:
                    continue
                a, b = self._idMap[idA], self._idMap[idB]
                pA, pB = artist_popularity[idA], artist_popularity[idB]
                peso = pA + pB
                if pA > pB:
                    self._graph.add_edge(a, b, weight=peso)
                elif pB > pA:
                    self._graph.add_edge(b, a, weight=peso)
                else:
                    self._graph.add_edge(a, b, weight=peso)
                    self._graph.add_edge(b, a, weight=peso)

    def getBestArtist(self):

        bestArtist = None
        bestScore = None

        for v in self._graph.nodes():

            outWeight = 0
            for _, _, data in self._graph.out_edges(v, data=True):
                outWeight += data["weight"]

            inWeight = 0
            for _, _, data in self._graph.in_edges(v, data=True):
                inWeight += data["weight"]

            score = outWeight - inWeight

            if bestScore is None or score > bestScore:
                bestScore = score
                bestArtist = v

        return bestArtist.Name, bestScore

    def getTop5Edges(self):

        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )

        return edges[:5]


    def getGenres(self):
        return DAO.getAllGenres()

    def getArtists(self):
        return self._graph.nodes()

    def getNumNodes(self):
        return len(self._graph.nodes())

    def getNumEdges(self):
        return len(self._graph.edges())