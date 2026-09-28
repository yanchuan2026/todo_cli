from __future__ import annotations

def show(tasks:list[str])->None:
    if not tasks:
        print("清单是空的")
        return
    for i,title in enumerate(tasks,start=1):
        print(f"{i}.{title}")

def main()->None:
    tasks=["背诵二十个单词","跑步三公里"]
    print("初始清单：")
    show(tasks)

    tasks.append("买菜")
    print("\n加了买菜之后:")
    show(tasks)

    remove=tasks.pop(0)
    print(f"删掉第一条({remove})之后")
    show(tasks)

    print(f"\n还剩{len(tasks)}条")
    
    



if __name__=="__main__":
    main()