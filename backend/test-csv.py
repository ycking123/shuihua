import pandas as pd

# 将 '您的文件名.xlsx' 替换为您的实际文件名
input_file = 'xiangjianduanlu.xlsx'
output_file = 'xiangjianduanlu.csv'

# 读取 Excel 文件
df = pd.read_excel(input_file)

# 保存为 CSV
# encoding='utf-8-sig' 可以防止在 Excel 中打开时出现中文乱码
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print("转换完成！")