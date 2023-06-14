from tables import Pomodoro 
from collections import deque

class Task():

    def __init__(self, id=None, task=None, color=0, active=1, desc='None', *kwargs):

        self.idx = id
        self.task = task
        self.color = color 
        self.active = active 
        self.desc = desc 

class Database():

    def __init__(self):

        self.table=Pomodoro()

        self.tasks = None
        self.task_list = {}
        self.full_task_list = {}
        self.task_chain = {None:[]}

        self.load_tasks()

    def load_tasks(self):

        self.tasks = {}
        self.task_list = {}
        self.full_task_list = {}
        t = Task()

        self.tasks[t.idx] = t

        raw_tasks = self.table.tasks.getAll()

        for entry in raw_tasks:
            t = Task(**entry)
            self.tasks[t.idx] = t

            if t.idx not in self.task_list:
                self.task_list[t.idx] = []
            if t.task not in self.task_list:
                self.task_list[t.task] = []

            self.task_list[t.task].append(t.idx)

        self.full_task_list = dict(self.task_list)
        self.colors = {None:[0]}
        self.levels = 0

        if None in self.task_list:
            q = deque([[1,None,x] for x in self.task_list[None]])
            while q:
                level,parent,idx = q.popleft()
                if self.tasks[idx].active > 0:
                    q.extend([[level+1,idx,x] for x in self.task_list[idx]])

                    if idx not in self.colors: self.colors.update({idx:[]})
                    color_list = []
                    if parent in self.colors: color_list.extend(self.colors[parent])
                    self.colors[idx].extend(color_list)
                    self.colors[idx].append(self.tasks[idx].color)

                    if self.levels <= level: self.levels = level + 1

                else:
                    q2 = deque([[idx,x] for x in self.task_list[idx]])
                    del self.task_list[parent][self.task_list[parent].index(idx)]
                    while q2:
                        level2,parent2,idx2 = q2.popleft()
                        q2.extend([[level2+1,idx2,x] for x in self.task_list[idx2]])
                        del self.task_list[idx2]

            for idx,color_list in self.colors.items():
                length = len(color_list)
                if length < self.levels:
                    if length > 0:
                        self.colors[idx].extend([color_list[-1] for i in range(self.levels - length)])
                    else:
                        self.colors[idx].extend([0 for i in range(self.levels - length)])

        self.task_chain = {None:[]}
        for task in self.tasks.keys():
            self.task_chain.update({task:self.find_task(task)})

    def find_task_rec(self,idx,l):

        for i in range(0,len(l)):
            if l[i] == idx:
                return [(l[i],i)]

            if l[i] in self.task_list:
                rl = self.find_task_rec(idx,self.task_list[l[i]])
                if len(rl) > 0:
                    rl.insert(0,(l[i],i))
                    return rl

        return []

    def find_task(self, idx):

        if None not in self.task_list:
            return []
        else:
            rl = self.find_task_rec(idx,self.task_list[None])
            return rl
