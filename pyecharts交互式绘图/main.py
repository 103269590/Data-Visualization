import pandas as pd
import numpy as np
from pyecharts.charts import Bar, Pie, Line, Timeline, Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import warnings


# 一个类方法，按照大类（非饮料和饮料）和各类（A、B、C、D、E）来对大类重新进行一个命名，可以更加直观看出数据属于哪类
# 以字典形式处理
def dl_gl(dl):
    mapping = {
        ('非饮料', 'A'): 'A非饮料',
        ('非饮料', 'B'): 'B非饮料',
        ('非饮料', 'C'): 'C非饮料',
        ('非饮料', 'D'): 'D非饮料',
        ('非饮料', 'E'): 'E非饮料',
        ('饮料', 'A'): 'A饮料',
        ('饮料', 'B'): 'B饮料',
        ('饮料', 'C'): 'C饮料',
        ('饮料', 'D'): 'D饮料',
    }
    return mapping.get((dl['大类'], dl['地点']), 'E饮料')


data = pd.read_csv('./处理后的数据.csv', encoding='gbk')

# 设置系统配置项和全局配置项，绘制销量前5的商品销量柱形图
data1 = data.groupby('商品').count()  # 按商品分组，统计商品的出现频次,即为商品的销量
data2 = data1.sort_values('订单号', ascending=False).head()['订单号']  # 获取销量前五的数据
columns = {'订单号': '销量'}  # 对列进行重新命名
data2 = pd.DataFrame(data2)  # 将其转换成一个DataFrame类型
data2 = data2.rename(columns=columns)  # 对列索引进行重新命名
data3 = data2.T  # 将获取已经处理好的数据进行一个转置
init_opts = opts.InitOpts(width='1000px', height='800px')
bar = (
    Bar(init_opts)
    .add_xaxis(data3.columns.tolist())
    .add_yaxis('销量', data3.loc['销量'].tolist(),
               label_opts=opts.LabelOpts(position='insideTop'))
    .set_global_opts(title_opts=opts.TitleOpts(
        title='销量前5的商品销量柱形图'))
)
bar.render('销量前5的商品销量柱形图.html')
bar.render_notebook()

# 设置系统配置项和全局配置项，绘制售货机每月总交易额折线图
data['支付时间'] = pd.to_datetime(data['支付时间'])  # 将支付时间转换成datetime类型，便于分析
data['月份'] = data['支付时间'].dt.month  # 从数据中提取出销售月份具体是哪月，并将其添加到data当中去
temp = data.groupby(by=['月份', '地点'], as_index=False)['实际金额'].sum()
x = sorted(list(set(data['月份'].values.tolist())))
x_data = [str(i) + '月' for i in x]
location = list(set(temp['地点'].values.tolist()))
location = sorted(location)
y = []
for i in location:
    y.append(np.round(temp[temp['地点'] == i]['实际金额'].values.tolist(), 2))
line = (Line()
        .add_xaxis(x_data)
        .add_yaxis('售货机A', y[0], label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('售货机B', y[1], label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('售货机C', y[2], label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('售货机D', y[3], label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('售货机E', y[4], label_opts=opts.LabelOpts(is_show=False))
        )
line.render('售货机每月总交易额折线图.html')
line.render_notebook()

warnings.filterwarnings('ignore')
category_sales = data.groupby(['地点', '大类'])['实际金额'].sum().reset_index()

# 调用方法
category_sales['大类'] = category_sales.apply(dl_gl, axis=1)

temp = data.groupby('大类')['实际金额'].sum()  # 进行分组统计
temp = pd.DataFrame(temp)
temp = temp.T  # 将获取的数据进行一个转置，便于计算
pie = (
    Pie()
    .add('', [list(z) for z in zip(temp.columns.tolist(), temp.loc['实际金额'].values.tolist())])
    .set_global_opts(title_opts=opts.TitleOpts(title='售货机各类（按大类）商品的销售额饼图'))
    .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{c} ({d}%)'))
)
pie.render('售货机各类（按大类）商品的销售额饼图.html')
pie.render_notebook()

# 按售货机和月份分组，计算每台售货机每月的总交易额
data_monthly = data.groupby(['地点', '月份'])['实际金额'].sum().reset_index()

# 创建时间线轮播多图
timeline = Timeline()

# 添加每个月的图表
for month in data_monthly['月份'].unique().tolist():
    bar = (
        Bar()
        .add_xaxis(data_monthly[data_monthly['月份'] == month]['地点'].tolist())
        .add_yaxis("销售额", data_monthly[data_monthly['月份'] == month]['实际金额'].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="2017年{}月每台售货机销售额".format(month)))
    )
    timeline.add(bar, "{}月".format(month))
timeline.render('2017年每月每台售货机的销售额的时间线轮播多图.html')
timeline.render_notebook()

colors1 = ["#00FF80", "#800000"]
colors2 = ["#000080", "#008000 "]
colors3 = ["red", "yellow"]
colors4 = ["#FF0080", "#80FF00"]
colors5 = ["#FF0000", "#00FF00#800000"]
# 获取每台售货机各类（按大类）商品的销售额数据
category_amount = data.groupby(['地点', '大类'])['实际金额'].sum().reset_index()

pie1 = (
    Pie(init_opts=opts.InitOpts(width='50px', height='40px', theme=ThemeType.LIGHT))
    .add("", [list(z) for z in zip(category_amount[category_amount['地点'] == 'A'].大类.tolist(),
                                   category_amount[category_amount['地点'] == 'A']['实际金额'].tolist())],
         radius=["30%", "50%"], center=["15%", "50%"], rosetype="radius")
    .set_colors(colors1)
    .set_global_opts(title_opts=opts.TitleOpts(title="商品的销售额饼图的并行多图"))
)
pie2 = (
    Pie(init_opts=opts.InitOpts(width='50px', height='40px', theme=ThemeType.VINTAGE))
    .add("", [list(z) for z in zip(category_amount[category_amount['地点'] == 'B'].大类.tolist(),
                                   category_amount[category_amount['地点'] == 'B']['实际金额'].tolist())],
         radius=["30%", "50%"], center=["30%", "50%"], rosetype="radius").set_colors(colors1)
    .set_colors(colors2)
)

# 绘制饼图
pie3 = (
    Pie(init_opts=opts.InitOpts(width='50px', height='40px', theme=ThemeType.WONDERLAND))
    .add("", [list(z) for z in zip(category_amount[category_amount['地点'] == 'C'].大类.tolist(),
                                   category_amount[category_amount['地点'] == 'C']['实际金额'].tolist())],
         radius=["30%", "50%"], center=["50%", "50%"], rosetype="radius")
    .set_colors(colors3)
)
pie4 = (
    Pie(init_opts=opts.InitOpts(width='50px', height='40px', theme=ThemeType.ROMA))
    .add("", [list(z) for z in zip(category_amount[category_amount['地点'] == 'D'].大类.tolist(),
                                   category_amount[category_amount['地点'] == 'D']['实际金额'].tolist())],
         radius=["30%", "50%"], center=["65%", "50%"], rosetype="radius")
    .set_colors(colors4)
)
pie5 = (
    Pie(init_opts=opts.InitOpts(width='50px', height='40px', theme=ThemeType.WESTEROS))
    .add("", [list(z) for z in zip(category_amount[category_amount['地点'] == 'E'].大类.tolist(),
                                   category_amount[category_amount['地点'] == 'E']['实际金额'].tolist())],
         radius=["30%", "50%"], center=["85%", "50%"], rosetype="radius")
    .set_colors(colors5)
)

grid = (
    Grid()
    .add(pie1, grid_opts=opts.GridOpts(pos_left="30%", pos_top="30%"))
    .add(pie2, grid_opts=opts.GridOpts(pos_left="60%", pos_right="30%"))
    .add(pie3, grid_opts=opts.GridOpts(pos_left="50%", pos_right="5%"))
    .add(pie4, grid_opts=opts.GridOpts(pos_left="70%", pos_right="5%"))
    .add(pie5, grid_opts=opts.GridOpts(pos_left="90%", pos_right="5%"))
)
grid.render('售货机每月各类（按大类）商品的销售额饼图的并行多图.html')
grid.render_notebook()  # 从左到右分别是A，B，C，D，E
