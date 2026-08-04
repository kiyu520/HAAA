from data import model_data 
import os

model_list=[]

def _mask_key(key):
    """脱敏 API KEY：只显示前4位，如 sk-xxxx-...-1234"""
    if not key:
        return ""
    if len(key) <= 8:
        return key[:4] + "****"
    return key[:4] + "****" + key[-4:]

def init_list():
    if not os.path.exists(".models"):
        print("[WARN] .models 文件不存在，模型列表为空")
        return
    with open(".models","r",encoding="utf-8") as f:
        lines=[]
        for i in f:
            lines.append(i.strip())
        if len(lines) % 3 != 0:
            raise ValueError("ERROR:.models 文件行数必须是 3 的整数倍（每 3 行一个模型：URL/KEY/NAME）")
        i=0
        while i < len(lines):
            model=model_data(lines[i],lines[i+1],lines[i+2])
            add_model(model)
            i+=3
def show_list():
    if len(model_list) == 0:
        print("模型列表为空。可用 `add` 命令添加模型。")
        return
    for i in range(0,len(model_list)):
        url,key,model=model_list[i].get_ALL()
        print("================")
        print(f"index:{i}")
        print(f"model_name:{model}")
        print(f"url:{url}")
        print(f"key:{_mask_key(key)}")

def show_default():
    if not os.path.exists(".default_model"):
        print("[WARN] .default_model 文件不存在，尚未设置默认模型")
        return
    with open(".default_model","r",encoding="utf-8") as f:
        lines=[]
        for i in f:
            lines.append(i.strip())
        if len(lines) < 3:
            raise ValueError("ERROR:.default_model 文件内容不完整，需包含 3 行：URL/KEY/NAME")
        url,key,model=lines[0],lines[1],lines[2]
        print("================")
        print(f"model_name:{model}")
        print(f"url:{url}")
        print(f"key:{_mask_key(key)}")

def save_list():
    with open(".models","w",encoding="utf-8") as f:
        for item in model_list:
            url,key,model_name=item.get_ALL()
            f.write(f"{url}\n")
            f.write(f"{key}\n")
            f.write(f"{model_name}\n")
def get_default():
    if not os.path.exists(".default_model"):
        raise FileNotFoundError("ERROR:.default_model 文件不存在！请先通过 save_default(index) 设置默认模型")
    with open(".default_model","r",encoding="utf-8") as f:
        lines=[]
        for i in f:
            lines.append(i.strip())
        if len(lines) < 3:
            raise ValueError("ERROR:.default_model 文件内容不完整，需包含 3 行：URL/KEY/NAME")
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

def get_list():
    return model_list

def delete_model(index=None):
    assert index is not None and index < len(model_list) and index >=0,"ERROR:not an available num!"
    model_list.pop(index)
