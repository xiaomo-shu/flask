# 此文件中定义我们自己封装一些代码


def do_rank_class(index):
    """获取点击排行新闻对应class"""
    if index < 0 or index >= 3:
        return ''

    rank_class_li = ['first', 'second', 'third']

    return rank_class_li[index]

