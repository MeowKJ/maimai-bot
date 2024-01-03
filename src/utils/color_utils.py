def get_color_code_from_score(score):
    """
    根据分数获取颜色代码。

    Args:
        score (int): 分数。

    Returns:
        tuple: 颜色代码，格式为 (R, G, B)。
    """
    score_ranges = [
        (0, 999, (0, 0, 0)),  # 白色
        (1000, 1999, (0, 221, 238)),  # 蓝色
        (2000, 3999, (0, 204, 85)),  # 绿色
        (4000, 6999, (238, 136, 17)),  # 黄色
        (7000, 9999, (238, 0, 17)),  # 红色
        (10000, 11999, (238, 0, 238)),  # 紫色
        (12000, 12999, (136, 51, 0)),  # 青铜色
        (13000, 13999, (91, 140, 170)),  # 银色
        (14000, 14499, (255, 207, 51)),  # 金色
        (14500, 14999, (255, 251, 85)),  # 白金色
    ]

    for lower, upper, color in score_ranges:
        if lower <= score <= upper:
            return color

    # 彩虹渐变效果，假定为黑色
    return 0, 0, 0


def get_img_code_from_dx_rating(dx_rating):
    """
    根据 DX 评级获取图片代码。

    Args:
        dx_rating (int): DX 评级。

    Returns:
        str: 图片代码。
    """
    ranges = [
        (0, 999, "01"),
        (1000, 1999, "02"),
        (2000, 3999, "03"),
        (4000, 6999, "04"),
        (7000, 9999, "05"),
        (10000, 11999, "06"),
        (12000, 12999, "07"),
        (13000, 13999, "08"),
        (14000, 14499, "09"),
        (14500, 14999, "09"),
    ]

    for lower, upper, code in ranges:
        if lower <= dx_rating <= upper:
            return code

    return "10"
