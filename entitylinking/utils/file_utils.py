import os


def get_files(dir, postfix=None):
    """从目录dir中获取文件名后缀是postfix的所有文件，
    如果dir只是单个文件，那么就直接返回包含这个文件的list

    Returns:
        list<str> -- 文件绝对路径列表
    """
    files_ret = []
    if not os.path.isdir(dir):
        if postfix == None or dir.endswith(postfix):
            files_ret.append(dir)
        return files_ret

    iterms = os.listdir(dir)
    for iterm in iterms:
        path = os.path.join(dir, iterm)
        if os.path.isdir(path):
            files = get_files(path)
            for f in files:
                files_ret.append(f)
        else:
            if postfix == None or iterm.endswith(postfix):
                files_ret.append(path)
    return files_ret
