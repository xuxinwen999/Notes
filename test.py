# import numpy as np
def lengthOfLongestSubstring(s: str) -> int:
    dic, res, i = {}, 0, -1
    for j in range(len(s)):
        if s[j] in dic:
            i = max(dic[s[j]], i) # 更新左指针 i
        dic[s[j]] = j # 哈希表记录
        res = max(res, j - i) # 更新结果
        print(i, j, res, dic)
    return res

s = "abcabcbb"
res = lengthOfLongestSubstring(s)
# print(res)