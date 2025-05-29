class AIBase:
    def __init__(self, entity, sprite):
        self.entity = entity         # 角色/怪物的数据实体
        self.sprite = sprite         # 表现层的控制接口
        self.blackboard = {}         # 存储共享状态（如控制状态、目标等）

    def update(self):
        raise NotImplementedError("AIBase is abstract.")
