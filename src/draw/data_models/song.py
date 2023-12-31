class SongData:
    def __init__(self, **kwargs):
        self.achievements = kwargs.get("achievements", 0)
        self.ds = kwargs.get("ds", 0)
        self.dx_score = kwargs.get("dx_score", 0)
        self.fc = kwargs.get("fc", "")
        self.fs = kwargs.get("fs", "")

        self.level = kwargs.get("level", "")
        self.level_index = kwargs.get("level_index", 0)
        self.rating = kwargs.get("rating", 0)
        self.rating_icon = kwargs.get("rating_icon", "")
        self.song_id = kwargs.get("id", 0)
        self.title = kwargs.get("title", "")
        self.type = kwargs.get("type", "")

    @classmethod
    def from_data_luoxue(cls, data1):
        id_value = data1.get("id", 0)

        # 处理 id 大于 1000 的情况
        if id_value > 1000:
            id_value += 10000

        return cls(
            achievements=data1["achievements"],
            ds=data1.get("level", 0),
            dx_score=data1.get("dx_score", 0),
            fc=data1.get("fc", ""),
            fs=data1.get("fs", ""),
            level=data1.get("level", ""),
            level_index=data1.get("level_index", 0),
            rating=int(data1.get("dx_rating", 0)),
            rating_icon=data1.get("rate", ""),
            id=id_value,  # 更新 id 的值
            title=data1.get("song_name", ""),
            type="sd" if data1.get("type") == "standard" else "dx",
        )

    @classmethod
    def from_data_divingfish(cls, data2):
        return cls(
            achievements=data2["achievements"],
            ds=data2.get("ds", 0),
            dx_score=data2.get("dxScore", 0),
            fc=data2.get("fc", ""),
            fs=data2.get("fs", ""),
            level=data2.get("level", ""),
            level_index=data2.get("level_index", 0),
            rating=data2.get("ra", 0),
            rating_icon=data2.get("rate", ""),
            id=data2.get("song_id", 0),
            song_name=data2.get("title", ""),
            type=data2.get("type"),
        )
