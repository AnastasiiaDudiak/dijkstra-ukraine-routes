import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import heapq
import math
import os
import matplotlib.image as mpimg
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from matplotlib import patheffects
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Двосторонні автомобільні сполучення та відстані з таблиці 1 методички.
ROADS = [
('Вінниця','Житомир',127),('Вінниця','Київ',267),('Вінниця','Кропивницький',320),
('Вінниця','Миколаїв',428),('Вінниця','Одеса',423),('Вінниця','Черкаси',341),
('Вінниця','Чернівці',276),('Дніпро','Донецьк',248),('Дніпро','Запоріжжя',85),
('Дніпро','Кропивницький',244),('Дніпро','Кривий Ріг',146),('Дніпро','Полтава',160),
('Дніпро','Харків',218),('Донецьк','Луганськ',156),('Донецьк','Маріуполь',113),
('Донецьк','Харків',294),('Запоріжжя','Мелітополь',125),
('Івано-Франківськ','Тернопіль',133),('Івано-Франківськ','Ужгород',293),
('Київ','Житомир',140),('Київ','Полтава',340),('Київ','Суми',333),
('Київ','Черкаси',189),('Київ','Чернігів',148),('Кропивницький','Полтава',246),
('Луганськ','Харків',325),('Львів','Івано-Франківськ',134),('Львів','Луцьк',151),
('Львів','Рівне',211),('Львів','Тернопіль',127),('Львів','Ужгород',268),
('Львів','Чернівці',268),('Мелітополь','Маріуполь',192),
('Мелітополь','Сімферополь',250),('Миколаїв','Херсон',69),('Рівне','Житомир',188),
('Рівне','Луцьк',73),('Рівне','Тернопіль',155),('Харків','Полтава',143),
('Херсон','Мелітополь',231),('Хмельницький','Вінниця',119),
('Хмельницький','Житомир',183),('Хмельницький','Рівне',194),
('Хмельницький','Тернопіль',112),('Хмельницький','Чернівці',187),
('Суми','Харків',184),('Черкаси','Полтава',233),('Полтава','Суми',175),
('Чернігів','Суми',306),('Сімферополь','Севастополь',81)]

# Орієнтовні географічні координати міст (довгота, широта) для розміщення графа.
COORDS = {
'Вінниця':(28.47,49.23),'Житомир':(28.66,50.25),'Київ':(30.52,50.45),
'Кропивницький':(32.26,48.51),'Миколаїв':(31.99,46.98),'Одеса':(30.73,46.48),
'Черкаси':(32.06,49.44),'Чернівці':(25.94,48.29),'Дніпро':(35.05,48.46),
'Донецьк':(37.80,48.00),'Запоріжжя':(35.14,47.84),'Кривий Ріг':(33.40,47.91),
'Полтава':(34.55,49.59),'Харків':(36.23,49.99),'Луганськ':(39.31,48.57),
'Маріуполь':(37.55,47.10),'Мелітополь':(35.37,46.85),
'Івано-Франківськ':(24.71,48.92),'Тернопіль':(25.59,49.55),
'Ужгород':(22.30,48.62),'Суми':(34.80,50.91),'Чернігів':(31.29,51.50),
'Львів':(24.03,49.84),'Луцьк':(25.33,50.75),'Рівне':(26.25,50.62),
'Сімферополь':(34.10,44.95),'Херсон':(32.62,46.64),
'Хмельницький':(26.99,49.42),'Севастополь':(33.53,44.60)}

# Спрощений контур України для орієнтації на графі. Це не GIS-карта
# і не використовується для обчислення довжин автомобільних маршрутів.
UKRAINE_OUTLINE = [
 (22.15,48.42),(22.36,48.75),(22.14,49.05),(22.55,49.13),
 (22.57,49.46),(22.90,49.60),(22.72,49.93),(23.20,50.10),
 (23.55,50.58),(24.10,50.82),(24.13,51.45),(24.70,51.58),
 (25.12,51.92),(25.85,51.92),(26.35,51.75),(27.10,51.62),
 (27.65,51.58),(28.20,51.58),(28.90,51.60),(29.25,51.47),
 (29.75,51.48),(30.25,51.52),(30.85,51.78),(31.30,52.12),
 (31.75,52.12),(32.28,52.32),(32.75,52.18),(33.25,52.35),
 (33.75,52.34),(34.25,51.95),(34.65,51.90),(35.20,51.65),
 (35.72,51.32),(36.20,50.85),(36.65,50.45),(37.12,50.42),
 (37.50,50.18),(37.90,49.95),(38.15,49.88),(38.60,49.98),
 (39.20,49.65),(39.72,49.52),(40.15,49.20),(39.75,48.90),
 (39.95,48.55),(39.72,48.30),(39.80,47.85),(39.30,47.82),
 (38.95,47.92),(38.45,47.75),(38.00,47.55),(37.70,47.10),
 (37.15,46.95),(36.65,46.78),(36.10,46.70),(35.55,46.50),
 (35.12,46.25),(34.80,46.20),(34.55,46.00),(34.35,45.75),
 (34.75,45.52),(35.10,45.38),(35.00,45.08),(34.55,44.82),
 (34.20,44.78),(33.75,44.40),(33.25,44.38),(33.05,44.60),
 (32.50,45.25),(32.45,45.72),(32.65,46.15),(32.15,46.32),
 (31.70,46.45),(31.10,46.55),(30.72,46.28),(30.20,45.98),
 (29.75,45.55),(29.55,45.42),(29.75,45.95),(29.65,46.35),
 (29.15,46.42),(28.90,46.52),(28.25,46.45),(28.10,46.70),
 (28.18,47.10),(27.60,47.42),(27.18,47.53),(26.68,48.20),
 (26.10,48.26),(25.62,47.92),(24.95,47.95),(24.35,47.96),
 (23.90,47.98),(23.45,48.05),(22.95,48.05),(22.60,48.15)
]

LABEL_OFFSETS = {
 'Львів':(-10,9),'Луцьк':(-11,10),'Рівне':(8,10),
 'Тернопіль':(-15,-12),'Івано-Франківськ':(-15,-12),
 'Ужгород':(-5,-13),'Чернівці':(-2,-13),
 'Хмельницький':(-8,-14),'Житомир':(-7,10),
 'Вінниця':(-8,-14),'Київ':(0,12),'Чернігів':(0,12),
 'Суми':(0,12),'Черкаси':(0,-13),'Полтава':(0,12),
 'Харків':(0,12),'Кропивницький':(0,-14),
 'Дніпро':(10,10),'Запоріжжя':(12,-10),
 'Кривий Ріг':(-12,-12),'Донецьк':(0,12),
 'Луганськ':(0,12),'Маріуполь':(10,-12),
 'Мелітополь':(12,-12),'Миколаїв':(12,8),
 'Одеса':(-5,-14),'Херсон':(12,-11),
 'Сімферополь':(12,-10),'Севастополь':(-10,-12)
}

class RoadGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self.reset()
    def reset(self):
        self.graph.clear()
        self.graph.add_weighted_edges_from(ROADS)
    def add_city(self, name):
        if not name.strip(): raise ValueError('Введіть назву міста.')
        if name in self.graph: raise ValueError('Таке місто вже існує.')
        self.graph.add_node(name)
    def remove_city(self, name):
        if name not in self.graph: raise ValueError('Міста немає в графі.')
        self.graph.remove_node(name)
    def add_road(self, a, b, weight):
        if a == b: raise ValueError('Міста мають бути різними.')
        if a not in self.graph or b not in self.graph: raise ValueError('Оберіть наявні міста.')
        if weight <= 0 or not math.isfinite(weight): raise ValueError('Відстань має бути додатною.')
        self.graph.add_edge(a,b,weight=weight)
    def remove_road(self,a,b):
        if not self.graph.has_edge(a,b): raise ValueError('Такої дороги немає.')
        self.graph.remove_edge(a,b)
    def dijkstra_steps(self,start,target):
        if start not in self.graph or target not in self.graph:
            raise ValueError('Оберіть наявні початкове та кінцеве міста.')
        dist={v:float('inf') for v in self.graph.nodes}
        prev={}
        dist[start]=0
        queue=[(0,start)]
        visited=set()
        steps=[]
        while queue:
            d,u=heapq.heappop(queue)
            if u in visited: continue
            visited.add(u)
            for v,attrs in sorted(self.graph[u].items()):
                nd=d+attrs['weight']
                if nd < dist[v]:
                    dist[v]=nd
                    prev[v]=u
                    heapq.heappush(queue,(nd,v))
            steps.append((u,visited.copy(),dist.copy()))
            if u==target: break
        if dist[target]==float('inf'):
            return steps, [], None
        path=[]
        at=target
        while at!=start:
            path.append(at)
            at=prev[at]
        path.append(start)
        path.reverse()
        return steps,path,dist[target]

class App:
    def __init__(self,root):
        self.root=root
        self.root.title('Лабораторна №5 — алгоритм Дейкстри')
        self.root.geometry('1320x820')
        self.model=RoadGraph()
        self.steps=[]; self.path=[]; self.distance=None; self.step_index=0
        self.after_id=None
        self.pending_city=None
        self.pos=dict(COORDS)
        self.build_ui()
        self.refresh()
    def build_ui(self):
        outer=ttk.Frame(self.root,padding=10); outer.pack(fill='both',expand=True)
        left=ttk.Frame(outer,width=320);left.pack(side='left',fill='y',padx=(0,10))
        right=ttk.Frame(outer);right.pack(side='left',fill='both',expand=True)
        ttk.Label(left,text='Пошук маршруту',font=('Arial',15,'bold')).pack(anchor='w',pady=(0,10))
        ttk.Label(left,text='Початкове місто').pack(anchor='w')
        self.start=ttk.Combobox(left,state='readonly',width=35);self.start.pack(fill='x',pady=3)
        ttk.Label(left,text='Цільове місто').pack(anchor='w')
        self.target=ttk.Combobox(left,state='readonly',width=35);self.target.pack(fill='x',pady=3)
        ttk.Button(left,text='Знайти найкоротший шлях',command=self.search).pack(fill='x',pady=(10,3))
        ttk.Button(left,text='Наступний крок',command=self.next_step).pack(fill='x',pady=3)
        ttk.Button(left,text='Автоматична візуалізація',command=self.animate).pack(fill='x',pady=3)
        ttk.Button(left,text='Показати результат',command=self.show_result).pack(fill='x',pady=3)
        ttk.Separator(left).pack(fill='x',pady=14)
        ttk.Label(left,text='Редагування графа',font=('Arial',13,'bold')).pack(anchor='w')
        ttk.Button(left,text='Додати місто',command=self.add_city).pack(fill='x',pady=3)
        ttk.Button(left,text='Видалити місто',command=self.remove_city).pack(fill='x',pady=3)
        ttk.Button(left,text='Додати / змінити дорогу',command=self.add_road).pack(fill='x',pady=3)
        ttk.Button(left,text='Видалити дорогу',command=self.remove_road).pack(fill='x',pady=3)
        ttk.Button(left,text='Відновити початковий граф',command=self.reset).pack(fill='x',pady=(10,3))
        ttk.Separator(left).pack(fill='x',pady=12)
        self.info=tk.StringVar(value='')
        ttk.Label(left,textvariable=self.info,wraplength=295,justify='left').pack(anchor='w')
        ttk.Label(left,text='Журнал пошуку',font=('Arial',11,'bold')).pack(anchor='w',pady=(15,4))
        self.log=tk.Text(left,height=13,width=38,wrap='word');self.log.pack(fill='both',expand=True)
        self.fig=Figure(figsize=(10,7),dpi=100)
        self.ax=self.fig.add_subplot(111)
        self.canvas=FigureCanvasTkAgg(self.fig,master=right)
        self.canvas.get_tk_widget().pack(fill='both',expand=True)
        self.canvas.mpl_connect('button_press_event', self.on_map_click)
        self.canvas.mpl_connect('key_press_event', self.on_map_key)
    def refresh(self):
        cities=sorted(self.model.graph.nodes)
        a=self.start.get();b=self.target.get()
        self.start['values']=cities;self.target['values']=cities
        self.start.set(a if a in cities else ('Львів' if 'Львів' in cities else (cities[0] if cities else '')))
        self.target.set(b if b in cities else ('Київ' if 'Київ' in cities else (cities[-1] if cities else '')))
        self.info.set(f'Вершин: {self.model.graph.number_of_nodes()} | Ребер: {self.model.graph.number_of_edges()}')
        self.draw()
    def draw(self,visited=None,current=None,show_path=False):
        self.ax.clear()
        ax=self.ax
        ax.set_facecolor('#eaf3fa')
        graph=self.model.graph
        missing=[n for n in graph if n not in self.pos]
        if missing:
            raise ValueError('Для нових міст потрібно вибрати місце на карті: '+', '.join(missing))
        pos={n:self.pos[n] for n in graph}

        # Географічна підкладка без полів: точна прив'язка пікселів до координат.
        # Міста і карта використовують ту саму довготу/широту.
        # Географічна підкладка з реальними береговими лініями та державними межами.
        # Файл PNG створено за картографічними даними Basemap (GSHHG).
        # Підкладка не впливає на відстані, задані методичкою.
        map_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              'ukraine_geography.png')
        if os.path.exists(map_path):
            ax.imshow(mpimg.imread(map_path),extent=(21.2,41.2,43.7,53.0),
                      origin='upper',interpolation='bilinear',zorder=0)
        ax.text(30.4,47.0,'У К Р А Ї Н А',color='#8d9b9e',
                fontsize=16,weight='bold',ha='center',zorder=1,alpha=.35)
        ax.text(30.2,45.15,'Чорне море',color='#5e9fbf',fontsize=10,
                style='italic',ha='center',zorder=1)
        ax.text(37.1,46.0,'Азовське море',color='#5e9fbf',fontsize=9,
                style='italic',ha='center',zorder=1)

        nx.draw_networkx_edges(graph,pos,ax=ax,edge_color='#9aabb4',
                               width=1.25,alpha=.72)
        if show_path and len(self.path)>1:
            pairs=list(zip(self.path,self.path[1:]))
            nx.draw_networkx_edges(graph,pos,edgelist=pairs,ax=ax,
                                   edge_color='#ed7048',width=4.2,alpha=.95)
        colors=['#f59e0b' if n==current else
                '#9fdbc2' if visited and n in visited else
                '#ffffff' for n in graph]
        nx.draw_networkx_nodes(graph,pos,ax=ax,node_color=colors,
                               node_size=105,edgecolors='#32799b',linewidths=1.5)
        if show_path and self.path:
            nx.draw_networkx_nodes(graph,pos,nodelist=self.path,ax=ax,
                                   node_color='#f5a181',node_size=125,
                                   edgecolors='#b63d22',linewidths=1.5)
        for name,(x,y) in pos.items():
            dx,dy=LABEL_OFFSETS.get(name,(7,8))
            annotation=ax.annotate(name,(x,y),xytext=(dx,dy),
                     textcoords='offset points',fontsize=8,
                     ha='center',va='center',color='#203747',zorder=6)
            annotation.set_path_effects([patheffects.withStroke(linewidth=3,
                                                                 foreground='#f7f4e9')])
        ax.set_xlim(21.2,max(41.2,max((p[0] for p in pos.values()),default=40)+.5))
        ax.set_ylim(43.7,53.0)
        ax.set_aspect(1.5,adjustable='box')
        ax.set_title('Автомобільні маршрути України · зважений граф',
                     fontsize=14,pad=18,color='#203747',weight='bold')
        ax.set_axis_off()
        self.fig.patch.set_facecolor('#eaf3fa')
        self.fig.tight_layout(pad=1.2)
        if self.pending_city:
            ax.text(.5,.025,f'Клацніть на карті, щоб розмістити: {self.pending_city} (Esc — скасувати)',
                    transform=ax.transAxes,ha='center',va='bottom',fontsize=10,
                    color='#a63a25',weight='bold',zorder=20)
        self.canvas.draw_idle()
    def on_map_click(self,event):
        if not self.pending_city or event.inaxes is not self.ax or event.button != 1:
            return
        if event.xdata is None or event.ydata is None:
            return
        lon,lat=float(event.xdata),float(event.ydata)
        if not (22.0 <= lon <= 40.3 and 44.3 <= lat <= 52.5):
            messagebox.showwarning('Розміщення міста','Оберіть точку в межах України, а не за краєм карти.')
            return
        name=self.pending_city
        self.pending_city=None
        self.pos[name]=(lon,lat)
        self.edit(lambda:self.model.add_city(name))
    def on_map_key(self,event):
        if event.key == 'escape' and self.pending_city:
            self.pending_city=None
            self.draw()
    def stop_animation(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id);self.after_id=None
    def clear_search(self):
        self.stop_animation();self.steps=[];self.path=[];self.distance=None;self.step_index=0
        self.log.delete('1.0','end')
    def search(self):
        self.clear_search()
        try:
            self.steps,self.path,self.distance=self.model.dijkstra_steps(self.start.get(),self.target.get())
        except ValueError as e:
            messagebox.showerror('Помилка',str(e));return
        self.log.insert('end',f'Старт: {self.start.get()}\nЦіль: {self.target.get()}\n')
        self.log.insert('end',f'Заплановано кроків: {len(self.steps)}\n')
        self.draw()
    def next_step(self):
        if not self.steps:
            self.search()
            if not self.steps:return
        if self.step_index<len(self.steps):
            u,visited,dist=self.steps[self.step_index]
            self.step_index+=1
            self.log.insert('end',f'{self.step_index}. {u}: {dist[u]:g} км; відвідано {len(visited)}\n')
            self.log.see('end')
            self.draw(visited,u,False)
        if self.step_index==len(self.steps):
            self.draw(self.steps[-1][1],None,True)
            self.log.insert('end','Пошук завершено. Натисніть «Показати результат».\n')
    def animate(self):
        if not self.steps:self.search()
        if not self.steps:return
        self.stop_animation()
        def tick():
            self.after_id=None
            if self.step_index<len(self.steps):
                self.next_step()
                if self.step_index<len(self.steps):self.after_id=self.root.after(550,tick)
        tick()
    def show_result(self):
        if not self.steps:self.search()
        if not self.steps:return
        window=tk.Toplevel(self.root)
        window.title('Результат пошуку Дейкстри')
        window.geometry('600x260')
        frame=ttk.Frame(window,padding=24);frame.pack(fill='both',expand=True)
        if self.path:
            msg=' → '.join(self.path)
            text=f'Найкоротший маршрут:\n{msg}\n\nЗагальна відстань: {self.distance:g} км'
        else:
            text='Маршрут між вибраними містами відсутній.'
        ttk.Label(frame,text=text,wraplength=545,justify='left',font=('Arial',12)).pack(anchor='w')
        self.draw(self.steps[-1][1],None,True)
    def edit(self,operation):
        self.clear_search()
        try:operation()
        except ValueError as e:messagebox.showerror('Помилка',str(e))
        self.refresh()
    def add_city(self):
        name=simpledialog.askstring('Нове місто','Назва міста:',parent=self.root)
        if name is None:return
        name=name.strip()
        if not name or name in self.model.graph:
            messagebox.showerror('Помилка','Введіть нову, непорожню назву міста.')
            return
        self.clear_search()
        self.pending_city=name
        self.draw()
        messagebox.showinfo('Розміщення міста',
            f'Клацніть лівою кнопкою на карті там, де має бути «{name}».\nДля скасування натисніть Esc на карті.')
    def remove_city(self):
        name=simpledialog.askstring('Видалення міста','Назва міста:',parent=self.root)
        if name is not None:self.edit(lambda:self.model.remove_city(name.strip()))
    def add_road(self):
        a=simpledialog.askstring('Дорога','Перше місто:',parent=self.root)
        if a is None:return
        b=simpledialog.askstring('Дорога','Друге місто:',parent=self.root)
        if b is None:return
        w=simpledialog.askfloat('Дорога','Відстань, км:',parent=self.root,minvalue=0.001)
        if w is not None:self.edit(lambda:self.model.add_road(a.strip(),b.strip(),w))
    def remove_road(self):
        a=simpledialog.askstring('Видалити дорогу','Перше місто:',parent=self.root)
        if a is None:return
        b=simpledialog.askstring('Видалити дорогу','Друге місто:',parent=self.root)
        if b is not None:self.edit(lambda:self.model.remove_road(a.strip(),b.strip()))
    def reset(self):
        self.pending_city=None
        self.clear_search();self.model.reset();self.pos=dict(COORDS);self.refresh()

if __name__=='__main__':
    root=tk.Tk()
    App(root)
    root.mainloop()
