import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

# 正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family'] = 'sans-serif'

# 1、读取数据
data = pd.read_csv('aqi.csv', encoding='utf-8')

# 绘制 aqi 和 pm2.5 的关系散点图
# 设置图像尺寸
plt.figure(figsize=(15, 10))
# 绘制散点图，横坐标为aqi数据的第二列，纵坐标为aqi数据的第四列
plt.scatter(data[data.columns[1]], data[data.columns[3]])
# 设置横轴标签为'AQI'，字体大小为20
plt.xlabel('AQI', fontsize=20)
# 设置纵轴标签为'PM2.5'，字体大小为20
plt.ylabel('PM2.5', fontsize=20)
# 设置图像标题为'芜湖市AQI和PM2.5的关系散点图'，字体大小为25
plt.title('芜湖市AQI和PM2.5的关系散点图', fontsize=25)
plt.show()

# 绘制空气质量等级分类散点图
# 设定画布大小
plt.figure(figsize=(15, 10))
# 绘制散点图，x轴：AQI数据，y轴：空气等级数据
sn.stripplot(x=data[data.columns[2]], y=data[data.columns[1]], data=data, jitter=True)
# 设定x轴标签和字体大小
plt.xlabel('AQI', fontsize=20)
# 设定y轴标签和字体大小
plt.ylabel('空气等级', fontsize=20)
# 设定标题和字体大小
plt.title('芜湖市空气质量等级分类散点图', fontsize=25)
plt.show()

# 绘制空气质量等级单变量分布图
# 绘制以第三列为 x 轴，数据来源为 aqi 的计数图
sn.countplot(x=data.columns[2], data=data)
# 设置标题为“空气质量等级单变量分布图”
plt.title("空气质量等级单变量分布图")
# 设置 x 轴标签为“质量等级”
plt.xlabel("质量等级")
# 设置 y 轴标签为“频数”
plt.ylabel("频数")
plt.show()

# 绘制PM2.5与AQI的线性回归拟合图
# 调用seaborn库的regplot函数，将PM2.5含量（ppm）作为x轴，AQI作为y轴，数据源为aqi
sn.regplot(x='PM2.5含量（ppm）', y='AQI', data=data)
# 设定图表标题为  'PM2.5与AQI的线性回归拟合图'
plt.title('PM2.5与AQI的线性回归拟合图')
# 设定图表x轴标签为'PM2.5含量（ppm）'
plt.xlabel('PM2.5含量（ppm）')
# 设定图表y轴标签为'AQI'
plt.ylabel('AQI')
plt.show()

# 计算相关系数
# 计算相关系数并赋值给变量 corr
corr = data[
    ['AQI', 'PM2.5含量（ppm）', 'PM10含量（ppm）', 'SO2含量（ppm）', 'CO含量（ppm）', 'NO2含量（ppm）', 'O3_8h含量（ppm）']].corr()
print("AQI与其他因素的相关系数如下：\n", corr)

# 绘制特征相关性热力图
# 设置画布大小
plt.figure(figsize=(17, 14))
# 计算相关系数并赋值给变量 corr
corr = data[
    ['AQI', 'PM2.5含量（ppm）', 'PM10含量（ppm）', 'SO2含量（ppm）', 'CO含量（ppm）', 'NO2含量（ppm）', 'O3_8h含量（ppm）']].corr()
# 以热图的形式展示相关性，并用蓝红色调表示，同时在每个方格中显示数值，并设置线宽为1
sn.heatmap(corr, cmap='RdBu_r', annot=True, linewidths=1)
# 设置热图的标题，并设置字体大小为25
plt.title("各污染物之间的特征相关性热力分布图", fontsize=25)
# 设置x轴标签字体大小为15
plt.xticks(fontsize=15)
# 设置y轴标签字体大小为15
plt.yticks(fontsize=15)
plt.show()