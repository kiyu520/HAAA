import model_data from data
import os

modle_list=[]

def init_list():
    with open(".models","r",encoding="utf-8") as f:
        lines=[]
        for i in f:
            lines.append(i.strip())
        i=0
        while i < len(lines):
            model=model_data(lines[i],lines[i+1],lines[i+2])
            add_model(model)
            i+=3
def show_list():
    for i in range(0,len(model_list)):
        url,key,model=i.get_ALL()
        print("================")
        print(f"index:{i}")
        print(f"model_name:{model}")
        print(f"url:{url}")
        print(f"key:{key}")

def save_list():
    with open(".models","w",encoding="utf-8") as f:
        for i in model:
            url,key,model=i.get_ALL()
            f.write(f"{url}\n")
            f.write(f"{key}\n")
            f.write(f"{model}\n")
def get_default():
    with open(".default_model","r",encoding="utf-8") as f:
        lines=[]
        for i in f:
            lines.append(i.strip())
        return model_data(lines[0],lines[1],lines[2])

def save_default(index):
    assert index >=0 and index <len(model_list),"not an available number!"
    url,key,model=model_list[index].get_ALL()
    with open(".default_model","w",encoding="utf-8") as f:
        f.write(f"{url}\n")
        f.write(f"{key}\n")
        f.write(f"{model}\n")

def create_model_input():
    print("please input your data below :)")
    print("API_URL:")
    url=input()
    print("API_KEY:")
    key=input()
    print("model_name:")
    model=input()
    return model_data(url,key,model)

def add_model(model=None):
    assert model is not None,"ERROR:can't add None into model list"
    model_list.append(model)

def delete_model(index=None)
    assert index is not None and index < len(model_list) and index >=0,"ERROR:not an available num!"
    model_list.pop(index)

