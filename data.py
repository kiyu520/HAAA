class model_data:
    def _init_(self,api_url=None,api_key=None,model=None):
        __API_URL,__API_KEY,model=api_url,api_key,model
    ai_prompts="""你是一个命令行AI助手。回答用户问题时必须：(1) 只给出确认的事实，绝不捏造信息；(2) 用最简洁的语言直接回答，通常不超过1-2句;(3) 不
    使用任何格式（如Markdown、列表、代码块）；(4) 如果不知道就说“不清楚”,避免任何解释或附加内容。"""
    #__API_URL,__API_KEY,__model=None,None,None
    def set_API_URL(URL):
        __API_URL=URL
    def get_API_URL():
        return __API_URL
    def set_API_KEY(API_KEY):
        __API_KEY=API_KEY
    def get_API_KEY():
        return __API_KEY
    def set_model(model):
        __model=model
    def get_model():
        return __model
    def get_ALL():
        return __API_URL,__API_KEY,__model


