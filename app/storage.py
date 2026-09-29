from __future__ import annotations
import json
from pathlib import Path
from app.tasks import Task,TodoList


DATA_FILE= Path(__file__).resolve().parents[1]/"data"/"tasks.json"

class DataError(Exception):'''这里是自定义异常错误，能够用except准确的接收到是什么错误，而不是整页'''

def load_tasks(path:Path|str=DATA_FILE)->TodoList:
    file_path=Path(path)
    if not file_path.exists():
        return TodoList()
    
    text = file_path.read_text(encoding="utf-8")
    try:                                                                                                              
        data = json.loads(text)                                                                                       
    except json.JSONDecodeError as exc:                                                                               
        raise DataError(f"{file_path.name} 不是合法的 JSON（第 {exc.lineno} 行）") from exc                           
                                                                                                                        
    if not isinstance(data, list):                                                                                    
        raise DataError(f"{file_path.name} 里应该是一个列表 [...]，实际是 {type(data).__name__}")                     
                                                                                                                        
    tasks=[Task.from_dict(item) for item in data]
    return TodoList(tasks)

def save_tasks(todo:TodoList,path:Path|str=DATA_FILE)->Path:
    """把待办列表写回json文件(覆盖写),返回实际写入的路径"""
    file_path=Path(path)
    file_path.parent.mkdir(parents=True,exist_ok= True)

    data=[task.to_dict() for task in todo.tasks]

    # ensure_ascii=False 让中文原样写进文件，而不是变成 \uXXXX
    text = json.dumps(data, ensure_ascii=False, indent=2)
    file_path.write_text(text + "\n", encoding="utf-8")
    return file_path
    