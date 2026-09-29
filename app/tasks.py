from __future__ import annotations

class Task:
    def __init__(self,title:str,done:bool=False)->None:
        title=title.strip()
        if not title:
            raise ValueError("待办内容不可以为空")
        self.title=title
        self.done=done

    def finish(self)->None:
        self.done=True

    def reopen(self)->None:
        self.done=False

    def to_dict(self)->dict:
        return {"title":self.title,"done":self.done}

    def __str__(self)->str:
        return f"[{self.mark}] {self.title}"
    
    @property
    def mark(self)->str:
        return "√" if self.done else " "
    
    @classmethod
    def from_dict(cls,data:dict)->"Task":
        """转化为一个Task的对象"""
        return cls(title=data["title"],done=data.get("done",False))


class TodoList:
    def __init__(self,tasks:list[Task]|None=None)->None:
        self.tasks=tasks if tasks is not None else []

    def __len__(self)->int:
        return len(self.tasks)

    def check_index(self,index:int)->None:
        """只是检查所以没有返回值"""
        if not self.tasks:
            raise ValueError("还没有待办任务，先add一条")
        if not 1<=index<=len(self.tasks):
            raise ValueError(f"序号必须在1到{len(self.tasks)}之间")

    def add(self,title:str)->Task:
        """返回新添加的对象"""
        task=Task(title)
        self.tasks.append(task)
        return task

    def finish(self,index:int)->Task:
        self.check_index(index)
        task=self.tasks[index-1]
        task.finish()
        return task

    def reopen(self,index:int)->Task:
        self.check_index(index)
        task=self.tasks[index-1]
        task.reopen()
        return task

    def remove(self,index:int)->Task:
        self.check_index(index)
        return self.tasks.pop(index-1)

    def search(self,keyword:str="")->list[Task]:
        keyword=keyword.strip()
        if not keyword:
            return list(self.tasks)
        return [task for task in self.tasks if keyword in task.title]

    def unfinished(self)->list[Task]:
        return [t for t in self.tasks if not t.done]

    def to_lines(self)->list[str]:
        if not self.tasks:
            return {"还没有待办，用add加一条"}
        lines=[f"{i:>2}.{t}"for i,t in enumerate(self.tasks,start=1)]
        lines.append("")
        lines.append(f"一共{len(self.tasks)}条，未完成{len(self.unfinished())}条")
        return lines
        

