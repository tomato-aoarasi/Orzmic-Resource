import json,os,sys
import UnityPy
import zipfile

DECRYPT_KEY = b"Big_True'sOrzmic"

file_apk = sys.argv[1]

UnityPy.set_assetbundle_decrypt_key(DECRYPT_KEY)

def createDirectory(directory : str):
    if not os.path.exists(directory):
        os.makedirs(directory)

def saveGamedatas(save_name : str = 'songs.json'):
    with zipfile.ZipFile(file_apk) as apk:
        with apk.open("assets/gamedatas") as f:
            env = UnityPy.load(f)
    for obj in env.objects:
        data = obj.read()
        if data.name == "MusicDatas":
            print(data.name)
            data = data.script
            break
    songs = json.loads(bytes(data))
    json_str = json.dumps(songs, ensure_ascii=False)
    with open(save_name, 'w', encoding='utf-8') as f:
        f.write(json_str)

def saveIll():
    envs = []
    with zipfile.ZipFile(file_apk) as apk:
        all_entries = apk.namelist()
        # 遍历所有项，找到在 'assets/charts' 目录下的项
        for entry in all_entries:
            if entry.startswith('assets/charts/'): # and not os.path.splitext(entry)[1]:
                with apk.open(entry) as f:
                    env = UnityPy.load(f)
                    count = 0
                    for obj in env.objects:
                        data = obj.read()
                        filename = data.name
                        sub_directory = f"{filename.split('_')[0]}"
                        
                        if filename.endswith("_img") and obj.type.name in ["Texture2D", "Sprite"]:
                            print(filename)
                            # parse the object data
                            r = data.read()

                            # create destination path
                            dir = f"covers/{sub_directory}/"
                            createDirectory(dir)
                            dest = os.path.join(dir, f"{obj.type.name}")
                            
                            count += 1

                            # make sure that the extension is correct
                            # you probably only want to do so with images/textures
                            dest, _ = os.path.splitext(dest)
                            dest = dest + ".png"

                            img = r.image
                            img.save(dest)
                        elif (obj.type.name not in ["Texture2D", "Sprite"]) and ("charts/" not in filename):
                            print(filename)
                            r = data.read()
                            chart_text = bytes(r.script).decode('utf-8')
                            
                            dir = f"charts/{sub_directory}/"
                            createDirectory(dir)
                            with open(f"{dir}/{filename.split('_')[1]}.txt", 'w', encoding='utf-8') as f:
                                f.write(chart_text)
              
def saveClips():
    dir = "clips"
    createDirectory(dir)
    with zipfile.ZipFile(file_apk) as apk:
        with apk.open("assets/clips") as f:
            env = UnityPy.load(f)
    for obj in env.objects:
        if obj.type.name in ["AudioClip"]:
            clip = obj.read()
            print(clip.name)
            #sub_directory = clip.name
            #print(sub_directory)
            #dir = f"clips/{sub_directory}"
            #createDirectory(dir)
            for name, data in clip.samples.items():
                with open(f"{dir}/{name}", "wb") as f:
                    f.write(data)
     
def saveCharacterheads():
    dir = "characters/"
    createDirectory(dir)
    # 头像获取
    with zipfile.ZipFile(file_apk) as apk:
        with apk.open("assets/characterheads") as f:
            env = UnityPy.load(f)
    for obj in env.objects:
        if obj.type.name not in ['Texture2D']:continue
        data = obj.read()
        filename = data.name
        print(f"{filename}_head")
        r = data.read()
        dest = os.path.join(dir, filename)
        dest, _ = os.path.splitext(dest)
        dest = dest + "_head.png"
        img = r.image
        img.save(dest)
    # 立绘获取
    match_str = 'assets/character_'
    with zipfile.ZipFile(file_apk) as apk:
        all_entries = apk.namelist()
        # 遍历所有项，找到在 'assets/charts' 目录下的项
        for entry in all_entries:
            if entry.startswith(match_str) and not entry.endswith(".manifest"): # and not os.path.splitext(entry)[1]:
                with apk.open(entry) as f:
                    env = UnityPy.load(f)
                    for obj in env.objects:
                        data = obj.read()
                        if obj.type.name in ["Texture2D"]:
                            filename = f"{entry.replace(match_str, '')}_{data.name}"
                            print(filename)
                            r = data.read()
                            dest = os.path.join(dir, filename)
                            dest, _ = os.path.splitext(dest)
                            dest = dest + ".png"
                            img = r.image
                            img.save(dest)
                        elif obj.type.name in ["TextAsset"]:
                            r = data.read()
                            character_text_json = json.loads(bytes(r.script).decode('utf-8'))
                            character_text = json.dumps(character_text_json, ensure_ascii=False)
                            filename = f"{entry.replace(match_str, '')}_{data.name}"
                            print(filename)
                            with open(f"{dir}{filename}.json", 'w', encoding='utf-8') as f:
                                f.write(character_text)
    
        
if __name__ == "__main__":
    while(True):
        print("""=======================
1. 获取游戏数据
2. 获取曲绘和铺面
3. 获取音频
4. 获取角色信息
其他键退出
-----------------------""")
        select_num = input("请输入编号: ")
        
        if select_num == "1":
            saveGamedatas()
            print("[*完成*]")
        elif select_num == "2":
            saveIll()
            print("[*完成*]")
        elif select_num == "3":
            print("读取中……")
            saveClips()
            print("[*完成*]")
        elif select_num == "4":
            saveCharacterheads()
            print("[*完成*]")
        else:
            break