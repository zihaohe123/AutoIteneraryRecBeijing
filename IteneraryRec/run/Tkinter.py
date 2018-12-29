from tkinter import *
from utils.onelinerecommendation import *
import webbrowser

start_description = ''
end_description = ''
duration = 0

def get_query():
    # print(entry_start.get(), entry_dst.get(), entry_duration.get())
    # print(var_nature.get(),var_culture.get(),var_museum.get(), var_shopping.get())

    visited_locations = entry_hist.get()
    if visited_locations == '无':
        visited_locs = []
    else:
        visited_locs = visited_locations.split(',')
    online_recommendation = OnlineRecommendation(start_point_description=entry_start.get(),
                                                 end_point_description=entry_dst.get(),
                                                 duration=int(entry_duration.get()),
                                                 mode=var_mode.get(),
                                                 nature = var_nature.get(),
                                                 culture=var_culture.get(),
                                                 museum=var_museum.get(),
                                                 shopping=var_shopping.get(),
                                                 visited_location_names=visited_locs,
                                                 current_season='autumn',
                                                 a1=float(entry_a1.get()),a2=float(entry_a2.get()),
                                                 a3=float(entry_a3.get()),a4=float(entry_a4.get())
                                                 )
    online_recommendation.query_verify()
    online_recommendation.query_preprossessing()
    online_recommendation.generate_trips()
    online_recommendation.trip_candidates_ranking()
    online_recommendation.trip_candidates_reranking()

    result.configure(text=online_recommendation.display())

    webbrowser.open(r'D:\Recommendation\ItineraryRec\run\itinerary.html')





master = Tk()
w,h = master.maxsize()
master.geometry("{}x{}".format(w, h))
master.title('基于城市GPS数据的用户行程推荐')


Label(master, text='行程基本信息',font=('微软雅黑', 14)).grid(row=0)
Label(master, text='起点：',font=('微软雅黑', 14)).grid(row=1,column=0)
Label(master, text='终点：',font=('微软雅黑', 14)).grid(row=2,column=0)
Label(master, text='时长：',font=('微软雅黑', 14)).grid(row=3,column=0)
entry_start = Entry(master,font=('微软雅黑', 14))
entry_start.grid(row=1, column=1,columnspan=5)
entry_dst = Entry(master,font=('微软雅黑', 14))
entry_dst.grid(row=2, column=1,columnspan=5)
entry_duration = Entry(master,font=('微软雅黑', 14))
entry_duration.grid(row=3, column=1,columnspan=5)

Label(master).grid(row=4, column=0)
Label(master,text='交通工具偏好',font=('微软雅黑', 14)).grid(row=5, column=0)
var_mode = StringVar()
var_mode.set('driving')
Radiobutton(master, variable=var_mode, text='驾车', value='driving',font=('微软雅黑', 14)).grid(row=6, column=0)
Radiobutton(master, variable=var_mode, text='公交', value='transit',font=('微软雅黑', 14)).grid(row=7, column=0)
Radiobutton(master, variable=var_mode, text='骑行', value='riding',font=('微软雅黑', 14)).grid(row=8, column=0)
Radiobutton(master, variable=var_mode, text='步行', value='walking',font=('微软雅黑', 14)).grid(row=9, column=0)


Label(master, text='兴趣点类型偏好',font=('微软雅黑', 14)).grid(row=5, column=1)
var_nature = BooleanVar()
var_nature.set(True)
Checkbutton(master, text='自然风景', variable = var_nature, onvalue = True, offvalue = False,font=('微软雅黑', 14)).grid(row=6, column=1,sticky=W)
var_culture = BooleanVar()
var_culture.set(True)
Checkbutton(master, text='名胜古迹', variable = var_culture, onvalue = True, offvalue =False,font=('微软雅黑', 14)).grid(row=7, column=1,sticky=W)
var_museum = BooleanVar()
var_museum.set(True)
Checkbutton(master, text='展馆', variable = var_museum, onvalue = True, offvalue = False,font=('微软雅黑', 14)).grid(row=8, column=1,sticky=W)
var_shopping = BooleanVar()
var_shopping.set(True)
Checkbutton(master, text='购物中心', variable = var_shopping, onvalue = True, offvalue = False,font=('微软雅黑', 14)).grid(row=9, column=1,sticky=W)
#
Label(master).grid(row=10, column=0)
Label(master, text='游玩过的景点（多个景点请以逗号分隔）：',font=('微软雅黑', 14)).grid(row=17,column=0,columnspan=4)
entry_hist = Entry(master,font=('微软雅黑', 14))
entry_hist.grid(row=17,column=4,columnspan=8,sticky=W)
entry_hist.insert(0,'无')


Label(master).grid(row=19, column=0)
Label(master, text='权值偏好',font=('微软雅黑', 14)).grid(row=20,column=0,columnspan=4,sticky=W)
Label(master, text='行程时间比：',font=('微软雅黑', 14)).grid(row=21,column=0,columnspan=4)
Label(master, text='停留时间比：',font=('微软雅黑', 14)).grid(row=22,column=0,columnspan=4)
Label(master, text='兴趣度密度比：',font=('微软雅黑', 14)).grid(row=23,column=0,columnspan=4)
Label(master, text='经典序列得分比：',font=('微软雅黑', 14)).grid(row=24,column=0,columnspan=4)

entry_a1 = Entry(master,font=('微软雅黑', 14))
entry_a2 = Entry(master,font=('微软雅黑', 14))
entry_a3 = Entry(master,font=('微软雅黑', 14))
entry_a4 = Entry(master,font=('微软雅黑', 14))
entry_a1.insert(0,1)
entry_a2.insert(0,1)
entry_a3.insert(0,1)
entry_a4.insert(0,1)
entry_a1.grid(row=21,column=4)
entry_a2.grid(row=22,column=4)
entry_a3.grid(row=23,column=4)
entry_a4.grid(row=24,column=4)


Label(master).grid(row=25, column=0)
Button(master, text='确定', command=get_query,font=('微软雅黑', 14)).grid(row=26, column=0, sticky=W, pady=4)
Button(master, text='退出', command=master.quit,font=('微软雅黑', 14)).grid(row=26, column=1, sticky=W, pady=4)


result = Label(master,font=('微软雅黑', 14))
result.grid(row=0, column=40, rowspan=40, columnspan=40, sticky=W)


mainloop()

