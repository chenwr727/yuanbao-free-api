from enum import Enum


class CHUNK_TYPE(str, Enum):
    SEARCH_GUIDE = "searchGuid"
    THINK = "think"
    TEXT = "text"
    STEP = "step"


MODEL_MAPPING = {
    "deepseek-v3": {"model": "deep_seek_v3", "support_functions": None},
    "deepseek-r1": {"model": "deep_seek", "support_functions": None},
    "deepseek-v3-search": {"model": "deep_seek_v3", "support_functions": ["supportInternetSearch"]},
    "deepseek-r1-search": {"model": "deep_seek", "support_functions": ["supportInternetSearch"]},
    "hunyuan": {"model": "hunyuan_gpt_175B_0404", "support_functions": None},
    "hunyuan-t1": {"model": "hunyuan_t1", "support_functions": None},
    "hunyuan-search": {"model": "hunyuan_gpt_175B_0404", "support_functions": ["supportInternetSearch"]},
    "hunyuan-t1-search": {"model": "hunyuan_t1", "support_functions": ["supportInternetSearch"]},
}
