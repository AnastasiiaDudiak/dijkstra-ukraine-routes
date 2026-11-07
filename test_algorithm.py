from main import RoadGraph, ROADS

def run():
    model=RoadGraph()
    assert model.graph.number_of_edges()==50
    assert len(ROADS)==50
    assert model.graph.number_of_nodes()==len(set([c for a,b,w in ROADS for c in (a,b)]))
    steps,path,dist=model.dijkstra_steps('Львів','Київ')
    import networkx as nx
    assert dist==nx.shortest_path_length(model.graph,'Львів','Київ',weight='weight')
    assert path[0]=='Львів' and path[-1]=='Київ'
    model.remove_road(path[0],path[1])
    _,_,new_dist=model.dijkstra_steps('Львів','Київ')
    assert new_dist is None or new_dist>=dist
    model.add_city('Тестове місто')
    assert model.dijkstra_steps('Львів','Тестове місто')[2] is None
    model.add_road('Львів','Тестове місто',10)
    assert model.dijkstra_steps('Львів','Тестове місто')[2]==10
    model.remove_city('Тестове місто')
    print('Усі перевірки успішні. Львів → Київ:', ' → '.join(path), '=',dist,'км')
if __name__=='__main__':run()
