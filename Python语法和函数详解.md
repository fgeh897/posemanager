# Python 语法详解 & 函数分析

> **目标读者**：Python 初学者  
> **文档目的**：理解代码中每个函数、每个知识点的含义

---

## 第一部分：基础知识点速查

### 1️⃣ Python 导入（import）

```python
import os                           # 导入系统操作模块
import json                         # 导入 JSON 数据处理模块
import services                     # 导入游戏 API
```

**什么是导入？**
- 导入就是"加载别人写好的代码"
- `import X` 表示加载名叫 X 的代码库
- 导入后可以使用那个库提供的函数

**例子：**
```python
import json
data = json.load(f)  # 使用 json 库中的 load 函数读取 JSON
```

---

### 2️⃣ 全局变量（global）

```python
FAVORITE_POSES = []              # 全局变量：在函数外定义

def add_to_favorites():
    global FAVORITE_POSES        # 声明这是全局变量
    FAVORITE_POSES.append(x)     # 修改全局变量
```

**为什么需要 `global`？**
- Python 默认：函数内的变量是**局部的**（只在函数内有效）
- 使用 `global` 可以让函数修改**全局变量**（外面的变量）

**对比：**
```python
x = 10                           # 全局变量

def bad_modify():
    x = 20                       # 这创建了一个新的局部变量 x
    print(x)                     # 打印 20
print(x)                         # 打印 10（全局 x 没变）

def good_modify():
    global x
    x = 20                       # 修改全局变量
    print(x)                     # 打印 20
print(x)                         # 打印 20（全局 x 改了）
```

---

### 3️⃣ 字典（dict）

```python
person = {
    "name": "Alice",             # 键: 值
    "age": 25,
    "city": "Beijing"
}

print(person["name"])            # 输出：Alice
person["age"] = 26               # 修改值
person["job"] = "Engineer"       # 添加新的键值对
```

**字典的本质：**
- 键值对的集合（像一本词典，可以按单词查释义）
- 通过键（key）快速查找值（value）

---

### 4️⃣ 列表（list）

```python
fruits = ["apple", "banana", "cherry"]

fruits.append("orange")          # 添加元素
fruits.remove("banana")          # 删除元素
print(fruits[0])                 # 输出：apple（索引从 0 开始）
print(len(fruits))               # 输出列表长度

for fruit in fruits:
    print(fruit)                 # 依次打印每个元素
```

**列表的特点：**
- 有序集合（顺序很重要）
- 可以重复元素
- 可以修改、添加、删除

---

### 5️⃣ 字符串操作

```python
text = "hello world"

# 字符串拆分
parts = text.split(" ")          # ["hello", "world"]

# 字符串包含判断
if "hello" in text:
    print("包含 hello")

# 字符串替换
new_text = text.replace("world", "Python")  # "hello Python"

# 字符串格式化
name = "Alice"
greeting = f"Hello, {name}!"     # "Hello, Alice!"
```

---

### 6️⃣ 条件判断

```python
age = 18

# if-elif-else
if age < 13:
    print("小孩")
elif age < 18:
    print("少年")
elif age < 60:
    print("成年")
else:
    print("老年")

# 三元表达式（一行条件）
status = "成年人" if age >= 18 else "未成年"

# 布尔操作
if x > 0 and x < 100:            # 同时满足两个条件
    print("x 在 0-100 之间")

if x == 0 or x == 100:           # 满足任一条件
    print("x 是 0 或 100")

if not flag:                     # 取反
    print("flag 是 False")
```

---

### 7️⃣ 循环

```python
# for 循环：遍历列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# for 循环：遍历指定次数
for i in range(5):               # i 从 0 到 4
    print(i)

# while 循环：条件循环
count = 0
while count < 5:
    print(count)
    count += 1                   # 等同于 count = count + 1
```

---

### 8️⃣ 函数定义和调用

```python
# 定义函数
def greet(name):                 # name 是参数
    return f"Hello, {name}!"     # return 返回结果

# 调用函数
result = greet("Alice")          # 传入参数 "Alice"
print(result)                    # 输出：Hello, Alice!

# 有多个参数
def add(a, b):
    return a + b

print(add(3, 5))                 # 输出：8

# 默认参数
def greet_with_title(name, title="Mr"):
    return f"Hello, {title} {name}"

print(greet_with_title("Alice"))              # "Hello, Mr Alice"
print(greet_with_title("Alice", "Ms"))       # "Hello, Ms Alice"
```

---

### 9️⃣ 异常处理

```python
try:
    # 可能出错的代码
    result = 10 / 0              # 除以 0 会出错
    print(result)
except:
    # 出错时执行这里
    print("发生了错误")

# 更细致的异常处理
try:
    value = int("abc")           # 字符串转整数会出错
except ValueError:
    print("输入不是数字")
except ZeroDivisionError:
    print("除以 0 了")
except Exception as e:
    print(f"其他错误：{e}")

# 最后总会执行的代码
try:
    f = open("file.txt")
    data = f.read()
except:
    print("文件打开失败")
finally:
    print("无论成功失败都执行")
```

---

### 🔟 文件操作

```python
# 读取文件
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()           # 读取全部内容
    print(content)

# with 的作用：自动关闭文件

# 读取 JSON 文件
with open("data.json", "r") as f:
    data = json.load(f)          # 解析 JSON 转成 Python 对象

# 写入文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello World")

# 写入 JSON 文件
data = {"name": "Alice", "age": 25}
with open("data.json", "w") as f:
    json.dump(data, f)           # 将 Python 对象转成 JSON 写入
```

---

## 第二部分：核心函数详解

### 🎯 函数 1：`get_stbl_text(stbl_id, *args)` 

**位置：** 第 72-80 行

```python
def get_stbl_text(stbl_id, *args):
    try:
        if args:                                    # 如果有额外参数
            processed_args = []
            for arg in args:
                if isinstance(arg, str):           # 如果是字符串
                    processed_args.append(
                        sims4.localization.LocalizationHelperTuning.get_raw_text(arg)
                    )
                else:
                    processed_args.append(arg)
            return sims4.localization._create_localized_string(stbl_id, *processed_args)
        return sims4.localization._create_localized_string(stbl_id)
    except:
        return sims4.localization.LocalizationHelperTuning.get_raw_text(f"ID:{hex(stbl_id)}")
```

**用途：** 获取游戏本地化文本（多语言支持）

**知识点解析：**

| 知识点 | 解释 |
|--------|------|
| `*args` | 可变参数，接收任意数量的参数 |
| `isinstance(arg, str)` | 检查 arg 是否是字符串类型 |
| `for arg in args` | 遍历所有额外参数 |
| `append()` | 添加元素到列表 |
| `try-except` | 异常捕获，防止崩溃 |
| `hex(stbl_id)` | 将数字转成十六进制字符串 |

**举例说明：**
```python
# 简单调用：只需要文本 ID
text1 = get_stbl_text(0x278CC3FC)           # 返回对应的文本

# 复杂调用：文本 ID + 参数（比如填充变量名）
text2 = get_stbl_text(STR_DYN_CREATOR_FAVED, "Creator_Name", 10)
# 可能返回："Creator_Name 已收藏 (10 个动作)"
```

---

### 🎯 函数 2：`get_mod_directory()`

**位置：** 第 137-142 行

```python
def get_mod_directory():
    try:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except:
        return ''
```

**用途：** 获取 MOD 的安装目录路径

**知识点解析：**

| 知识点 | 解释 |
|--------|------|
| `__file__` | 当前文件的路径 |
| `os.path.abspath()` | 转换成绝对路径 |
| `os.path.dirname()` | 获取目录的上一级目录 |

**逐步分解：**
```
原始路径：C:\Games\Sims4\Mods\posemanager\script\posemanager2.py

第一次 dirname：C:\Games\Sims4\Mods\posemanager\script
第二次 dirname：C:\Games\Sims4\Mods\posemanager
结果就是 MOD 的根目录！
```

---

### 🎯 函数 3：`load_favorites()`

**位置：** 第 154-174 行

```python
def load_favorites():
    global FAVORITE_POSES, FAVORITE_CREATORS, FAVORITE_PACKS
    
    # 加载收藏的动作
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, 'r', encoding='utf-8') as f:
                FAVORITE_POSES = list(dict.fromkeys(json.load(f)))
        except:
            pass
    
    # 加载收藏的作者
    if os.path.exists(FAV_CREATORS_FILE):
        try:
            with open(FAV_CREATORS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                FAVORITE_CREATORS = list(dict.fromkeys(data))
        except:
            pass
    
    # 加载收藏的包
    if os.path.exists(FAV_PACKS_FILE):
        try:
            with open(FAV_PACKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                FAVORITE_PACKS = list(dict.fromkeys(data))
        except:
            pass
```

**用途：** 从硬盘读取用户的收藏数据

**知识点解析：**

```python
os.path.exists(FAV_FILE)              # 检查文件是否存在

with open(FAV_FILE, 'r', encoding='utf-8') as f:
    # 'r' = 读取模式
    # encoding='utf-8' = 使用 UTF-8 编码（支持中文）
    # with 自动关闭文件

json.load(f)                          # 从文件读取并解析 JSON

dict.fromkeys(list)                   # 去除列表中的重复元素
# 原理：dict 的键不能重复，所以转成 dict 再转回 list 就自动去重了

list(dict_object)                     # 将 dict 转回列表
```

**执行流程：**
```
检查文件是否存在
  ├─ 存在：打开并读取
  │  ├─ 成功：加载数据 + 去重
  │  └─ 失败：捕获异常，什么都不做
  └─ 不存在：什么都不做
```

---

### 🎯 函数 4：`save_favorites()`

**位置：** 第 177-186 行

```python
def save_favorites():
    try:
        with open(FAV_FILE, 'w', encoding='utf-8') as f:
            json.dump(FAVORITE_POSES, f, ensure_ascii=False)
        with open(FAV_CREATORS_FILE, 'w', encoding='utf-8') as f:
            json.dump(FAVORITE_CREATORS, f, ensure_ascii=False)
        with open(FAV_PACKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(FAVORITE_PACKS, f, ensure_ascii=False)
    except:
        pass
```

**用途：** 将收藏数据保存到硬盘

**知识点解析：**

```python
'w' 模式                              # 写入模式（覆盖原有内容）
json.dump(data, f, ensure_ascii=False)
# 将 Python 对象转成 JSON 并写入文件
# ensure_ascii=False: 允许中文等非 ASCII 字符
```

---

### 🎯 函数 5：`get_pack_type(pack)`

**位置：** 第 189-200 行

```python
def get_pack_type(pack):
    if not pack: 
        return 'NORMAL'
    
    # 构建搜索字符串
    combined_str = str(pack).lower() if isinstance(pack, str) else \
                   str(getattr(pack, '__name__', '')).lower()
    
    if not isinstance(pack, str) and hasattr(pack, 'pose_list'):
        combined_str += " " + " ".join(
            [str(getattr(p, 'pose_name', '')).lower() for p in getattr(pack, 'pose_list', [])]
        )

    if 'hegfcreator' in combined_str: 
        return 'CREATORS'
    if 'fgeh_poses' in combined_str: 
        return 'POSES'
    if 'fgeh_fav_packs' in combined_str: 
        return 'FAV_PACKS'
    return 'NORMAL'
```

**用途：** 识别动作包的类型

**知识点解析：**

```python
if not pack:                          # 如果 pack 为空/None，返回 'NORMAL'

isinstance(pack, str)                 # 检查 pack 是否是字符串
getattr(pack, '__name__', '')        # 获取 pack 对象的 __name__ 属性
                                     # 如果没有，默认返回 ''

str(pack).lower()                     # 转成字符串并转小写

hasattr(pack, 'pose_list')           # 检查 pack 是否有 pose_list 属性

[... for p in ...]                   # 列表推导式（下面详解）

'hegfcreator' in combined_str        # 字符串包含判断
```

**列表推导式详解：**
```python
# 普通写法
result = []
for p in pack.pose_list:
    result.append(str(getattr(p, 'pose_name', '')).lower())

# 简洁写法（列表推导式）
result = [str(getattr(p, 'pose_name', '')).lower() for p in pack.pose_list]
```

**执行示例：**
```python
pack = <一个动作包对象>
# 如果包的名字中包含 "hegfcreator"，识别为作者包
# 如果包的名字中包含 "fgeh_poses"，识别为动作包
# 如果包的名字中包含 "fgeh_fav_packs"，识别为收藏包
# 否则识别为普通包
```

---

### 🎯 函数 6：`build_cache_safe()`

**位置：** 第 203-237 行

```python
def build_cache_safe():
    global CACHE_BUILT, GLOBAL_ALL_POSES_CACHE, GLOBAL_ALL_CREATORS_CACHE, GLOBAL_ALL_PACKS_CACHE
    
    if CACHE_BUILT: 
        return                       # 如果已经构建过，直接返回
    
    try:
        manager = services.get_instance_manager(sims4.resources.Types.SNIPPET)
        if manager is None: 
            return
        
        # 初始化临时缓存
        temp_pose_cache, temp_creator_cache, temp_pack_cache = {}, {}, {}
        
        # 遍历所有的游戏对象
        for _, pack in manager._tuned_classes.items():
            # 检查是否是动作包
            if hasattr(pack, 's4s_mod_type') and \
               str(pack.s4s_mod_type).upper() == 'POSE_PACK':
                
                pack_id = str(getattr(pack, '__name__', 'Unknown'))
                temp_pack_cache[pack_id] = pack
                
                # 从第一个动作中提取作者名
                creator = ""
                for pose in getattr(pack, 'pose_list', []):
                    pose_name = getattr(pose, 'pose_name', None)
                    if pose_name and ':' in str(pose_name).strip():
                        creator = str(pose_name).strip().split(':')[0].strip()
                        break
                
                # 如果没有找到作者，从包属性中获取
                if not creator or creator.lower() == 'unknown':
                    creator_obj = getattr(pack, 'creator_name', None)
                    creator = str(creator_obj).strip() if creator_obj else 'Unknown'

                # 将包添加到作者的包列表
                if creator not in temp_creator_cache: 
                    temp_creator_cache[creator] = []
                temp_creator_cache[creator].append(pack)

                # 缓存每个动作
                for pose in getattr(pack, 'pose_list', []):
                    p_name = getattr(pose, 'pose_name', None)
                    if p_name: 
                        temp_pose_cache[p_name] = {
                            'pose': pose, 
                            'pack_name': creator, 
                            'pack_ref': pack
                        }

        # 更新全局缓存
        GLOBAL_ALL_POSES_CACHE, GLOBAL_ALL_CREATORS_CACHE, GLOBAL_ALL_PACKS_CACHE = \
            temp_pose_cache, temp_creator_cache, temp_pack_cache
        CACHE_BUILT = True
    except:
        CACHE_BUILT = True
```

**用途：** 建立"缓存"——快速查找所有动作包的信息

**知识点解析：**

| 知识点 | 解释 |
|--------|------|
| `manager._tuned_classes.items()` | 获取所有游戏对象和它们的信息 |
| `.items()` | 字典方法，返回键值对 |
| `for _, pack in ...` | `_` 表示不需要第一个返回值 |
| `hasattr(pack, 's4s_mod_type')` | 检查包是否有此属性 |
| `.strip()` | 移除字符串两端的空格 |
| `.split(':')` | 按 ':' 分割字符串 |

**缓存数据结构：**

```python
# 动作缓存
GLOBAL_ALL_POSES_CACHE = {
    "pose_001": {
        "pose": <动作对象>,
        "pack_name": "Creator_A",
        "pack_ref": <包对象>
    },
    "pose_002": { ... }
}

# 作者缓存
GLOBAL_ALL_CREATORS_CACHE = {
    "Creator_A": [<包对象1>, <包对象2>],
    "Creator_B": [<包对象3>]
}

# 包缓存
GLOBAL_ALL_PACKS_CACHE = {
    "pack_id_1": <包对象>,
    "pack_id_2": <包对象>
}
```

**执行流程图：**
```
扫描所有游戏对象
    ↓
对于每个动作包 pack：
    ├─ 将 pack 存入 GLOBAL_ALL_PACKS_CACHE
    ├─ 从动作名提取作者（格式：作者:动作名）
    ├─ 将 pack 添加到该作者的列表
    └─ 对于每个动作 pose：
       └─ 将 pose 的信息存入 GLOBAL_ALL_POSES_CACHE
```

---

### 🎯 函数 7：`custom_pack_rows_gen_safe(original, *args, **kwargs)`

**位置：** 第 242-265 行

```python
@injector2.inject(target_cls, 'picker_rows_gen')
def custom_pack_rows_gen_safe(original, *args, **kwargs):
    try:
        # ... 清空原有的包列表
        if hasattr(target_cls, 'POSE_PACKS'): 
            target_cls.POSE_PACKS = None
        
        try:
            gen = original(*args, **kwargs)
        except TypeError:
            gen = original(*args[1:], **kwargs)

        # 添加 3 个自定义菜单项
        yield ObjectPickerRow(name=get_stbl_text(STR_L1_FAV_PACKS_TITLE),
                              row_description=get_stbl_text(STR_L1_FAV_PACKS_DESC), 
                              icon=MY_CUSTOM_ICON,
                              tag="fgeh_fav_packs_folder")
        yield ObjectPickerRow(name=get_stbl_text(STR_L1_CREATORS_TITLE),
                              row_description=get_stbl_text(STR_L1_CREATORS_DESC), 
                              icon=MY_CUSTOM_ICON,
                              tag="hegfcreator_folder")
        yield ObjectPickerRow(name=get_stbl_text(STR_L1_POSES_TITLE),
                              row_description=get_stbl_text(STR_L1_POSES_DESC), 
                              icon=MY_CUSTOM_ICON,
                              tag="fgeh_poses_folder")

        # 添加原有的菜单项（除了我们自定义的）
        seen_tags = {"fgeh_fav_packs_folder", "hegfcreator_folder", "fgeh_poses_folder"}
        for row in gen:
            if row.tag in seen_tags: 
                continue                    # 跳过已添加的
            pack = row.tag
            if get_pack_type(pack) == 'NORMAL':
                sn, dn = str(getattr(pack, 'sort_name', "")).strip().lower(), \
                         str(getattr(pack, 'display_name', "")).strip().lower()
                # 过滤掉无效的包
                if not sn or sn in ('', 'unknown', '0x00000000', 'none', 'nan', '0x0', '0') or \
                   dn in ('0x00000000', '0x0'):
                    continue
            yield row
    except:
        try:
            yield from original(*args, **kwargs)
        except TypeError:
            yield from original(*args[1:], **kwargs)
```

**用途：** 生成第一层菜单（主菜单），添加自定义选项

**关键知识点：**

```python
@injector2.inject(...)                   # 装饰器：修改原有函数的行为

def custom_pack_rows_gen_safe(original, ...):
    original(*args, **kwargs)            # 调用原有函数获取原菜单

yield ObjectPickerRow(...)               # 生成器语法：返回一个菜单项

seen_tags = {...}                        # 集合（set）：存放已添加的标签
if row.tag in seen_tags:                 # 检查是否在集合中
    continue                             # 跳过此次循环

yield from original(...)                 # 从原函数的生成器中取出所有项
```

**装饰器详解：**
```python
# 装饰器的作用：包装原有函数

原本：
poseplayer.PoseByPackInteraction.picker_rows_gen()
    ↓ 返回原菜单

修改后：
@injector2.inject(poseplayer.PoseByPackInteraction, 'picker_rows_gen')
def custom_pack_rows_gen_safe(original, ...):
    # 生成自定义菜单 + 原菜单
    ...
```

**生成器语法详解：**
```python
# 普通函数：一次性返回全部
def get_items():
    return [item1, item2, item3]

result = get_items()  # 一次性获得所有项

# 生成器函数：逐个返回
def get_items():
    yield item1
    yield item2
    yield item3

for item in get_items():       # 循环调用时逐个获得
    print(item)
```

---

### 🎯 函数 8：`custom_pose_rows_gen(inst, target, context, **kwargs)`

**位置：** 第 268-438 行（这是最复杂的函数！）

这个函数根据当前选中的包类型生成不同的菜单。让我们按类型分解：

#### 8.1：处理"动作包收藏夹"（FAV_PACKS 类型）

```python
if pack_type == 'FAV_PACKS':
    if not CACHE_BUILT: 
        build_cache_safe()     # 确保缓存已构建

    if FAV_PACKS_VIEW_MODE == P_MODE_FAVS:
        # 显示 3 个按钮
        yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_MANAGE),
                              tag="BTN_FAV_PACKS_MANAGE")
        yield ObjectPickerRow(name=get_stbl_text(STR_BTN_DELETE_MODE),
                              tag="BTN_FAV_PACKS_DELETE_MODE")
        yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_CLEAR),
                              tag="BTN_FAV_PACKS_CLEAR")

        # 显示收藏的包列表
        fav_packs_sorted = []
        for pck_id in FAVORITE_PACKS:                    # 遍历收藏 ID
            pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)    # 查询包对象
            if pck: 
                fav_packs_sorted.append(
                    (getattr(pck, 'display_name', None) or ..., pck_id, pck)
                )
        fav_packs_sorted.sort(key=lambda x: str(x[0]).lower())  # 排序

        for pck_name, pck_id, pck in fav_packs_sorted:
            yield ObjectPickerRow(name=pck_name,
                                  count=len(getattr(pck, 'pose_list', [])),
                                  tag=f"P_SELECT::{pck_id}")
```

**知识点：**

```python
GLOBAL_ALL_PACKS_CACHE.get(pck_id)     # 字典 get 方法：安全获取值
                                       # 如果 key 不存在返回 None

getattr(pck, 'display_name', None) or ...
                                       # 链式操作：如果第一个是 None，用第二个

fav_packs_sorted.sort(key=lambda x: ...)
                                       # 按自定义规则排序
                                       # lambda 是匿名函数

f"P_SELECT::{pck_id}"                 # f-string 格式化字符串（嵌入变量）
```

#### 8.2：处理"作者收藏夹"（CREATORS 类型）

```python
if pack_type == 'CREATORS':
    if CREATOR_VIEW_MODE == C_MODE_FAVS:
        # 显示按钮
        yield ObjectPickerRow(name=get_stbl_text(STR_C_BTN_ADD), 
                              tag="BTN_ALL_CREATORS")
        
        # 显示收藏的作者
        for creator in sorted(FAVORITE_CREATORS):  # 排序后遍历
            if creator in GLOBAL_ALL_CREATORS_CACHE:
                count = len(GLOBAL_ALL_CREATORS_CACHE[creator])
                yield ObjectPickerRow(
                    name=get_stbl_text(STR_DYN_CREATOR_FAVED, creator, count),
                    tag=f"C_VIEW::{creator}"
                )
```

#### 8.3：处理"动作包内"（NORMAL 类型）

```python
if pack_type == 'NORMAL':
    # 显示返回按钮
    yield ObjectPickerRow(name=get_stbl_text(STR_DYN_TOGGLE_MODE_2, current_mode_str),
                          icon=MY_CUSTOM_ICON,
                          tag="TOGGLE_MODE_BTN")
    
    # 显示"收藏此包"和"收藏此包内所有动作"按钮
    pack_id = str(getattr(pack, '__name__', 'Unknown'))
    is_pack_faved = pack_id in FAVORITE_PACKS
    
    yield ObjectPickerRow(
        name=get_stbl_text(pack_btn_id),  # "添加" 或 "移除"
        tag="TOGGLE_FAV_PACK_ONLY_BTN"
    )
    
    # 显示包内的每个动作
    for pose_item in getattr(pack, 'pose_list', []):
        yield ObjectPickerRow(name=pose_item.pose_display_name, 
                              icon=pose_item.icon, 
                              tag=pose_item)
```

---

### 🎯 函数 9：`custom_pose_on_choice(self, choice_tag, **kwargs)`

**位置：** 第 441-603 行（处理菜单点击）

这个函数是整个系统的"大脑"——每当玩家点击一个菜单项，就会调用此函数。

#### 9.1：处理动作点击

```python
if choice_tag is None or not isinstance(choice_tag, str):
    if hasattr(choice_tag, 'pose_name'):
        p_name = choice_tag.pose_name
        
        # 模式 1：收藏模式 - 点击动作时切换收藏状态
        if CURRENT_MODE == MODE_FAV:
            if p_name in FAVORITE_POSES:
                FAVORITE_POSES.remove(p_name)      # 取消收藏
            else:
                FAVORITE_POSES.append(p_name)      # 收藏
            save_favorites()                       # 保存到文件
            return self._show_picker_dialog(...)   # 刷新菜单
        
        # 模式 2：追踪模式 - 点击动作时跳转到该动作所在的包
        if CURRENT_MODE == MODE_TRACE:
            build_cache_safe()
            info = GLOBAL_ALL_POSES_CACHE.get(p_name)  # 查找动作信息
            if info:
                self.selected_pose_pack = info['pack_ref']  # 跳转到包
                GLOBAL_TRACED_PACK_REF = info['pack_ref']
                RETURN_TO_FAV_ON_CLOSE = True      # 记住返回位置
                CURRENT_MODE = MODE_NORMAL         # 切换回普通模式
                return self._show_picker_dialog(...)
```

**关键概念：**

```python
choice_tag is None                          # 检查是否为 None
isinstance(choice_tag, str)                 # 检查是否为字符串
hasattr(choice_tag, 'pose_name')           # 检查是否有 pose_name 属性

# 如果 choice_tag 是动作对象，则有 pose_name 属性
# 如果 choice_tag 是字符串标签，则没有 pose_name 属性
```

#### 9.2：处理字符串标签（菜单按钮点击）

```python
# 删除收藏包
if choice_tag == "BTN_FAV_PACKS_DELETE_MODE": 
    FAV_PACKS_VIEW_MODE = P_MODE_DELETE      # 切换到删除模式
    return self._show_picker_dialog(...)     # 刷新菜单

# 删除特定的收藏包
if choice_tag.startswith("P_DELETE::"):
    pck_id = choice_tag.split("::")[1]       # 提取包 ID
    if pck_id in FAVORITE_PACKS:
        FAVORITE_PACKS.remove(pck_id)        # 从收藏中移除
        save_favorites()                     # 保存
    return self._show_picker_dialog(...)

# 切换收藏状态
if choice_tag.startswith("P_TOGGLE::"):
    pck_id = choice_tag.split("::")[1]
    if pck_id in FAVORITE_PACKS:
        FAVORITE_PACKS.remove(pck_id)
    else:
        FAVORITE_PACKS.append(pck_id)
    save_favorites()
    return self._show_picker_dialog(...)

# 返回菜单
if choice_tag == "RETURN_TO_FAV_PACKS_MENU_BTN":
    self.selected_pose_pack = "fgeh_fav_packs_folder"  # 选中收藏包文件夹
    FAV_PACKS_VIEW_MODE = P_MODE_FAVS                  # 返回浏览模式
    return self._show_picker_dialog(...)
```

**字符串操作详解：**

```python
choice_tag = "P_DELETE::pack_123"

choice_tag.startswith("P_DELETE::")        # 检查前缀：True
choice_tag.split("::")                     # 按 "::" 分割：["P_DELETE", "pack_123"]
choice_tag.split("::")[1]                  # 获取第二部分："pack_123"
```

#### 9.3：处理模式切换

```python
if choice_tag == "TOGGLE_MODE_BTN":
    if pack_type == 'POSES':
        # 在收藏菜单中：普通 → 收藏 → 追踪 → 普通
        CURRENT_MODE = (CURRENT_MODE + 1) % 3
    else:
        # 在普通包中：普通 ↔ 收藏
        CURRENT_MODE = MODE_FAV if CURRENT_MODE == MODE_NORMAL else MODE_NORMAL
    return self._show_picker_dialog(...)
```

**模运算详解：**
```python
CURRENT_MODE = (CURRENT_MODE + 1) % 3

当 CURRENT_MODE = 0 时：(0 + 1) % 3 = 1
当 CURRENT_MODE = 1 时：(1 + 1) % 3 = 2
当 CURRENT_MODE = 2 时：(2 + 1) % 3 = 0    # 回到 0
```

---

## 第三部分：完整工作流示例

### 场景：玩家想要收藏一个动作

```
玩家点击"选择动作"按钮
    ↓
游戏调用 PoseByPackInteraction.picker_rows_gen()
    ↓
我们的 custom_pack_rows_gen_safe() 被调用
    ↓
生成菜单：
  [我的收藏包]
  [作者]
  [全部动作]
  [普通包 1]
  [普通包 2]
  ...
    ↓
玩家选择 [普通包 1]
    ↓
自动调用 custom_pose_on_choice(self, <包对象>, **kwargs)
    ↓
触发：
  - self.selected_pose_pack = <包对象>
  - custom_pose_rows_gen() 生成该包内的动作列表
    ↓
显示菜单：
  [模式切换按钮]
  [收藏此包按钮]
  [收藏包内所有动作按钮]
  [动作 1]
  [动作 2]
  ...
    ↓
玩家选择 [切换模式] 按钮
    ↓
custom_pose_on_choice() 被调用
    ↓
CURRENT_MODE 从 0 (普通) 变为 1 (收藏)
    ↓
菜单刷新，按钮文字变为 "退出收藏模式"
    ↓
玩家选择 [动作 1]
    ↓
custom_pose_on_choice(self, <动作1对象>, **kwargs) 被调用
    ↓
因为 CURRENT_MODE == 1，执行收藏逻辑：
  if "动作1名" not in FAVORITE_POSES:
      FAVORITE_POSES.append("动作1名")
  save_favorites()  # 写入 JSON 文件
    ↓
菜单刷新，显示"已收藏"
```

---

## 第四部分：常见 Python 模式速查

### 模式 1：安全获取对象属性

```python
# 不安全：如果 obj 没有 attr，会报错
value = obj.attr

# 安全做法 1：使用 getattr（推荐）
value = getattr(obj, 'attr', None)     # 如果没有，返回 None
value = getattr(obj, 'attr', 'default') # 如果没有，返回 'default'

# 安全做法 2：检查后获取
if hasattr(obj, 'attr'):
    value = obj.attr
```

### 模式 2：处理 None 值的链式操作

```python
# 问题：如果 obj.attr 是 None，后续操作会报错
display_name = obj.display_name.lower()

# 解决方案：使用 or 操作符
display_name = (obj.display_name or "default").lower()

# 更复杂的例子
name = getattr(obj, 'display_name', None) or \
       getattr(obj, 'sort_name', None) or \
       getattr(obj, '__name__', 'Unknown')
```

### 模式 3：字符串分割和提取

```python
# 获取冒号前的部分（作者名）
text = "Author_Name : Pose_Name"
author = text.split(":")[0].strip()    # "Author_Name"

# 更安全的做法
parts = text.split(":")
if len(parts) > 0:
    author = parts[0].strip()

# 在列表中查找和替换
items = ["a", "b", "c"]
if "b" in items:
    items.remove("b")
```

### 模式 4：字典的快速查找

```python
cache = {
    "key1": "value1",
    "key2": "value2"
}

# 方式 1：直接访问（如果 key 不存在会报错）
value = cache["key1"]

# 方式 2：get 方法（推荐，安全）
value = cache.get("key1")           # 如果不存在返回 None
value = cache.get("key1", "default") # 如果不存在返回 "default"

# 检查 key 是否存在
if "key1" in cache:
    print(cache["key1"])
```

### 模式 5：列表的排序和去重

```python
# 排序
numbers = [3, 1, 4, 1, 5]
sorted_numbers = sorted(numbers)    # [1, 1, 3, 4, 5]

# 去重
unique_numbers = list(set(numbers)) # [1, 3, 4, 5]（顺序不保证）

# 去重且保持顺序
unique_numbers = list(dict.fromkeys(numbers))  # [3, 1, 4, 5]

# 自定义排序规则
objects = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
sorted_objects = sorted(objects, key=lambda x: x["age"])
# 按年龄升序排列
```

### 模式 6：异常捕获的最佳实践

```python
# 捕获所有异常（不推荐，会隐藏 bug）
try:
    risky_operation()
except:
    pass

# 捕获特定异常（推荐）
try:
    value = int("abc")
except ValueError as e:
    print(f"输入错误：{e}")
except FileNotFoundError:
    print("文件不存在")
except Exception as e:
    print(f"其他错误：{e}")

# try-except-finally
try:
    f = open("file.txt")
    data = f.read()
except:
    print("打开失败")
finally:
    f.close()  # 无论成功失败都执行
```

---

## 📚 总结速查表

| 概念 | 用途 | 例子 |
|-----|------|------|
| `global` | 在函数内修改全局变量 | `global FAVORITE_POSES` |
| `import` | 加载外部代码库 | `import json` |
| `dict` | 键值对存储 | `cache = {"key": "value"}` |
| `list` | 有序集合 | `items = [1, 2, 3]` |
| `for` 循环 | 遍历集合 | `for item in items:` |
| `if-elif-else` | 条件判断 | `if x > 0:` |
| `try-except` | 异常捕获 | `try: ... except: ...` |
| `getattr()` | 安全获取属性 | `getattr(obj, 'attr', None)` |
| `isinstance()` | 类型检查 | `isinstance(x, str)` |
| `split()` | 字符串分割 | `"a:b".split(":")` |
| `sort()` | 排序 | `items.sort(key=lambda x: ...)` |
| `yield` | 生成器 | `def gen(): yield item` |
| `lambda` | 匿名函数 | `lambda x: x * 2` |
| `f-string` | 字符串格式化 | `f"Hello {name}"` |

---

## 💬 你还有问题吗？

如果对某个函数或语法点还有疑惑，可以问我：
- "函数 X 是干什么的？"
- "这行代码什么意思？"
- "为什么要用 global？"

我会给你更详细的解释！
