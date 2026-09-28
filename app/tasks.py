from __future__ import annotations

def add_task(tasks:list[dict],title:str)->dict:
    """新增一条待办，返回新增的那一条"""
    title=title.strip()
    if not title:
        raise ValueError("待办内容不可以为空")
    task = {"title": title, "done": False}
    tasks.append(task)
    return task

def check_index(tasks:list[dict],index:int)->None:
    """检查序号是否合法，从1开始，不合法就抛valueError"""
    if not tasks:
        raise ValueError("清单还是空的，先add一条")
    if not 1<=index<=len(tasks):
        raise ValueError(f"序号必须在{1}到{len(tasks)}之间，你给的是{index}")

def finish_task(tasks:list[dict],index:int)->dict:
    """把第index个任务标记已完成并返回"""
    check_index(tasks,index)
    task= tasks[index-1]
    task["done"]=True
    return task

def undone_task(tasks:list[dict],index:int)->dict:
    """改变第index个任务的完成状态并返回"""
    check_index(tasks,index)
    task=tasks[index-1]
    task["done"]=False
    return task


def remove_task(tasks:list[dict],index:int)->dict:
    """删除第index条，并返回"""
    check_index(tasks,index)
    return tasks.pop(index-1)

def search_task(tasks:list[dict],keyword:str)->list[tuple[int,dict]]:
    """按照关键词搜索标题，返回[(序号，任务)]"""
    keyword=keyword.strip()
    if not keyword:
        raise ValueError("search后面要跟关键词")
    return [(i,t) for i,t in enumerate(tasks,start=1) if keyword in t["title"]]

def unfinished_count(tasks:list[dict])->int:
    """还有几条没有完成"""
    return sum(1 for t in tasks if not t["done"])

def format_task(index :int,task:dict)->list[str]:
    """把一条待办格式化为一行文本，比如:1、【x】买菜"""
    mark="√" if task["done"] else " "
    return f"{index:>2}.[{mark}]{task['title']}"

def unfinished_titles(tasks:list[dict])->list[str]:
    return [task["title"] for task in tasks if not task["done"]]

def build_lines(tasks:list[dict])->list[str]:
    """把整个清单变成一组行文本（只返回字符串，不打印）"""
    if not tasks:
        return ["(还没有待办，用add加一条)"]
    lines=[format_task(i,t) for i,t in enumerate(tasks,start=1)]
    lines.append("")
    lines.append(f"一共{len(tasks)}条，未完成{unfinished_count(tasks)}条")
    return lines


