from __future__ import annotations

import sys

from app.storage import DataError,load_tasks,save_tasks
from app.tasks import TodoList

USAGE = """用法：
    python -m app.main todo               显示所有待办任务
    python -m app.main clear             清空全部待办
    python -m app.main list              查看全部
    python -m app.main add "买菜"         新增一条
    python -m app.main done 2            把第 2 条标记为完成
    python -m app.main undone 1           把第1条标记为未完成
    python -m app.main remove 2          删除第 2 条
    python -m app.main search 买          按关键词搜索"""


def to_index(rest:list[str])->int:
    """把命令行给出的序号转成整数（不合法的话就报错）"""
    if not rest:
        raise ValueError("这个命令后面要跟序号，例如 done 2")
    try:
        return int(rest[0])
    except ValueError as exc:
        raise ValueError(f"序号必须是整数，你给的是{rest[0]!r}")from exc

def main(argv:list[str]|None=None)->int:
    """返回退出码 0 成功，2 用法或者数据有问题"""
    args=list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(USAGE)
        return 0
    command, rest = args[0],args[1:]
    try:
        todo=load_tasks()
        if command=="list":
            print("\n".join(todo.to_lines()))
            return 0
        
        if command=="add":
            if not rest:
                raise ValueError('add后面要跟内容,例如add "买菜"')
            task=todo.add(" ".join(rest))
            save_tasks(todo)
            print(f"已经添加：{task.title}(现在一共{len(todo)}条)")
            return 0
        
        if command == "done":
            task= todo.finish(to_index(rest))
            save_tasks(todo)
            print(f"已完成:{task.title}")
            return 0

        if command=="undone":
            task=todo.reopen(to_index(rest))
            save_tasks(todo)
            print(f"{task.title}已改为未完成")
            return 0
        
        if command=="remove":
            task= todo.remove(to_index(rest))
            save_tasks(todo)
            print(f"已删除：{task.title}")
            return 0
        
        if command=="search":
            if not rest:
                raise ValueError("search后面要跟关键词")
            found = todo.search(rest[0])
            if not found:
                print(f"没有找到包含{rest[0]!r}的待办")
                return 0
            for index,task in enumerate(found,start=1):
                print(f"{index:>2}.{task}")
            return 0

        if command=="todo":
            pending= todo.unfinished()
            if not pending:
                print("已经全部完成，没有待办！")
                return 0
            for i,task in enumerate(pending,start=1):
                print(f"{i:>2}.{task} :待办")            
            return 0
        
        if command=="clear":
            if not todo:
                print("没有待办的事情")
                return 0
            save_tasks(TodoList())
            print("已经清空全部待办")
            return 0
        print(f"不认识的命令：{command}\n")
        print(USAGE)
        return 2
    except(DataError,ValueError) as exc:
        print(f"错误，{exc}",file=sys.stderr)
        return 2

if __name__=="__main__":
    raise SystemExit(main())

            