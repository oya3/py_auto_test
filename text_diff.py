import difflib

str_1 = '''\
1行目       
2行目       
3行目       
'''

str_2 = '''\
先頭行追加
1行目       
2行目       (変更)
'''

df = difflib.HtmlDiff()
res = df.make_file(str_1.splitlines(), str_2.splitlines(),)
with open('html_diff.html', 'w', encoding='utf-8') as f:
    f.write(res)
