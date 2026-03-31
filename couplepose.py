import os
import json
import services
import sims4.utils
from ui.ui_dialog_picker import ObjectPickerRow
import sims4.localization
import poseplayer
import sims4.resources
import injector2

# ==========================================
# 1. 文本哈希值配置区
# ==========================================
STR_L1_FAV_PACKS_TITLE = 0x278CC3FC
STR_L1_FAV_PACKS_DESC = 0x99F6F93C
STR_L1_CREATORS_TITLE = 0x655A38FA
STR_L1_CREATORS_DESC = 0xB1EA92D4
STR_L1_POSES_TITLE = 0x6C2DBAE1
STR_L1_POSES_DESC = 0x0BB118B4
STR_P_BTN_MANAGE = 0xC9E2B018
STR_P_BTN_MANAGE_DESC = 0x8AFA7155
STR_P_BTN_CLEAR = 0xB19F02B3
STR_P_BTN_CLEAR_DESC = 0x874D3807
STR_P_BTN_RETURN = 0x64C1549F
STR_C_BTN_ADD = 0x3E149230
STR_C_EMPTY = 0x6878BA66
STR_C_BTN_RETURN_LIST = 0x1338038D
STR_C_BTN_RETURN_FAVS = 0x9B1140F2
STR_S_BTN_CLEAR = 0x67831B33
STR_S_BTN_CLEAR_DESC = 0x6790F2BE
STR_S_EMPTY = 0x5354C743
STR_N_RETURN_TO_POSES = 0x1E0A5B44
STR_N_RETURN_TO_PACKS = 0x5ABDD568
STR_N_ADD_PACK = 0x55E0BBD6
STR_N_REMOVE_PACK = 0x55E0BBD6
STR_N_PACK_DESC = 0x5C400CD4
STR_N_ADD_ALL_POSES = 0x19D0EB22
STR_N_REMOVE_ALL_POSES = 0x19D0EB22
STR_N_ALL_POSES_DESC = 0x0BC210E6
STR_DYN_CREATOR_FAVED = 0x90A41E21
STR_DYN_CREATOR_STAR = 0x12E877A7
STR_DYN_CREATOR_NO_STAR = 0x3C932139
STR_DYN_RETURN_CREATOR = 0xB79CC45D
STR_DYN_TOGGLE_MODE_1 = 0xCCCD272F
STR_DYN_TOGGLE_MODE_1_DESC = 0x33CB4932
STR_DYN_TOGGLE_MODE_2 = 0xCCCD272F
STR_MODE_NAME_PLAY = 0xDAC8DF1D
STR_MODE_NAME_FAV = 0x9ED370DB
STR_MODE_NAME_TRACE = 0x1C252E56
STR_BTN_DELETE_MODE = 0x11DDB545
STR_P_BTN_DELETE_DESC = 0xBBDE2231
STR_C_BTN_DELETE_DESC = 0x83FDF125
STR_DYN_DELETE_ITEM = 0xB1161D76

# --- 分组器及视图专属哈希值 ---
STR_L1_GROUPED_TITLE = 0x735B69A4    
STR_L1_GROUPED_DESC = 0x7F4AE930     
STR_G_BTN_ADD_PACK = 0x49D735E3      
STR_G_BTN_REMOVE_PACK = 0x996A642F   
STR_G_PACK_DESC = 0xEF566C16         
STR_G_BTN_MANAGE_HOME = 0x307F315E   
STR_G_BTN_MANAGE_DESC = 0x6AC2B49D   
STR_G_BTN_AUTO_SORT = 0x425FD09E     
STR_G_BTN_AUTO_DESC = 0x492040A9     
STR_G_BTN_ADD_GROUP = 0x7E6BCA8D    
STR_G_DYN_PLAY_GRP = 0x06F2B644      
STR_G_DYN_EDIT_GRP = 0xEDCDFB41      
STR_G_DYN_DEL_GRP = 0xC94CA602       
STR_G_DYN_STAR_ITEM = 0x17E58B66     
STR_G_DYN_NO_STAR_ITEM = 0xBB0B554C  
STR_G_BTN_TOGGLE_ALL = 0x41A2B3C5    
STR_G_BTN_PATTERN_MATCH = 0x5B6C7D8E 
STR_G_PATTERN_DESC = 0x6C7D8E9F      
STR_G_BTN_RETURN_REMOVE = 0x676BB522
STR_G_BTN_RETURN_LIST = 0x4DD885AC
STR_G_BTN_RETURN_UP = 0x14082133
STR_G_BTN_PLAY_ALL = 0x9856EB2D
STR_G_DESC_PLAY_ALL = 0x89EBBB4F
STR_G_BTN_RETURN_SETTING = 0xC626CAB7
STR_G_BTN_RETURN_SELECT = 0xB04238CE
STR_G_BTN_TOGGLE_VIEW = 0x2190D304      
STR_G_VIEW_ALL = 0x21992F02             
STR_G_VIEW_CREATOR = 0x495EBA82         

# --- 【新增】虫洞哈希值 (请替换成你的生成器跑出来的 Hash！) ---
STR_G_BTN_WORMHOLE = 0x626289C7       # S4S: fgeh: [⚙️] 立即前往分组面板
STR_G_WORMHOLE_DESC = 0x62B43E2A      # S4S: fgeh: 直接跳转到该动作包的分组设置
STR_G_DYN_RENAME_GRP = 0x1A2B3C4D  # 请换成你实际生成的哈希！   # S4S: fgeh: [-] 重命名：{0}
STR_G_DYN_EDIT_RENAME_GRP = 0xA7E99AD1  # 请替换为：[⚙️] 编辑动作/重命名：{0.String} 的哈希
STR_G_BTN_RENAME_CURRENT = 0x9ADA6A84   # 请替换为：[✏️] 重命名当前组 的哈希
STR_G_RENAME_DIALOG_TITLE = 0xA3587516  # 请替换为：重命名动作分组 的哈希
STR_G_RENAME_DIALOG_TEXT = 0x68E68756   # 请替换为：请输入新的名称（例如：男左女右）： 的哈希

def get_stbl_text(stbl_id, *args):
    try:
        if args:
            processed_args = []
            for arg in args:
                if isinstance(arg, str):
                    processed_args.append(sims4.localization.LocalizationHelperTuning.get_raw_text(arg))
                else:
                    processed_args.append(arg)
            return sims4.localization._create_localized_string(stbl_id, *processed_args)
        return sims4.localization._create_localized_string(stbl_id)
    except:
        return sims4.localization.LocalizationHelperTuning.get_raw_text(f"ID:{hex(stbl_id)}")

MY_CUSTOM_ICON = sims4.resources.Key(0x00B2D882, 0x00B62A884676486C, 0x00000000)

# === 状态变量区 ===
MODE_NORMAL, MODE_FAV, MODE_TRACE = 0, 1, 2
CURRENT_MODE = MODE_NORMAL
CAME_FROM_L1_FAVS = False
CAME_FROM_CREATOR = False
GLOBAL_FAV_PACK_REF, GLOBAL_TRACED_PACK_REF, RETURN_TO_FAV_ON_CLOSE = None, None, False

P_MODE_FAVS, P_MODE_MANAGE, P_MODE_DELETE, P_MODE_CREATOR_PACKS = 0, 1, 2, 3
FAV_PACKS_VIEW_MODE = P_MODE_FAVS
CURRENT_SELECTED_FAV_CREATOR = None

C_MODE_FAVS, C_MODE_ALL, C_MODE_PACKS, C_MODE_DELETE = 0, 1, 2, 3
CREATOR_VIEW_MODE = C_MODE_FAVS
CURRENT_SELECTED_CREATOR = None

S_MODE_PLAY, S_MODE_DELETE = 0, 1
FAV_POSES_VIEW_MODE = S_MODE_PLAY

G_MODE_LIST, G_MODE_DELETE_PACK, G_MODE_PACK_HOME, G_MODE_PACK_MANAGE, G_MODE_EDIT_GROUP, G_MODE_PLAY_GROUP, G_MODE_CREATOR_PACKS = 0, 1, 2, 3, 4, 5, 6
G_VIEW_MODE = G_MODE_LIST
CURRENT_SELECTED_GROUP = None
CURRENT_SELECTED_GROUP_CREATOR = None
CAME_FROM_GROUPED = False

# === 数据层结构 ===
FAVORITE_POSES, FAVORITE_CREATORS, FAVORITE_PACKS = [], [], []
GROUPED_PACKS = {}

# 记忆视图开关
GROUPED_VIEW_BY_CREATOR = False  
FAV_PACKS_VIEW_BY_CREATOR = False 

GLOBAL_ALL_POSES_CACHE, GLOBAL_ALL_CREATORS_CACHE, GLOBAL_ALL_PACKS_CACHE = {}, {}, {}
CACHE_BUILT = False


# === 文件系统重构 ===
def get_mod_directory():
    try: return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except: return ''

FAV_FILE = os.path.join(get_mod_directory(), 'my_favorite_poses.json')
FAV_CREATORS_FILE = os.path.join(get_mod_directory(), 'my_favorite_creators.json')
FAV_PACKS_FILE = os.path.join(get_mod_directory(), 'my_favorite_packs.json')
USER_DATA_FILE = os.path.join(get_mod_directory(), 'fgeh_user_data.json')
USER_DATA_BAK = os.path.join(get_mod_directory(), 'fgeh_user_data.bak')

def load_favorites():
    global FAVORITE_POSES, FAVORITE_CREATORS, FAVORITE_PACKS, GROUPED_PACKS
    global GROUPED_VIEW_BY_CREATOR, FAV_PACKS_VIEW_BY_CREATOR
    
    def try_load_file(filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict): return data
            except: pass
        return None

    data = try_load_file(USER_DATA_FILE)
    if data is None: data = try_load_file(USER_DATA_BAK)
        
    if data:
        FAVORITE_POSES = list(dict.fromkeys(data.get("fav_poses", [])))
        FAVORITE_CREATORS = list(dict.fromkeys(data.get("fav_creators", [])))
        FAVORITE_PACKS = list(dict.fromkeys(data.get("fav_packs", [])))
        raw_grouped = data.get("grouped_packs", {})
        GROUPED_PACKS = raw_grouped if isinstance(raw_grouped, dict) else {}
        
        GROUPED_VIEW_BY_CREATOR = data.get("grouped_view_by_creator", False)
        FAV_PACKS_VIEW_BY_CREATOR = data.get("fav_packs_view_by_creator", False)
        return

    migrated = False
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, 'r', encoding='utf-8') as f: FAVORITE_POSES = list(dict.fromkeys(json.load(f)))
            migrated = True
        except: pass
    if os.path.exists(FAV_CREATORS_FILE):
        try:
            with open(FAV_CREATORS_FILE, 'r', encoding='utf-8') as f: FAVORITE_CREATORS = list(dict.fromkeys(json.load(f)))
            migrated = True
        except: pass
    if os.path.exists(FAV_PACKS_FILE):
        try:
            with open(FAV_PACKS_FILE, 'r', encoding='utf-8') as f: FAVORITE_PACKS = list(dict.fromkeys(json.load(f)))
            migrated = True
        except: pass
        
    if migrated:
        save_favorites()


def save_favorites():
    try:
        data = {
            "fav_poses": FAVORITE_POSES,
            "fav_creators": FAVORITE_CREATORS,
            "fav_packs": FAVORITE_PACKS,
            "grouped_packs": GROUPED_PACKS,
            "grouped_view_by_creator": GROUPED_VIEW_BY_CREATOR,
            "fav_packs_view_by_creator": FAV_PACKS_VIEW_BY_CREATOR
        }
        temp_file = USER_DATA_FILE + ".tmp"
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            
        if os.path.exists(USER_DATA_FILE):
            if os.path.exists(USER_DATA_BAK):
                os.remove(USER_DATA_BAK)
            os.rename(USER_DATA_FILE, USER_DATA_BAK)
            
        os.rename(temp_file, USER_DATA_FILE)
    except:
        pass


def auto_sort_couple_pack(pack):
    result = {"组 1": [], "组 2": []}
    try:
        pose_list = getattr(pack, 'pose_list', [])
        for idx, pose in enumerate(pose_list):
            p_name = getattr(pose, 'pose_name', None)
            if p_name:
                if idx % 2 == 0: result["组 1"].append(p_name)
                else: result["组 2"].append(p_name)
    except: pass
    return result


def get_pack_type(pack):
    if not pack: return 'NORMAL'
    combined_str = str(pack).lower() if isinstance(pack, str) else str(getattr(pack, '__name__', '')).lower()
    if not isinstance(pack, str) and hasattr(pack, 'pose_list'):
        combined_str += " " + " ".join([str(getattr(p, 'pose_name', '')).lower() for p in getattr(pack, 'pose_list', [])])

    if 'hegfcreator' in combined_str: return 'CREATORS'
    if 'fgeh_poses' in combined_str: return 'POSES'
    if 'fgeh_fav_packs' in combined_str: return 'FAV_PACKS'
    if 'fgeh_grouped' in combined_str: return 'GROUPED_PACKS'
    return 'NORMAL'


def build_cache_safe():
    global CACHE_BUILT, GLOBAL_ALL_POSES_CACHE, GLOBAL_ALL_CREATORS_CACHE, GLOBAL_ALL_PACKS_CACHE
    if CACHE_BUILT: return
    try:
        manager = services.get_instance_manager(sims4.resources.Types.SNIPPET)
        if manager is None: return
        temp_pose_cache, temp_creator_cache, temp_pack_cache = {}, {}, {}
        for _, pack in manager._tuned_classes.items():
            if hasattr(pack, 's4s_mod_type') and str(pack.s4s_mod_type).upper() == 'POSE_PACK':
                pack_id = str(getattr(pack, '__name__', 'Unknown'))
                temp_pack_cache[pack_id] = pack
                creator = ""
                for pose in getattr(pack, 'pose_list', []):
                    pose_name = getattr(pose, 'pose_name', None)
                    if pose_name and ':' in str(pose_name).strip():
                        creator = str(pose_name).strip().split(':')[0].strip()
                        break
                if not creator or creator.lower() == 'unknown':
                    creator_obj = getattr(pack, 'creator_name', None)
                    creator = str(creator_obj).strip() if creator_obj else 'Unknown'

                if creator not in temp_creator_cache: temp_creator_cache[creator] = []
                temp_creator_cache[creator].append(pack)

                for pose in getattr(pack, 'pose_list', []):
                    p_name = getattr(pose, 'pose_name', None)
                    if p_name: temp_pose_cache[p_name] = {'pose': pose, 'pack_name': creator, 'pack_ref': pack}

        GLOBAL_ALL_POSES_CACHE, GLOBAL_ALL_CREATORS_CACHE, GLOBAL_ALL_PACKS_CACHE = temp_pose_cache, temp_creator_cache, temp_pack_cache
        CACHE_BUILT = True
    except: CACHE_BUILT = True


# ==========================================
# 菜单渲染区
# ==========================================
target_cls = getattr(poseplayer, 'PoseByPackInteraction', None)

if target_cls is not None and not isinstance(target_cls, str):
    @injector2.inject(target_cls, 'picker_rows_gen')
    def custom_pack_rows_gen_safe(original, *args, **kwargs):
        global CAME_FROM_GROUPED, CAME_FROM_L1_FAVS, CAME_FROM_CREATOR, G_VIEW_MODE
        CAME_FROM_GROUPED, CAME_FROM_L1_FAVS, CAME_FROM_CREATOR = False, False, False
        G_VIEW_MODE = G_MODE_LIST 
        
        try:
            if hasattr(target_cls, 'POSE_PACKS'): target_cls.POSE_PACKS = None
            try: gen = original(*args, **kwargs)
            except TypeError: gen = original(*args[1:], **kwargs)

            yield ObjectPickerRow(name=get_stbl_text(STR_L1_GROUPED_TITLE), row_description=get_stbl_text(STR_L1_GROUPED_DESC), icon=MY_CUSTOM_ICON, tag="fgeh_grouped_folder")
            yield ObjectPickerRow(name=get_stbl_text(STR_L1_FAV_PACKS_TITLE), row_description=get_stbl_text(STR_L1_FAV_PACKS_DESC), icon=MY_CUSTOM_ICON, tag="fgeh_fav_packs_folder")
            yield ObjectPickerRow(name=get_stbl_text(STR_L1_CREATORS_TITLE), row_description=get_stbl_text(STR_L1_CREATORS_DESC), icon=MY_CUSTOM_ICON, tag="hegfcreator_folder")
            yield ObjectPickerRow(name=get_stbl_text(STR_L1_POSES_TITLE), row_description=get_stbl_text(STR_L1_POSES_DESC), icon=MY_CUSTOM_ICON, tag="fgeh_poses_folder")

            seen_tags = {"fgeh_fav_packs_folder", "hegfcreator_folder", "fgeh_poses_folder", "fgeh_grouped_folder"}
            for row in gen:
                if row.tag in seen_tags: continue
                pack = row.tag
                if get_pack_type(pack) == 'NORMAL':
                    sn, dn = str(getattr(pack, 'sort_name', "")).strip().lower(), str(getattr(pack, 'display_name', "")).strip().lower()
                    if not sn or sn in ('', 'unknown', '0x00000000', 'none', 'nan', '0x0', '0') or dn in ('0x00000000', '0x0'):
                        continue
                yield row
        except:
            try: yield from original(*args, **kwargs)
            except TypeError: yield from original(*args[1:], **kwargs)


def custom_pose_rows_gen(inst, target, context, **kwargs):
    global CURRENT_MODE, GLOBAL_FAV_PACK_REF, RETURN_TO_FAV_ON_CLOSE, GLOBAL_TRACED_PACK_REF
    global CREATOR_VIEW_MODE, CURRENT_SELECTED_CREATOR, CAME_FROM_L1_FAVS, CAME_FROM_CREATOR
    global FAV_PACKS_VIEW_MODE, FAV_POSES_VIEW_MODE, CURRENT_SELECTED_FAV_CREATOR
    global G_VIEW_MODE, CURRENT_SELECTED_GROUP, CAME_FROM_GROUPED, CURRENT_SELECTED_GROUP_CREATOR
    global GROUPED_VIEW_BY_CREATOR, FAV_PACKS_VIEW_BY_CREATOR

    pack = getattr(inst, 'selected_pose_pack', None)
    if not pack: return
    pack_type = get_pack_type(pack)

    if pack_type == 'POSES': GLOBAL_FAV_PACK_REF = pack
    elif pack_type == 'NORMAL':
        if CURRENT_MODE == MODE_TRACE: CURRENT_MODE = MODE_NORMAL
        if pack != GLOBAL_TRACED_PACK_REF: RETURN_TO_FAV_ON_CLOSE = False

    mode_map = {MODE_NORMAL: STR_MODE_NAME_PLAY, MODE_FAV: STR_MODE_NAME_FAV, MODE_TRACE: STR_MODE_NAME_TRACE}
    current_mode_stbl_id = mode_map.get(CURRENT_MODE, STR_MODE_NAME_PLAY)
    current_mode_str = get_stbl_text(current_mode_stbl_id)

    # ==========================================
    # 动作分组器菜单层级
    # ==========================================
    if pack_type == 'GROUPED_PACKS':
        if not CACHE_BUILT: build_cache_safe()
        
        if G_VIEW_MODE not in (G_MODE_LIST, G_MODE_DELETE_PACK, G_MODE_CREATOR_PACKS):
            G_VIEW_MODE = G_MODE_LIST
            CAME_FROM_GROUPED = False

        if G_VIEW_MODE == G_MODE_LIST:
            yield ObjectPickerRow(name=get_stbl_text(STR_BTN_DELETE_MODE), row_description=get_stbl_text(STR_P_BTN_DELETE_DESC), icon=MY_CUSTOM_ICON, tag="BTN_GROUPED_DELETE_MODE")
            
            view_status_id = STR_G_VIEW_CREATOR if GROUPED_VIEW_BY_CREATOR else STR_G_VIEW_ALL
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_TOGGLE_VIEW, get_stbl_text(view_status_id)), icon=MY_CUSTOM_ICON, tag="BTN_G_TOGGLE_VIEW")

            if GROUPED_VIEW_BY_CREATOR:
                creator_dict = {}
                for pck_id in GROUPED_PACKS.keys():
                    pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                    if pck:
                        found_creator = "Unknown"
                        for c_name, pcks in GLOBAL_ALL_CREATORS_CACHE.items():
                            if pck in pcks: found_creator = c_name; break
                        if found_creator not in creator_dict: creator_dict[found_creator] = []
                        creator_dict[found_creator].append(pck_id)

                for c_name in sorted(creator_dict.keys(), key=lambda x: str(x).lower()):
                    count = len(creator_dict[c_name])
                    # 完美复用原版星星逻辑！
                    c_name_stbl = STR_DYN_CREATOR_STAR if c_name in FAVORITE_CREATORS else STR_DYN_CREATOR_NO_STAR
                    yield ObjectPickerRow(name=get_stbl_text(c_name_stbl, c_name, count), icon=MY_CUSTOM_ICON, tag=f"G_CREATOR::{c_name}")
            else:
                grp_packs_sorted = []
                for pck_id in GROUPED_PACKS.keys():
                    pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                    if pck: grp_packs_sorted.append((getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
                grp_packs_sorted.sort(key=lambda x: str(x[1]).lower())
                for pck_name, pck_id, pck in grp_packs_sorted:
                    yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"G_SELECT::{pck_id}")

        elif G_VIEW_MODE == G_MODE_CREATOR_PACKS:
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RETURN_LIST), icon=MY_CUSTOM_ICON, tag="BTN_GROUPED_RETURN_LIST")
            creator_packs_sorted = []
            for pck_id in GROUPED_PACKS.keys():
                pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                if pck:
                    found_creator = "Unknown"
                    for c_name, pcks in GLOBAL_ALL_CREATORS_CACHE.items():
                        if pck in pcks: found_creator = c_name; break
                    if found_creator == CURRENT_SELECTED_GROUP_CREATOR:
                        creator_packs_sorted.append((getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            creator_packs_sorted.sort(key=lambda x: str(x[1]).lower())
            for pck_name, pck_id, pck in creator_packs_sorted:
                yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"G_SELECT::{pck_id}")

        elif G_VIEW_MODE == G_MODE_DELETE_PACK:
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RETURN_REMOVE), icon=MY_CUSTOM_ICON, tag="BTN_GROUPED_RETURN_LIST")
            del_grp_packs = []
            for pck_id in GROUPED_PACKS.keys():
                pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                if pck: del_grp_packs.append((getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            del_grp_packs.sort(key=lambda x: str(x[1]).lower())
            for pck_name, pck_id, pck in del_grp_packs:
                yield ObjectPickerRow(name=get_stbl_text(STR_DYN_DELETE_ITEM, pck_name), row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"G_DEL_PACK::{pck_id}")
        return

    if CAME_FROM_GROUPED and pack_type == 'NORMAL':
        pack_id = str(getattr(pack, '__name__', 'Unknown'))
        if pack_id not in GROUPED_PACKS: GROUPED_PACKS[pack_id] = {}; save_favorites()

        if G_VIEW_MODE not in (G_MODE_PACK_HOME, G_MODE_PLAY_GROUP, G_MODE_PACK_MANAGE, G_MODE_EDIT_GROUP):
            G_VIEW_MODE = G_MODE_PACK_HOME

        if G_VIEW_MODE == G_MODE_PACK_HOME:
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RETURN_LIST), icon=MY_CUSTOM_ICON, tag="RETURN_TO_GROUPED_LIST")
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_MANAGE_HOME), row_description=get_stbl_text(STR_G_BTN_MANAGE_DESC), icon=MY_CUSTOM_ICON, tag="G_BTN_MANAGE_HOME")
            for grp_name in GROUPED_PACKS[pack_id].keys():
                yield ObjectPickerRow(name=get_stbl_text(STR_G_DYN_PLAY_GRP, str(grp_name)), count=len(GROUPED_PACKS[pack_id][grp_name]), icon=MY_CUSTOM_ICON, tag=f"G_PLAY_GRP::{grp_name}")
                
        elif G_VIEW_MODE == G_MODE_PLAY_GROUP:
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RETURN_UP), icon=MY_CUSTOM_ICON, tag="G_BTN_BACK_TO_HOME")
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_PLAY_ALL), row_description=get_stbl_text(STR_G_DESC_PLAY_ALL), icon=MY_CUSTOM_ICON, tag="G_PLAY_ALL_IN_GROUP")
            valid_poses = GROUPED_PACKS[pack_id].get(CURRENT_SELECTED_GROUP, [])
            for pose_item in getattr(pack, 'pose_list', []):
                if getattr(pose_item, 'pose_name', None) in valid_poses:
                    yield ObjectPickerRow(name=pose_item.pose_display_name, icon=pose_item.icon, tag=pose_item)

        elif G_VIEW_MODE == G_MODE_PACK_MANAGE:
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RETURN_SETTING), icon=MY_CUSTOM_ICON, tag="G_BTN_BACK_TO_HOME")
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_AUTO_SORT), row_description=get_stbl_text(STR_G_BTN_AUTO_DESC), icon=MY_CUSTOM_ICON, tag="G_BTN_AUTO_SORT")
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_ADD_GROUP), icon=MY_CUSTOM_ICON, tag="G_BTN_ADD_GROUP")
            
            for grp_name in GROUPED_PACKS[pack_id].keys():
                # 纯净哈希化：编辑/重命名 按钮
                yield ObjectPickerRow(name=get_stbl_text(STR_G_DYN_EDIT_RENAME_GRP, str(grp_name)), count=len(GROUPED_PACKS[pack_id][grp_name]), icon=MY_CUSTOM_ICON, tag=f"G_EDIT_GRP::{grp_name}")
                yield ObjectPickerRow(name=get_stbl_text(STR_G_DYN_DEL_GRP, str(grp_name)), icon=MY_CUSTOM_ICON, tag=f"G_DEL_GRP::{grp_name}")
                
        elif G_VIEW_MODE == G_MODE_EDIT_GROUP:
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RETURN_SELECT), icon=MY_CUSTOM_ICON, tag="G_BTN_BACK_TO_MANAGE")
            
            # 纯净哈希化：内层的重命名按钮
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RENAME_CURRENT), icon=MY_CUSTOM_ICON, tag=f"G_RENAME_GRP::{CURRENT_SELECTED_GROUP}")
            
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_TOGGLE_ALL), icon=MY_CUSTOM_ICON, tag="G_BTN_TOGGLE_ALL")
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_PATTERN_MATCH), row_description=get_stbl_text(STR_G_PATTERN_DESC), icon=MY_CUSTOM_ICON, tag="G_BTN_PATTERN_MATCH")

            grp_poses = GROUPED_PACKS[pack_id].get(CURRENT_SELECTED_GROUP, [])
            for pose_item in getattr(pack, 'pose_list', []):
                p_name = getattr(pose_item, 'pose_name', None)
                stbl_id = STR_G_DYN_STAR_ITEM if p_name in grp_poses else STR_G_DYN_NO_STAR_ITEM
                yield ObjectPickerRow(name=get_stbl_text(stbl_id, pose_item.pose_display_name), icon=pose_item.icon, tag=f"G_TOGGLE_POSE::{p_name}")
        return
    # ==========================================
    # 收藏动作包 (支持作者分类视图！)
    # ==========================================
    if pack_type == 'FAV_PACKS':
        if not CACHE_BUILT: build_cache_safe()
        
        if FAV_PACKS_VIEW_MODE == P_MODE_FAVS:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_MANAGE), row_description=get_stbl_text(STR_P_BTN_MANAGE_DESC), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_MANAGE")
            yield ObjectPickerRow(name=get_stbl_text(STR_BTN_DELETE_MODE), row_description=get_stbl_text(STR_P_BTN_DELETE_DESC), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_DELETE_MODE")
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_CLEAR), row_description=get_stbl_text(STR_P_BTN_CLEAR_DESC), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_CLEAR")

            view_status_id = STR_G_VIEW_CREATOR if FAV_PACKS_VIEW_BY_CREATOR else STR_G_VIEW_ALL
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_TOGGLE_VIEW, get_stbl_text(view_status_id)), icon=MY_CUSTOM_ICON, tag="BTN_P_TOGGLE_VIEW")

            if FAV_PACKS_VIEW_BY_CREATOR:
                creator_dict = {}
                for pck_id in FAVORITE_PACKS:
                    pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                    if pck:
                        found_creator = "Unknown"
                        for c_name, pcks in GLOBAL_ALL_CREATORS_CACHE.items():
                            if pck in pcks: found_creator = c_name; break
                        if found_creator not in creator_dict: creator_dict[found_creator] = []
                        creator_dict[found_creator].append(pck_id)

                for c_name in sorted(creator_dict.keys(), key=lambda x: str(x).lower()):
                    count = len(creator_dict[c_name])
                    c_name_stbl = STR_DYN_CREATOR_STAR if c_name in FAVORITE_CREATORS else STR_DYN_CREATOR_NO_STAR
                    yield ObjectPickerRow(name=get_stbl_text(c_name_stbl, c_name, count), icon=MY_CUSTOM_ICON, tag=f"P_CREATOR::{c_name}")
            else:
                fav_packs_sorted = []
                for pck_id in FAVORITE_PACKS:
                    pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                    if pck: fav_packs_sorted.append((getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
                fav_packs_sorted.sort(key=lambda x: str(x[1]).lower())
                for pck_name, pck_id, pck in fav_packs_sorted:
                    yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"P_SELECT::{pck_id}")

        elif FAV_PACKS_VIEW_MODE == P_MODE_CREATOR_PACKS:
            yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_RETURN_LIST), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_RETURN")
            creator_packs_sorted = []
            for pck_id in FAVORITE_PACKS:
                pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                if pck:
                    found_creator = "Unknown"
                    for c_name, pcks in GLOBAL_ALL_CREATORS_CACHE.items():
                        if pck in pcks: found_creator = c_name; break
                    if found_creator == CURRENT_SELECTED_FAV_CREATOR:
                        creator_packs_sorted.append((getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            creator_packs_sorted.sort(key=lambda x: str(x[1]).lower())
            for pck_name, pck_id, pck in creator_packs_sorted:
                yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"P_SELECT::{pck_id}")

        elif FAV_PACKS_VIEW_MODE == P_MODE_MANAGE:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_RETURN), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_RETURN")
            all_packs_sorted = []
            for pck_id, pck in GLOBAL_ALL_PACKS_CACHE.items():
                sn, dn = str(getattr(pck, 'sort_name', "")).strip().lower(), str(getattr(pck, 'display_name', "")).strip().lower()
                if not sn or sn in ('', 'unknown', '0x00000000', 'none', 'nan', '0x0', '0') or dn in ('0x00000000', '0x0'): continue
                all_packs_sorted.append((getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            all_packs_sorted.sort(key=lambda x: str(x[1]).lower())
            for pck_name, pck_id, pck in all_packs_sorted:
                yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"P_TOGGLE::{pck_id}")

        elif FAV_PACKS_VIEW_MODE == P_MODE_DELETE:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_RETURN), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_RETURN")
            del_packs_sorted = []
            for pck_id in FAVORITE_PACKS:
                pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                if pck: del_packs_sorted.append((getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            del_packs_sorted.sort(key=lambda x: str(x[1]).lower())
            for pck_name, pck_id, pck in del_packs_sorted:
                yield ObjectPickerRow(name=get_stbl_text(STR_DYN_DELETE_ITEM, pck_name), row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"P_DELETE::{pck_id}")
        return

    # ==========================================
    # 以下为剩余收藏模块 (保持不变)
    # ==========================================
    if pack_type == 'CREATORS':
        if not CACHE_BUILT: build_cache_safe()

        if CREATOR_VIEW_MODE == C_MODE_FAVS:
            yield ObjectPickerRow(name=get_stbl_text(STR_C_BTN_ADD), icon=MY_CUSTOM_ICON, tag="BTN_ALL_CREATORS")
            yield ObjectPickerRow(name=get_stbl_text(STR_BTN_DELETE_MODE), row_description=get_stbl_text(STR_C_BTN_DELETE_DESC), icon=MY_CUSTOM_ICON, tag="BTN_CREATORS_DELETE_MODE")
            if not FAVORITE_CREATORS:
                yield ObjectPickerRow(name=get_stbl_text(STR_C_EMPTY), icon=MY_CUSTOM_ICON)
            else:
                for creator in sorted(FAVORITE_CREATORS):
                    if creator in GLOBAL_ALL_CREATORS_CACHE:
                        count = len(GLOBAL_ALL_CREATORS_CACHE[creator])
                        yield ObjectPickerRow(name=get_stbl_text(STR_DYN_CREATOR_FAVED, creator, count), icon=MY_CUSTOM_ICON, tag=f"C_VIEW::{creator}")

        elif CREATOR_VIEW_MODE == C_MODE_ALL:
            yield ObjectPickerRow(name=get_stbl_text(STR_C_BTN_RETURN_LIST), icon=MY_CUSTOM_ICON, tag="BTN_RETURN_FAV_CREATORS")
            for creator in sorted(GLOBAL_ALL_CREATORS_CACHE.keys()):
                count = len(GLOBAL_ALL_CREATORS_CACHE[creator])
                c_name_stbl = STR_DYN_CREATOR_STAR if creator in FAVORITE_CREATORS else STR_DYN_CREATOR_NO_STAR
                yield ObjectPickerRow(name=get_stbl_text(c_name_stbl, creator, count), icon=MY_CUSTOM_ICON, tag=f"C_TOGGLE::{creator}")

        elif CREATOR_VIEW_MODE == C_MODE_PACKS:
            yield ObjectPickerRow(name=get_stbl_text(STR_C_BTN_RETURN_FAVS), icon=MY_CUSTOM_ICON, tag="BTN_RETURN_FAV_CREATORS")
            packs = GLOBAL_ALL_CREATORS_CACHE.get(CURRENT_SELECTED_CREATOR, [])
            packs_sorted = sorted(packs, key=lambda x: str(getattr(x, 'display_name', getattr(x, 'sort_name', ''))).lower())
            for pck in packs_sorted:
                idx = packs.index(pck)
                pck_name = getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or getattr(pck, '__name__', 'Unknown Pack')
                yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None), count=len(getattr(pck, 'pose_list', [])), icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"CREATOR_PACK::{CURRENT_SELECTED_CREATOR}::{idx}")

        elif CREATOR_VIEW_MODE == C_MODE_DELETE:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_RETURN), icon=MY_CUSTOM_ICON, tag="BTN_CREATORS_RETURN_FAVS")
            for creator in sorted(FAVORITE_CREATORS):
                yield ObjectPickerRow(name=get_stbl_text(STR_DYN_DELETE_ITEM, creator), icon=MY_CUSTOM_ICON, tag=f"C_DELETE::{creator}")
        return

    if pack_type == 'POSES':
        if not CACHE_BUILT: build_cache_safe()
        yield ObjectPickerRow(name=get_stbl_text(STR_DYN_TOGGLE_MODE_1, current_mode_str), row_description=get_stbl_text(STR_DYN_TOGGLE_MODE_1_DESC), icon=MY_CUSTOM_ICON, tag="TOGGLE_MODE_BTN")
        yield ObjectPickerRow(name=get_stbl_text(STR_S_BTN_CLEAR), row_description=get_stbl_text(STR_S_BTN_CLEAR_DESC), icon=MY_CUSTOM_ICON, tag="CLEAR_ALL_FAV_BTN")

        if not FAVORITE_POSES:
            yield ObjectPickerRow(name=get_stbl_text(STR_S_EMPTY), icon=MY_CUSTOM_ICON)
        else:
            fav_display_list = [GLOBAL_ALL_POSES_CACHE.get(p) for p in FAVORITE_POSES if 'fgeh' not in str(p).lower() and GLOBAL_ALL_POSES_CACHE.get(p)]
            fav_display_list.sort(key=lambda x: x['pack_name'])
            for item in fav_display_list:
                p = item['pose']
                yield ObjectPickerRow(name=p.pose_display_name, icon=p.icon, row_description=p.pose_description, tag=p)
        return

    if RETURN_TO_FAV_ON_CLOSE and pack == GLOBAL_TRACED_PACK_REF:
        yield ObjectPickerRow(name=get_stbl_text(STR_N_RETURN_TO_POSES), icon=MY_CUSTOM_ICON, tag="RETURN_TO_FAV_BTN")

    if CAME_FROM_L1_FAVS:
        yield ObjectPickerRow(name=get_stbl_text(STR_N_RETURN_TO_PACKS), icon=MY_CUSTOM_ICON, tag="RETURN_TO_FAV_PACKS_MENU_BTN")

    if CAME_FROM_CREATOR and CURRENT_SELECTED_CREATOR:
        yield ObjectPickerRow(name=get_stbl_text(STR_DYN_RETURN_CREATOR, CURRENT_SELECTED_CREATOR), icon=MY_CUSTOM_ICON, tag="RETURN_TO_CREATOR_PACKS_BTN")

    yield ObjectPickerRow(name=get_stbl_text(STR_DYN_TOGGLE_MODE_2, current_mode_str), icon=MY_CUSTOM_ICON, tag="TOGGLE_MODE_BTN")

    pack_id = str(getattr(pack, '__name__', 'Unknown'))
    is_pack_faved = pack_id in FAVORITE_PACKS
    is_grouped = pack_id in GROUPED_PACKS
    
    # 收藏动作包与分组器的联动按钮
    grp_btn_id = STR_G_BTN_REMOVE_PACK if is_grouped else STR_G_BTN_ADD_PACK
    yield ObjectPickerRow(name=get_stbl_text(grp_btn_id), row_description=get_stbl_text(STR_G_PACK_DESC), icon=MY_CUSTOM_ICON, tag="TOGGLE_GROUPED_PACK_ONLY_BTN")
    
    # 【新增】：虫洞按钮直达！
    if is_grouped:
        yield ObjectPickerRow(name=get_stbl_text(STR_G_BTN_WORMHOLE), row_description=get_stbl_text(STR_G_WORMHOLE_DESC), icon=MY_CUSTOM_ICON, tag="BTN_G_WORMHOLE_JUMP")

    names = [p.pose_name for p in getattr(pack, 'pose_list', []) if hasattr(p, 'pose_name')]
    is_all_poses_faved = bool(names) and all(n in FAVORITE_POSES for n in names)

    pack_btn_id = STR_N_REMOVE_PACK if is_pack_faved else STR_N_ADD_PACK
    pose_btn_id = STR_N_REMOVE_ALL_POSES if is_all_poses_faved else STR_N_ADD_ALL_POSES

    yield ObjectPickerRow(name=get_stbl_text(pack_btn_id), row_description=get_stbl_text(STR_N_PACK_DESC), icon=MY_CUSTOM_ICON, tag="TOGGLE_FAV_PACK_ONLY_BTN")
    yield ObjectPickerRow(name=get_stbl_text(pose_btn_id), row_description=get_stbl_text(STR_N_ALL_POSES_DESC), icon=MY_CUSTOM_ICON, tag="TOGGLE_FAV_ALL_POSES_ONLY_BTN")

    for pose_item in getattr(pack, 'pose_list', []):
        yield ObjectPickerRow(name=pose_item.pose_display_name, icon=pose_item.icon, tag=pose_item)


# ==========================================
# 路由点击处理区
# ==========================================
original_pose_on_choice = poseplayer.PoseByPackNameInteraction.on_choice_selected

def custom_pose_on_choice(self, choice_tag, **kwargs):
    global CURRENT_MODE, RETURN_TO_FAV_ON_CLOSE, GLOBAL_FAV_PACK_REF, GLOBAL_TRACED_PACK_REF
    global CREATOR_VIEW_MODE, CURRENT_SELECTED_CREATOR, FAVORITE_PACKS, FAVORITE_POSES
    global CAME_FROM_CREATOR, CAME_FROM_L1_FAVS, FAV_PACKS_VIEW_MODE, CURRENT_SELECTED_FAV_CREATOR
    global G_VIEW_MODE, CURRENT_SELECTED_GROUP, CAME_FROM_GROUPED, GROUPED_PACKS
    global GROUPED_VIEW_BY_CREATOR, CURRENT_SELECTED_GROUP_CREATOR, FAV_PACKS_VIEW_BY_CREATOR

    pack_type = get_pack_type(self.selected_pose_pack)

    if choice_tag is None or not isinstance(choice_tag, str):
        if hasattr(choice_tag, 'pose_name'):
            p_name = choice_tag.pose_name
            if CURRENT_MODE == MODE_FAV:
                if p_name in FAVORITE_POSES: FAVORITE_POSES.remove(p_name)
                else: FAVORITE_POSES.append(p_name)
                save_favorites()
                return self._show_picker_dialog(self.sim, target_sim=self.target)

            if CURRENT_MODE == MODE_TRACE:
                build_cache_safe()
                info = GLOBAL_ALL_POSES_CACHE.get(p_name)
                if info:
                    self.selected_pose_pack = info['pack_ref']
                    GLOBAL_TRACED_PACK_REF = info['pack_ref']
                    RETURN_TO_FAV_ON_CLOSE = True
                    CAME_FROM_L1_FAVS = False
                    CAME_FROM_CREATOR = False
                    CAME_FROM_GROUPED = False
                    CURRENT_MODE = MODE_NORMAL
                    return self._show_picker_dialog(self.sim, target_sim=self.target)
                    
            if CURRENT_MODE == MODE_NORMAL:
                from interactions.context import QueueInsertStrategy
                from interactions.priority import Priority
                self.interaction_parameters['pose_name'] = p_name
                self.push_tunable_continuation((self.continuation), pose_name=p_name, insert_strategy=(QueueInsertStrategy.LAST), priority=Priority.High, actor=(self.target))
                return self._show_picker_dialog(self.sim, target_sim=self.target)

        return original_pose_on_choice(self, choice_tag, **kwargs)

    # 收藏动作包视图切换功能
    if choice_tag == "BTN_P_TOGGLE_VIEW":
        FAV_PACKS_VIEW_BY_CREATOR = not FAV_PACKS_VIEW_BY_CREATOR
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag.startswith("P_CREATOR::"):
        CURRENT_SELECTED_FAV_CREATOR = choice_tag.split("::")[1]
        FAV_PACKS_VIEW_MODE = P_MODE_CREATOR_PACKS
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_G_TOGGLE_VIEW":
        GROUPED_VIEW_BY_CREATOR = not GROUPED_VIEW_BY_CREATOR
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)
        
    if choice_tag.startswith("G_CREATOR::"):
        CURRENT_SELECTED_GROUP_CREATOR = choice_tag.split("::")[1]
        G_VIEW_MODE = G_MODE_CREATOR_PACKS
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_GROUPED_RETURN_LIST":
        G_VIEW_MODE = G_MODE_LIST
        return self._show_picker_dialog(self.sim, target_sim=self.target)
        
    if choice_tag == "RETURN_TO_GROUPED_LIST":
        self.selected_pose_pack = "fgeh_grouped_folder"
        G_VIEW_MODE = G_MODE_CREATOR_PACKS if GROUPED_VIEW_BY_CREATOR and CURRENT_SELECTED_GROUP_CREATOR else G_MODE_LIST
        CAME_FROM_GROUPED = False
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_GROUPED_DELETE_MODE": G_VIEW_MODE = G_MODE_DELETE_PACK; return self._show_picker_dialog(self.sim, target_sim=self.target)
    
    if choice_tag.startswith("G_SELECT::"):
        pck_id = choice_tag.split("::")[1]
        pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
        if pck:
            self.selected_pose_pack = pck
            CAME_FROM_GROUPED = True
            CAME_FROM_L1_FAVS = False
            CAME_FROM_CREATOR = False
            G_VIEW_MODE = G_MODE_PACK_HOME
            return self._show_picker_dialog(self.sim, target_sim=self.target)
            
    if choice_tag.startswith("G_DEL_PACK::"):
        pck_id = choice_tag.split("::")[1]
        if pck_id in GROUPED_PACKS: del GROUPED_PACKS[pck_id]; save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    # 虫洞跳跃！
    if choice_tag == "BTN_G_WORMHOLE_JUMP":
        CAME_FROM_GROUPED = True
        G_VIEW_MODE = G_MODE_PACK_HOME
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "G_PLAY_ALL_IN_GROUP":
        pack_id = str(getattr(self.selected_pose_pack, '__name__', 'Unknown'))
        valid_poses = GROUPED_PACKS.get(pack_id, {}).get(CURRENT_SELECTED_GROUP, [])
        for pose_item in getattr(self.selected_pose_pack, 'pose_list', []):
            p_name = getattr(pose_item, 'pose_name', None)
            if p_name in valid_poses:
                self.interaction_parameters['pose_name'] = p_name
                from interactions.context import QueueInsertStrategy
                from interactions.priority import Priority
                self.push_tunable_continuation((self.continuation), pose_name=p_name, insert_strategy=(QueueInsertStrategy.LAST), priority=Priority.High, actor=(self.target))
        return self._show_picker_dialog(self.sim, target_sim=self.target)
        
    if choice_tag == "G_BTN_MANAGE_HOME": G_VIEW_MODE = G_MODE_PACK_MANAGE; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag == "G_BTN_BACK_TO_HOME": G_VIEW_MODE = G_MODE_PACK_HOME; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag == "G_BTN_BACK_TO_MANAGE": G_VIEW_MODE = G_MODE_PACK_MANAGE; return self._show_picker_dialog(self.sim, target_sim=self.target)
    
    pack_id = str(getattr(self.selected_pose_pack, '__name__', 'Unknown'))
    
    if choice_tag.startswith("G_PLAY_GRP::"):
        CURRENT_SELECTED_GROUP = choice_tag.split("::")[1]
        G_VIEW_MODE = G_MODE_PLAY_GROUP
        return self._show_picker_dialog(self.sim, target_sim=self.target)
        
    if choice_tag.startswith("G_EDIT_GRP::"):
        CURRENT_SELECTED_GROUP = choice_tag.split("::")[1]
        G_VIEW_MODE = G_MODE_EDIT_GROUP
        return self._show_picker_dialog(self.sim, target_sim=self.target)
        
    # ... 在 if choice_tag.startswith("G_DEL_GRP::"): 这段代码的下面加入： ...

    # ==========================================
    # 【新增】重命名组 (白嫖原作者的文本框)
    # ==========================================
    # ==========================================
    # 重命名组 (纯净全哈希弹窗版)
    # ==========================================
    if choice_tag.startswith("G_RENAME_GRP::"):
        old_grp_name = choice_tag.split("::")[1]
        
        import services, sims4.resources
        pose_by_name_interaction = services.get_instance_manager(sims4.resources.Types.INTERACTION).get(15221397919050208516)
        
        if pose_by_name_interaction:
            def on_rename_response(dialog):
                if not dialog.accepted:
                    self._show_picker_dialog(self.sim, target_sim=self.target)
                    return
                
                new_name = dialog.text_input_responses.get('pose_name')
                if new_name and new_name.strip():
                    new_name = new_name.strip()
                    if new_name != old_grp_name and new_name not in GROUPED_PACKS[pack_id]:
                        GROUPED_PACKS[pack_id][new_name] = GROUPED_PACKS[pack_id].pop(old_grp_name)
                        global CURRENT_SELECTED_GROUP
                        CURRENT_SELECTED_GROUP = new_name 
                        save_favorites()
                        
                self._show_picker_dialog(self.sim, target_sim=self.target)

            from sims4.localization import LocalizationHelperTuning
            # 这里的 old_grp_name 是内存里的动态变量，不需要哈希
            text_input_overrides = {'pose_name': lambda *_, **__: LocalizationHelperTuning.get_raw_text(old_grp_name)}
            
            dialog = pose_by_name_interaction.pose_dialog(self.sim, self.get_resolver())
            
            # 【纯净哈希化】：直接调用 get_stbl_text 获取你录入的 STBL
            dialog.title = lambda *_, **__: get_stbl_text(STR_G_RENAME_DIALOG_TITLE)
            dialog.text = lambda *_, **__: get_stbl_text(STR_G_RENAME_DIALOG_TEXT)
            
            dialog.show_dialog(on_response=on_rename_response, text_input_overrides=text_input_overrides)
            
        return
    
    if choice_tag == "G_BTN_AUTO_SORT":
        GROUPED_PACKS[pack_id] = auto_sort_couple_pack(self.selected_pose_pack)
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)
        
    if choice_tag == "G_BTN_ADD_GROUP":
        n = len(GROUPED_PACKS.get(pack_id, {})) + 1
        new_grp = f"分组 {n}"
        while new_grp in GROUPED_PACKS.get(pack_id, {}):
            n += 1
            new_grp = f"分组 {n}"
        if pack_id not in GROUPED_PACKS: GROUPED_PACKS[pack_id] = {}
        GROUPED_PACKS[pack_id][new_grp] = []
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "G_BTN_TOGGLE_ALL":
        pose_list = getattr(self.selected_pose_pack, 'pose_list', [])
        all_pose_names = [getattr(p, 'pose_name', None) for p in pose_list if getattr(p, 'pose_name', None)]
        current_grp = GROUPED_PACKS.get(pack_id, {}).get(CURRENT_SELECTED_GROUP, [])
        if len(current_grp) == len(all_pose_names):
            GROUPED_PACKS[pack_id][CURRENT_SELECTED_GROUP] = []
        else:
            GROUPED_PACKS[pack_id][CURRENT_SELECTED_GROUP] = all_pose_names
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "G_BTN_PATTERN_MATCH":
        pose_list = getattr(self.selected_pose_pack, 'pose_list', [])
        current_grp = GROUPED_PACKS.get(pack_id, {}).get(CURRENT_SELECTED_GROUP, [])
        selected_indices = []
        for i, p in enumerate(pose_list):
            if getattr(p, 'pose_name', None) in current_grp:
                selected_indices.append(i)
        if len(selected_indices) >= 2:
            start_idx = selected_indices[0]
            interval = selected_indices[1] - selected_indices[0]
            if interval > 0:
                new_grp = []
                for i in range(start_idx, len(pose_list), interval):
                    p_name = getattr(pose_list[i], 'pose_name', None)
                    if p_name: new_grp.append(p_name)
                GROUPED_PACKS[pack_id][CURRENT_SELECTED_GROUP] = new_grp
                save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag.startswith("G_TOGGLE_POSE::"):
        p_name = choice_tag.split("::")[1]
        target_list = GROUPED_PACKS.get(pack_id, {}).get(CURRENT_SELECTED_GROUP, [])
        if p_name in target_list: target_list.remove(p_name)
        else: target_list.append(p_name)
        GROUPED_PACKS[pack_id][CURRENT_SELECTED_GROUP] = target_list
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "TOGGLE_GROUPED_PACK_ONLY_BTN":
        if pack_id in GROUPED_PACKS: del GROUPED_PACKS[pack_id]
        else: GROUPED_PACKS[pack_id] = {}
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)


    # ==========================================
    # 以下处理逻辑 (保持不变)
    # ==========================================
    if choice_tag == "BTN_FAV_PACKS_DELETE_MODE": FAV_PACKS_VIEW_MODE = P_MODE_DELETE; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag.startswith("P_DELETE::"):
        pck_id = choice_tag.split("::")[1]
        if pck_id in FAVORITE_PACKS:
            FAVORITE_PACKS.remove(pck_id)
            save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "RETURN_TO_FAV_PACKS_MENU_BTN":
        self.selected_pose_pack = "fgeh_fav_packs_folder"
        FAV_PACKS_VIEW_MODE = P_MODE_CREATOR_PACKS if FAV_PACKS_VIEW_BY_CREATOR and CURRENT_SELECTED_FAV_CREATOR else P_MODE_FAVS
        CAME_FROM_L1_FAVS = False
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_FAV_PACKS_MANAGE": FAV_PACKS_VIEW_MODE = P_MODE_MANAGE; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag == "BTN_FAV_PACKS_RETURN": FAV_PACKS_VIEW_MODE = P_MODE_FAVS; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag == "BTN_FAV_PACKS_CLEAR": FAVORITE_PACKS.clear(); save_favorites(); return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag.startswith("P_TOGGLE::"):
        pck_id = choice_tag.split("::")[1]
        if pck_id in FAVORITE_PACKS: FAVORITE_PACKS.remove(pck_id)
        else: FAVORITE_PACKS.append(pck_id)
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag.startswith("P_SELECT::"):
        pck_id = choice_tag.split("::")[1]
        pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
        if pck:
            self.selected_pose_pack = pck
            CURRENT_MODE = MODE_NORMAL
            CAME_FROM_L1_FAVS = True
            CAME_FROM_CREATOR = False
            CAME_FROM_GROUPED = False
            RETURN_TO_FAV_ON_CLOSE = False
            return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_CREATORS_DELETE_MODE": CREATOR_VIEW_MODE = C_MODE_DELETE; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag == "BTN_CREATORS_RETURN_FAVS": CREATOR_VIEW_MODE = C_MODE_FAVS; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag.startswith("C_DELETE::"):
        creator = choice_tag.split("::")[1]
        if creator in FAVORITE_CREATORS:
            FAVORITE_CREATORS.remove(creator)
            save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "RETURN_TO_CREATOR_PACKS_BTN":
        self.selected_pose_pack = "hegfcreator_folder"
        CREATOR_VIEW_MODE = C_MODE_PACKS
        CAME_FROM_CREATOR = False
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_ALL_CREATORS": CREATOR_VIEW_MODE = C_MODE_ALL; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag == "BTN_RETURN_FAV_CREATORS": CREATOR_VIEW_MODE = C_MODE_FAVS; CURRENT_SELECTED_CREATOR = None; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag.startswith("C_VIEW::"): CREATOR_VIEW_MODE = C_MODE_PACKS; CURRENT_SELECTED_CREATOR = choice_tag.split("::")[1]; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag.startswith("C_TOGGLE::"):
        creator = choice_tag.split("::")[1]
        if creator in FAVORITE_CREATORS: FAVORITE_CREATORS.remove(creator)
        else: FAVORITE_CREATORS.append(creator)
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag.startswith("CREATOR_PACK::"):
        parts = choice_tag.split("::")
        if len(parts) >= 3:
            packs = GLOBAL_ALL_CREATORS_CACHE.get(parts[1], [])
            pack_idx = int(parts[2])
            if 0 <= pack_idx < len(packs):
                self.selected_pose_pack = packs[pack_idx]
                CURRENT_MODE = MODE_NORMAL
                CAME_FROM_CREATOR = True
                CAME_FROM_L1_FAVS = False
                CAME_FROM_GROUPED = False
                RETURN_TO_FAV_ON_CLOSE = False
                return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "TOGGLE_MODE_BTN":
        if pack_type == 'POSES': CURRENT_MODE = (CURRENT_MODE + 1) % 3
        else: CURRENT_MODE = MODE_FAV if CURRENT_MODE == MODE_NORMAL else MODE_NORMAL
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "RETURN_TO_FAV_BTN":
        if GLOBAL_FAV_PACK_REF:
            self.selected_pose_pack = GLOBAL_FAV_PACK_REF
            RETURN_TO_FAV_ON_CLOSE = False
            return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "TOGGLE_FAV_PACK_ONLY_BTN":
        pack = self.selected_pose_pack
        pack_id = str(getattr(pack, '__name__', 'Unknown'))
        if pack_id in FAVORITE_PACKS: FAVORITE_PACKS.remove(pack_id)
        else: FAVORITE_PACKS.append(pack_id)
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "TOGGLE_FAV_ALL_POSES_ONLY_BTN":
        pack = self.selected_pose_pack
        names = [p.pose_name for p in getattr(pack, 'pose_list', []) if hasattr(p, 'pose_name')]
        is_fully_faved = bool(names) and all(n in FAVORITE_POSES for n in names)

        if is_fully_faved:
            for n in names:
                if n in FAVORITE_POSES: FAVORITE_POSES.remove(n)
        else:
            for n in names:
                if n not in FAVORITE_POSES: FAVORITE_POSES.append(n)
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "CLEAR_ALL_FAV_BTN":
        FAVORITE_POSES.clear()
        save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

# === 挂载点 ===
try:
    load_favorites()
    poseplayer.PoseByPackNameInteraction.picker_rows_gen = custom_pose_rows_gen
    poseplayer.PoseByPackNameInteraction.on_choice_selected = custom_pose_on_choice
except:
    pass