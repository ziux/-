import pyperclip
import datetime
import os
import sys

md_path = r"C:\Users\yangyu\Documents\docs\-\learn"


def main():
    save = False
    this_month = datetime.date.today().strftime('%y%m')
    tmp_value = pyperclip.paste()
    print(tmp_value)
    if not tmp_value:
        return
    remark = ''
    args = sys.argv[1:]
    if args:
        if args[0] == 'save':
            save = True
            if len(args) > 1:
                remark = args[1]
        else:
            remark = args[0]

    with open(os.path.join(md_path, f'{this_month}.txt'), 'a+', encoding='utf-8') as f:
        f.write(f'--------{remark}-------\n')
        f.write(tmp_value)
        f.write('\n')

    if save:
        os.chdir(md_path)
        os.system(f'git add {this_month}.txt')
        os.system('git commit -a -m "learn save"')
        os.system('git push')


main()
