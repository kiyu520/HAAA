class model_data:
    def __init__(self, api_url=None, api_key=None, model=None):
        self.__API_URL = api_url
        self.__API_KEY = api_key
        self.__model = model
    ai_prompts = (
        "你是一个命令行AI助手。回答用户问题时必须："
        "(1) 只给出确认的事实，绝不捏造信息；"
        "(2) 用简洁的语言直接回答;"
        "(3) 不使用任何格式（如Markdown、列表、代码块）；"
        "(4) 如果不知道就说“不清楚”,避免任何解释或附加内容。"
    )
    def set_API_URL(self, URL):
        self.__API_URL = URL
    def get_API_URL(self):
        return self.__API_URL
    def set_API_KEY(self, API_KEY):
        self.__API_KEY = API_KEY
    def get_API_KEY(self):
        return self.__API_KEY
    def set_model(self, model):
        self.__model = model
    def get_model(self):
        return self.__model
    def get_ALL(self):
        return self.__API_URL, self.__API_KEY, self.__model
