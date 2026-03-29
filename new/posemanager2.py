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

# 新增的管理模式哈希值 (沿用你刚才配好的)
STR_BTN_DELETE_MODE = 0x11DDB545
STR_P_BTN_DELETE_DESC = 0xBBDE2231
STR_C_BTN_DELETE_DESC = 0x83FDF125  # 借用你刚才加的S的描述，用在作者管理里
STR_DYN_DELETE_ITEM = 0xB1161D76


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
FAVORITE_POSES, FAVORITE_CREATORS, FAVORITE_PACKS = [], [], []
GLOBAL_ALL_POSES_CACHE, GLOBAL_ALL_CREATORS_CACHE, GLOBAL_ALL_PACKS_CACHE = {}, {}, {}
CACHE_BUILT = False
GLOBAL_FAV_PACK_REF, GLOBAL_TRACED_PACK_REF, RETURN_TO_FAV_ON_CLOSE = None, None, False

P_MODE_FAVS, P_MODE_MANAGE, P_MODE_DELETE = 0, 1, 2
FAV_PACKS_VIEW_MODE = P_MODE_FAVS

# 【修改】给作者收藏增加删除模式 C_MODE_DELETE
C_MODE_FAVS, C_MODE_ALL, C_MODE_PACKS, C_MODE_DELETE = 0, 1, 2, 3
CREATOR_VIEW_MODE = C_MODE_FAVS
CURRENT_SELECTED_CREATOR = None


# === 文件系统 ===
def get_mod_directory():
    try:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except:
        return ''


FAV_FILE = os.path.join(get_mod_directory(), 'my_favorite_poses.json')
FAV_CREATORS_FILE = os.path.join(get_mod_directory(), 'my_favorite_creators.json')
FAV_PACKS_FILE = os.path.join(get_mod_directory(), 'my_favorite_packs.json')


def load_favorites():
    global FAVORITE_POSES, FAVORITE_CREATORS, FAVORITE_PACKS
    if os.path.exists(FAV_FILE):
        try:
            with open(FAV_FILE, 'r', encoding='utf-8') as f:
                FAVORITE_POSES = list(dict.fromkeys(json.load(f)))
        except:
            pass
    if os.path.exists(FAV_CREATORS_FILE):
        try:
            with open(FAV_CREATORS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                FAVORITE_CREATORS = list(dict.fromkeys(data))
        except:
            pass
    if os.path.exists(FAV_PACKS_FILE):
        try:
            with open(FAV_PACKS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                FAVORITE_PACKS = list(dict.fromkeys(data))
        except:
            pass


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


def get_pack_type(pack):
    if not pack: return 'NORMAL'
    combined_str = str(pack).lower() if isinstance(pack, str) else str(getattr(pack, '__name__', '')).lower()
    if not isinstance(pack, str) and hasattr(pack, 'pose_list'):
        combined_str += " " + " ".join(
            [str(getattr(p, 'pose_name', '')).lower() for p in getattr(pack, 'pose_list', [])])

    if 'hegfcreator' in combined_str: return 'CREATORS'
    if 'fgeh_poses' in combined_str: return 'POSES'
    if 'fgeh_fav_packs' in combined_str: return 'FAV_PACKS'
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
    except:
        CACHE_BUILT = True


# ==========================================
# 第一部分：第一层 UI
# ==========================================
target_cls = getattr(poseplayer, 'PoseByPackInteraction', None)

if target_cls is not None and not isinstance(target_cls, str):
    @injector2.inject(target_cls, 'picker_rows_gen')
    def custom_pack_rows_gen_safe(original, *args, **kwargs):
        try:
            if hasattr(target_cls, 'POSE_PACKS'): target_cls.POSE_PACKS = None
            try:
                gen = original(*args, **kwargs)
            except TypeError:
                gen = original(*args[1:], **kwargs)

            yield ObjectPickerRow(name=get_stbl_text(STR_L1_FAV_PACKS_TITLE),
                                  row_description=get_stbl_text(STR_L1_FAV_PACKS_DESC), icon=MY_CUSTOM_ICON,
                                  tag="fgeh_fav_packs_folder")
            yield ObjectPickerRow(name=get_stbl_text(STR_L1_CREATORS_TITLE),
                                  row_description=get_stbl_text(STR_L1_CREATORS_DESC), icon=MY_CUSTOM_ICON,
                                  tag="hegfcreator_folder")
            yield ObjectPickerRow(name=get_stbl_text(STR_L1_POSES_TITLE),
                                  row_description=get_stbl_text(STR_L1_POSES_DESC), icon=MY_CUSTOM_ICON,
                                  tag="fgeh_poses_folder")

            seen_tags = {"fgeh_fav_packs_folder", "hegfcreator_folder", "fgeh_poses_folder"}
            for row in gen:
                if row.tag in seen_tags: continue
                pack = row.tag
                if get_pack_type(pack) == 'NORMAL':
                    sn, dn = str(getattr(pack, 'sort_name', "")).strip().lower(), str(
                        getattr(pack, 'display_name', "")).strip().lower()
                    if not sn or sn in ('', 'unknown', '0x00000000', 'none', 'nan', '0x0', '0') or dn in (
                    '0x00000000', '0x0'):
                        continue
                yield row
        except:
            try:
                yield from original(*args, **kwargs)
            except TypeError:
                yield from original(*args[1:], **kwargs)


# ==========================================
# 第二部分：第二层 UI (菜单渲染)
# ==========================================
def custom_pose_rows_gen(inst, target, context, **kwargs):
    global CURRENT_MODE, GLOBAL_FAV_PACK_REF, RETURN_TO_FAV_ON_CLOSE, GLOBAL_TRACED_PACK_REF
    global CREATOR_VIEW_MODE, CURRENT_SELECTED_CREATOR, CAME_FROM_L1_FAVS, CAME_FROM_CREATOR
    global FAV_PACKS_VIEW_MODE

    pack = getattr(inst, 'selected_pose_pack', None)
    if not pack: return
    pack_type = get_pack_type(pack)

    if pack_type == 'POSES':
        GLOBAL_FAV_PACK_REF = pack
    elif pack_type == 'NORMAL':
        if CURRENT_MODE == MODE_TRACE: CURRENT_MODE = MODE_NORMAL
        if pack != GLOBAL_TRACED_PACK_REF: RETURN_TO_FAV_ON_CLOSE = False

    mode_map = {MODE_NORMAL: STR_MODE_NAME_PLAY, MODE_FAV: STR_MODE_NAME_FAV, MODE_TRACE: STR_MODE_NAME_TRACE}
    current_mode_stbl_id = mode_map.get(CURRENT_MODE, STR_MODE_NAME_PLAY)
    current_mode_str = get_stbl_text(current_mode_stbl_id)

    # --- 动作包收藏夹 ---
    if pack_type == 'FAV_PACKS':
        if not CACHE_BUILT: build_cache_safe()

        if FAV_PACKS_VIEW_MODE == P_MODE_FAVS:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_MANAGE),
                                  row_description=get_stbl_text(STR_P_BTN_MANAGE_DESC), icon=MY_CUSTOM_ICON,
                                  tag="BTN_FAV_PACKS_MANAGE")
            yield ObjectPickerRow(name=get_stbl_text(STR_BTN_DELETE_MODE),
                                  row_description=get_stbl_text(STR_P_BTN_DELETE_DESC), icon=MY_CUSTOM_ICON,
                                  tag="BTN_FAV_PACKS_DELETE_MODE")
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_CLEAR),
                                  row_description=get_stbl_text(STR_P_BTN_CLEAR_DESC), icon=MY_CUSTOM_ICON,
                                  tag="BTN_FAV_PACKS_CLEAR")

            fav_packs_sorted = []
            for pck_id in FAVORITE_PACKS:
                pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                if pck: fav_packs_sorted.append(
                    (getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            fav_packs_sorted.sort(key=lambda x: str(x[0]).lower())

            for pck_name, pck_id, pck in fav_packs_sorted:
                yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None),
                                      count=len(getattr(pck, 'pose_list', [])),
                                      icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"P_SELECT::{pck_id}")

        elif FAV_PACKS_VIEW_MODE == P_MODE_MANAGE:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_RETURN), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_RETURN")

            all_packs_sorted = []
            for pck_id, pck in GLOBAL_ALL_PACKS_CACHE.items():
                sn, dn = str(getattr(pck, 'sort_name', "")).strip().lower(), str(
                    getattr(pck, 'display_name', "")).strip().lower()
                if not sn or sn in ('', 'unknown', '0x00000000', 'none', 'nan', '0x0', '0') or dn in (
                '0x00000000', '0x0'): continue
                all_packs_sorted.append(
                    (getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            all_packs_sorted.sort(key=lambda x: str(x[1]).lower())

            for pck_name, pck_id, pck in all_packs_sorted:
                yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None),
                                      count=len(getattr(pck, 'pose_list', [])),
                                      icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"P_TOGGLE::{pck_id}")

        elif FAV_PACKS_VIEW_MODE == P_MODE_DELETE:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_RETURN), icon=MY_CUSTOM_ICON, tag="BTN_FAV_PACKS_RETURN")

            del_packs_sorted = []
            for pck_id in FAVORITE_PACKS:
                pck = GLOBAL_ALL_PACKS_CACHE.get(pck_id)
                if pck: del_packs_sorted.append(
                    (getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or pck_id, pck_id, pck))
            del_packs_sorted.sort(key=lambda x: str(x[0]).lower())

            for pck_name, pck_id, pck in del_packs_sorted:
                # 【修复核心：去掉 str(pck_name)，直接传 EA LocalizedString，彻底解决 hash 显示问题】
                yield ObjectPickerRow(name=get_stbl_text(STR_DYN_DELETE_ITEM, pck_name),
                                      row_description=getattr(pck, 'description', None),
                                      count=len(getattr(pck, 'pose_list', [])),
                                      icon=getattr(pck, 'icon', MY_CUSTOM_ICON), tag=f"P_DELETE::{pck_id}")
        return

    # --- 作者收藏夹 ---
    if pack_type == 'CREATORS':
        if not CACHE_BUILT: build_cache_safe()

        if CREATOR_VIEW_MODE == C_MODE_FAVS:
            yield ObjectPickerRow(name=get_stbl_text(STR_C_BTN_ADD), icon=MY_CUSTOM_ICON, tag="BTN_ALL_CREATORS")
            # 【新增：作者管理删除按钮】
            yield ObjectPickerRow(name=get_stbl_text(STR_BTN_DELETE_MODE),
                                  row_description=get_stbl_text(STR_C_BTN_DELETE_DESC), icon=MY_CUSTOM_ICON,
                                  tag="BTN_CREATORS_DELETE_MODE")

            if not FAVORITE_CREATORS:
                yield ObjectPickerRow(name=get_stbl_text(STR_C_EMPTY), icon=MY_CUSTOM_ICON)
            else:
                for creator in sorted(FAVORITE_CREATORS):
                    if creator in GLOBAL_ALL_CREATORS_CACHE:
                        count = len(GLOBAL_ALL_CREATORS_CACHE[creator])
                        yield ObjectPickerRow(name=get_stbl_text(STR_DYN_CREATOR_FAVED, creator, count),
                                              icon=MY_CUSTOM_ICON, tag=f"C_VIEW::{creator}")

        elif CREATOR_VIEW_MODE == C_MODE_ALL:
            yield ObjectPickerRow(name=get_stbl_text(STR_C_BTN_RETURN_LIST), icon=MY_CUSTOM_ICON,
                                  tag="BTN_RETURN_FAV_CREATORS")
            for creator in sorted(GLOBAL_ALL_CREATORS_CACHE.keys()):
                count = len(GLOBAL_ALL_CREATORS_CACHE[creator])
                c_name_stbl = STR_DYN_CREATOR_STAR if creator in FAVORITE_CREATORS else STR_DYN_CREATOR_NO_STAR
                yield ObjectPickerRow(name=get_stbl_text(c_name_stbl, creator, count), icon=MY_CUSTOM_ICON,
                                      tag=f"C_TOGGLE::{creator}")

        elif CREATOR_VIEW_MODE == C_MODE_PACKS:
            yield ObjectPickerRow(name=get_stbl_text(STR_C_BTN_RETURN_FAVS), icon=MY_CUSTOM_ICON,
                                  tag="BTN_RETURN_FAV_CREATORS")
            packs = GLOBAL_ALL_CREATORS_CACHE.get(CURRENT_SELECTED_CREATOR, [])
            packs_sorted = sorted(packs,
                                  key=lambda x: str(getattr(x, 'display_name', getattr(x, 'sort_name', ''))).lower())
            for pck in packs_sorted:
                idx = packs.index(pck)
                pck_name = getattr(pck, 'display_name', None) or getattr(pck, 'sort_name', None) or getattr(pck,
                                                                                                            '__name__',
                                                                                                            'Unknown Pack')
                yield ObjectPickerRow(name=pck_name, row_description=getattr(pck, 'description', None),
                                      count=len(getattr(pck, 'pose_list', [])),
                                      icon=getattr(pck, 'icon', MY_CUSTOM_ICON),
                                      tag=f"CREATOR_PACK::{CURRENT_SELECTED_CREATOR}::{idx}")

        # 【新增：作者专属的移除模式】
        elif CREATOR_VIEW_MODE == C_MODE_DELETE:
            yield ObjectPickerRow(name=get_stbl_text(STR_P_BTN_RETURN), icon=MY_CUSTOM_ICON,
                                  tag="BTN_CREATORS_RETURN_FAVS")
            for creator in sorted(FAVORITE_CREATORS):
                yield ObjectPickerRow(name=get_stbl_text(STR_DYN_DELETE_ITEM, creator), icon=MY_CUSTOM_ICON,
                                      tag=f"C_DELETE::{creator}")
        return

    # --- 单独动作收藏 (完全恢复原始无删减状态) ---
    if pack_type == 'POSES':
        if not CACHE_BUILT: build_cache_safe()
        
        # 只有原版的模式切换和一键清空
        yield ObjectPickerRow(name=get_stbl_text(STR_DYN_TOGGLE_MODE_1, current_mode_str), row_description=get_stbl_text(STR_DYN_TOGGLE_MODE_1_DESC), icon=MY_CUSTOM_ICON, tag="TOGGLE_MODE_BTN")
        yield ObjectPickerRow(name=get_stbl_text(STR_S_BTN_CLEAR), row_description=get_stbl_text(STR_S_BTN_CLEAR_DESC), icon=MY_CUSTOM_ICON, tag="CLEAR_ALL_FAV_BTN")

        if not FAVORITE_POSES:
            yield ObjectPickerRow(name=get_stbl_text(STR_S_EMPTY), icon=MY_CUSTOM_ICON)
        else:
            # 100% 沿用你原本完美的按作者排序逻辑
            fav_display_list = [GLOBAL_ALL_POSES_CACHE.get(p) for p in FAVORITE_POSES if 'fgeh' not in str(p).lower() and GLOBAL_ALL_POSES_CACHE.get(p)]
            fav_display_list.sort(key=lambda x: x['pack_name'])
            
            for item in fav_display_list:
                p = item['pose']
                yield ObjectPickerRow(name=p.pose_display_name, icon=p.icon, row_description=p.pose_description, tag=p)
        
        return # 这个拦截底层的防崩防火墙必须留着

    # --- 普通包内 ---
    if RETURN_TO_FAV_ON_CLOSE and pack == GLOBAL_TRACED_PACK_REF:
        yield ObjectPickerRow(name=get_stbl_text(STR_N_RETURN_TO_POSES), icon=MY_CUSTOM_ICON, tag="RETURN_TO_FAV_BTN")

    if CAME_FROM_L1_FAVS:
        yield ObjectPickerRow(name=get_stbl_text(STR_N_RETURN_TO_PACKS), icon=MY_CUSTOM_ICON,
                              tag="RETURN_TO_FAV_PACKS_MENU_BTN")

    if CAME_FROM_CREATOR and CURRENT_SELECTED_CREATOR:
        yield ObjectPickerRow(name=get_stbl_text(STR_DYN_RETURN_CREATOR, CURRENT_SELECTED_CREATOR), icon=MY_CUSTOM_ICON,
                              tag="RETURN_TO_CREATOR_PACKS_BTN")

    yield ObjectPickerRow(name=get_stbl_text(STR_DYN_TOGGLE_MODE_2, current_mode_str), icon=MY_CUSTOM_ICON,
                          tag="TOGGLE_MODE_BTN")

    pack_id = str(getattr(pack, '__name__', 'Unknown'))
    is_pack_faved = pack_id in FAVORITE_PACKS
    names = [p.pose_name for p in getattr(pack, 'pose_list', []) if hasattr(p, 'pose_name')]
    is_all_poses_faved = bool(names) and all(n in FAVORITE_POSES for n in names)

    pack_btn_id = STR_N_REMOVE_PACK if is_pack_faved else STR_N_ADD_PACK
    pose_btn_id = STR_N_REMOVE_ALL_POSES if is_all_poses_faved else STR_N_ADD_ALL_POSES

    yield ObjectPickerRow(name=get_stbl_text(pack_btn_id), row_description=get_stbl_text(STR_N_PACK_DESC),
                          icon=MY_CUSTOM_ICON, tag="TOGGLE_FAV_PACK_ONLY_BTN")
    yield ObjectPickerRow(name=get_stbl_text(pose_btn_id), row_description=get_stbl_text(STR_N_ALL_POSES_DESC),
                          icon=MY_CUSTOM_ICON, tag="TOGGLE_FAV_ALL_POSES_ONLY_BTN")

    for pose_item in getattr(pack, 'pose_list', []):
        yield ObjectPickerRow(name=pose_item.pose_display_name, icon=pose_item.icon, tag=pose_item)


# ==========================================
# 第三部分：第二层 UI 点击处理
# ==========================================
original_pose_on_choice = poseplayer.PoseByPackNameInteraction.on_choice_selected


def custom_pose_on_choice(self, choice_tag, **kwargs):
    global CURRENT_MODE, RETURN_TO_FAV_ON_CLOSE, GLOBAL_FAV_PACK_REF, GLOBAL_TRACED_PACK_REF
    global CREATOR_VIEW_MODE, CURRENT_SELECTED_CREATOR, FAVORITE_PACKS, FAVORITE_POSES
    global CAME_FROM_CREATOR, CAME_FROM_L1_FAVS, FAV_PACKS_VIEW_MODE

    pack_type = get_pack_type(self.selected_pose_pack)

    if choice_tag is None or not isinstance(choice_tag, str):
        if hasattr(choice_tag, 'pose_name'):
            p_name = choice_tag.pose_name
            if CURRENT_MODE == MODE_FAV:
                if p_name in FAVORITE_POSES:
                    FAVORITE_POSES.remove(p_name)
                else:
                    FAVORITE_POSES.append(p_name)
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
                    CURRENT_MODE = MODE_NORMAL
                    return self._show_picker_dialog(self.sim, target_sim=self.target)
        return original_pose_on_choice(self, choice_tag, **kwargs)

    # --- 动作包：独立删除模式逻辑 ---
    if choice_tag == "BTN_FAV_PACKS_DELETE_MODE": FAV_PACKS_VIEW_MODE = P_MODE_DELETE; return self._show_picker_dialog(
        self.sim, target_sim=self.target)
    if choice_tag.startswith("P_DELETE::"):
        pck_id = choice_tag.split("::")[1]
        if pck_id in FAVORITE_PACKS:
            FAVORITE_PACKS.remove(pck_id)
            save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    # --- 包收藏夹常规逻辑 ---
    if choice_tag == "RETURN_TO_FAV_PACKS_MENU_BTN":
        self.selected_pose_pack = "fgeh_fav_packs_folder"
        FAV_PACKS_VIEW_MODE = P_MODE_FAVS
        CAME_FROM_L1_FAVS = False
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_FAV_PACKS_MANAGE": FAV_PACKS_VIEW_MODE = P_MODE_MANAGE; return self._show_picker_dialog(
        self.sim, target_sim=self.target)
    if choice_tag == "BTN_FAV_PACKS_RETURN": FAV_PACKS_VIEW_MODE = P_MODE_FAVS; return self._show_picker_dialog(
        self.sim, target_sim=self.target)
    if choice_tag == "BTN_FAV_PACKS_CLEAR": FAVORITE_PACKS.clear(); save_favorites(); return self._show_picker_dialog(
        self.sim, target_sim=self.target)

    if choice_tag.startswith("P_TOGGLE::"):
        pck_id = choice_tag.split("::")[1]
        if pck_id in FAVORITE_PACKS:
            FAVORITE_PACKS.remove(pck_id)
        else:
            FAVORITE_PACKS.append(pck_id)
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
            RETURN_TO_FAV_ON_CLOSE = False
            return self._show_picker_dialog(self.sim, target_sim=self.target)

    # --- 【新增】作者：独立删除模式逻辑 ---
    if choice_tag == "BTN_CREATORS_DELETE_MODE": CREATOR_VIEW_MODE = C_MODE_DELETE; return self._show_picker_dialog(
        self.sim, target_sim=self.target)
    if choice_tag == "BTN_CREATORS_RETURN_FAVS": CREATOR_VIEW_MODE = C_MODE_FAVS; return self._show_picker_dialog(
        self.sim, target_sim=self.target)
    if choice_tag.startswith("C_DELETE::"):
        creator = choice_tag.split("::")[1]
        if creator in FAVORITE_CREATORS:
            FAVORITE_CREATORS.remove(creator)
            save_favorites()
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    # --- 作者收藏夹常规逻辑 ---
    if choice_tag == "RETURN_TO_CREATOR_PACKS_BTN":
        self.selected_pose_pack = "hegfcreator_folder"
        CREATOR_VIEW_MODE = C_MODE_PACKS
        CAME_FROM_CREATOR = False
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "BTN_ALL_CREATORS": CREATOR_VIEW_MODE = C_MODE_ALL; return self._show_picker_dialog(self.sim,
                                                                                                         target_sim=self.target)
    if choice_tag == "BTN_RETURN_FAV_CREATORS": CREATOR_VIEW_MODE = C_MODE_FAVS; CURRENT_SELECTED_CREATOR = None; return self._show_picker_dialog(
        self.sim, target_sim=self.target)
    if choice_tag.startswith("C_VIEW::"): CREATOR_VIEW_MODE = C_MODE_PACKS; CURRENT_SELECTED_CREATOR = \
    choice_tag.split("::")[1]; return self._show_picker_dialog(self.sim, target_sim=self.target)
    if choice_tag.startswith("C_TOGGLE::"):
        creator = choice_tag.split("::")[1]
        if creator in FAVORITE_CREATORS:
            FAVORITE_CREATORS.remove(creator)
        else:
            FAVORITE_CREATORS.append(creator)
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
                RETURN_TO_FAV_ON_CLOSE = False
                return self._show_picker_dialog(self.sim, target_sim=self.target)

    # --- 单独动作与通用逻辑 ---
    if choice_tag == "TOGGLE_MODE_BTN":
        if pack_type == 'POSES':
            CURRENT_MODE = (CURRENT_MODE + 1) % 3
        else:
            CURRENT_MODE = MODE_FAV if CURRENT_MODE == MODE_NORMAL else MODE_NORMAL
        return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "RETURN_TO_FAV_BTN":
        if GLOBAL_FAV_PACK_REF:
            self.selected_pose_pack = GLOBAL_FAV_PACK_REF
            RETURN_TO_FAV_ON_CLOSE = False
            return self._show_picker_dialog(self.sim, target_sim=self.target)

    if choice_tag == "TOGGLE_FAV_PACK_ONLY_BTN":
        pack = self.selected_pose_pack
        pack_id = str(getattr(pack, '__name__', 'Unknown'))
        if pack_id in FAVORITE_PACKS:
            FAVORITE_PACKS.remove(pack_id)
        else:
            FAVORITE_PACKS.append(pack_id)
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