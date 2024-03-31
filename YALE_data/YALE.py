import tkinter as tk
import random
from tkinter import messagebox
import datetime
import subprocess


contants_list_name=[]
contants_list_weight=[]
contants_list_time=[]
config_sub=None
list_time=[]
free_time=5

contants_count=0
root = tk.Tk()
root.title("YALE")
root.state('zoomed')

label = tk.Label(root, text="スケジュールを自動生成します",font=("",20))
label.pack()

E1 = tk.Entry(root, bd=1)
E1.pack()
dt_now = datetime.datetime.now()
time_str=('{0:%H}：{0:%M}'.format(dt_now))
E1.insert(tk.END,time_str)

label = tk.Label(root, text="から",font=("",20))
label.pack()

E2 = tk.Entry(root, bd=1)
E2.pack()

sc_str="\n"

def start_clicked():
    E1_text=E1.get()
    E2_text=E2.get()
    input_flag=True
    global list_time
    try:
        try:
            list_time=[int(E1_text[0]+E1_text[1]),int(E1_text[3]+E1_text[4]),int(E2_text[0]+E2_text[1]),int(E2_text[3]+E2_text[4])]
        except:
            input_flag=False
            messagebox.showerror("入力エラー", "フォーマットどうりに入力してください")

        for integer in list_time:
            if type(integer)!=int:
                input_flag=False
                messagebox.showerror("入力エラー", "フォーマットどうりに入力してください")

    except IndexError:
        input_flag=False
        messagebox.showerror("入力エラー", "フォーマットどうりに入力してください")
    if input_flag:
        list_name_text=[]
        list_weight_number=[]
        list_time_number=[]
        list_schdule_name=[]
        list_time_schdule=[]
        free_flag=False
        end_count=0
        weight_sum=0
        with open('config.txt') as fr:
            list_saved_contants = fr.readlines()
        ir=0
        while ir<len(list_saved_contants):
            list_name_text.append(list_saved_contants[ir].rstrip())
            list_weight_number.append(int(list_saved_contants[ir+1].rstrip()))
            weight_sum+=int(list_saved_contants[ir+1].rstrip())
            list_time_number.append(int(list_saved_contants[ir+2].rstrip()))
            ir+=3
        continue_flag=True
        distance_minute=(list_time[2]-list_time[0])*60+(list_time[3]-list_time[1])
        weight_adjust=[1]*len(list_name_text)
        adjust_value=0.8
        aggregate=[0]*len(list_name_text)
        count_schedule=0
        #
        #scedule選択
        while continue_flag:
            random_contents=random.randrange(len(list_name_text))
            #print(list_name_text[random_contents])
            if free_flag:
                count_schedule+=1
                list_schdule_name.append('自由')
                distance_minute-=30
                list_time_schdule.append(30)
                if distance_minute<=0:
                    continue_flag=False
            elif list_weight_number[random_contents]==-999:
                print('thorough')
                continue
            elif list_weight_number[random_contents]>0 :
                print(list_name_text[random_contents]+':'+str(list_weight_number[random_contents]))
                if weight_adjust[random_contents]>0.3:
                    weight_adjust[random_contents]*=adjust_value
                else:
                    weight_adjust[random_contents]=1
                aggregate[random_contents]+=1
                count_schedule+=1
                list_schdule_name.append(list_name_text[random_contents])
                #print(list_name_text[random_contents])
                if distance_minute-list_time_number[random_contents]>0:
                    list_time_schdule.append(list_time_number[random_contents])
                    distance_minute-=list_time_number[random_contents]
                else:
                    list_time_schdule.append(distance_minute)
                    continue_flag=False
                list_weight_number[random_contents]-=1
            else:
                print('end'+list_name_text[random_contents])
                end_count+=1
                list_weight_number[random_contents]=-999
                if end_count==len(list_name_text):
                    free_flag=True
                # if weight_adjust[random_contents]<1.7:
                #     weight_adjust[random_contents]*=1+1-adjust_value
                # else:
                #     weight_adjust[random_contents]=1

        with open('schedule.txt','w') as f:
            i=0
            now_hour=list_time[0]
            now_minute=list_time[1]
            global sc_str
            while i<len(list_schdule_name):
                now_minute+=list_time_schdule[i]
                if now_minute>=60:
                    now_hour+=1
                    now_minute-=60
                str_schedule=str(now_hour)+':'+str(now_minute)+'まで'+list_schdule_name[i]+'\n'
                sc_str+=str_schedule
                print(str_schedule)
                f.write(str_schedule)
                i+=1
        for name,value in zip(list_name_text,aggregate):
            print(name+str(value/count_schedule)+'\n')
        text_sc.set(sc_str)
        sc_str="\n"



start_botton = tk.Button(
    root,
    text='生成開始',
    command=start_clicked)
start_botton.pack()

text_sc=tk.StringVar()
text_sc.set(" ")
label = tk.Label(root, textvariable=text_sc,font=("",10))
label.pack()

config_flag=True


def config_clicked():
    global config_flag
    if config_flag:
        config = tk.Toplevel()
        config.grab_set()
        config.focus_set()
        config_contants(config)
        global config_sub
        config_sub=config
    config_flag=False

config_botton = tk.Button(
    root,
    text='コンテンツの設定画面へ',
    command=config_clicked,
    height=5,
    width=30,
    bg="#80ff80")
config_botton.pack(side='bottom',pady=30)


def file_clicked():
    file=subprocess.run('schedule.txt',shell=True)


file_botton = tk.Button(
    root,
    text='スケージュールファイルを開く',
    command=file_clicked,
    height=3,
    width=30,
    bg="#ffdead")
file_botton.pack(side='bottom',pady=0)




#以下コンテンツ設定画面
def config_contants(window):
    def add_contants_all(name_string,weight_string,time_string):
        global contants_count
        text=tk.StringVar()
        text.set(name_string+'       ')
        name = tk.Label(contans_frame,textvariable=text,font=("",12))
        name.grid(row=contants_count,padx=5, column=0,sticky=tk.E)
        contants_list_name.append(name)
        weight = tk.Entry(contans_frame,justify=tk.CENTER, width=5)
        weight.insert(tk.END,weight_string)
        weight.grid(row=contants_count, column=1,padx=10,sticky=tk.E)
        contants_list_weight.append(weight)
        time = tk.Entry(contans_frame,justify=tk.CENTER, width=8)
        time.insert(tk.END,time_string)
        time.grid(row=contants_count, column=2,padx=10,sticky=tk.E)
        contants_list_time.append(time)
        def remove_contants():
            weight.grid_forget()
            time.grid_forget()
            remove_botton.grid_forget()
            text.set("(削除されました)")
        remove_botton = tk.Button(
        contans_frame,
        text='削除',
        command=remove_contants)
        remove_botton.grid(row=contants_count, column=3,padx=5,sticky=tk.E)
        contants_count+=1
    def add_contants():
        #global contants_list_name
        #global contants_list_weight
        get_contans_name=contans_name.get()
        if not get_contans_name:
            messagebox.showerror("入力エラー", "コンテンツ名を入力してください")
        else:
            add_contants_all(get_contans_name,'1','30')
            contans_name.delete(0, tk.END)


    header = tk.Label(window, text='コンテンツ名       出現頻度 　時間',font=("",12))
    header.pack()
    canvas = tk.Canvas(window,highlightthickness=0)

    bar = tk.Scrollbar(window, orient=tk.VERTICAL)
    bar.pack(side=tk.RIGHT, fill=tk.Y)
    bar.config(command=canvas.yview)

    canvas.config(yscrollcommand=bar.set)
    canvas.config(scrollregion=(0,0,400,500))
    canvas.pack(fill=tk.BOTH)
    contans_frame=tk.Frame(canvas)
    contans_frame.grid_columnconfigure(0, weight=1)
    contans_frame.grid_rowconfigure(0, weight=1)
    canvas.create_window((0,0), window=contans_frame, anchor=tk.NW, width=canvas.cget('width'))

    with open('config.txt') as fr:
        list_saved_contants = fr.readlines()
    ir=0
    global contants_list_name
    global contants_list_weight
    global contants_list_time
    contants_list_name=[]
    contants_list_weight=[]
    contants_list_time=[]
    while ir<len(list_saved_contants):
        add_contants_all(list_saved_contants[ir].rstrip(),list_saved_contants[ir+1].rstrip(),list_saved_contants[ir+2].rstrip())
        ir+=3
    add_frame=tk.Frame(window)
    add_frame.pack(side='bottom')
    def add_contants_enter(event):
        add_contants()
    contans_name = tk.Entry(add_frame, bd=1)
    contans_name.pack(padx=10,pady=5,side='left')
    contans_name.bind('<Return>', add_contants_enter)
    add_botton = tk.Button(
    add_frame,
    text='コンテンツを追加',
    command=add_contants)
    add_botton.pack(padx=10,pady=5,side='left')
    def end_config():
        global contants_list_name
        global contants_list_weight
        global contants_list_time
        global config_flag
        f = open('config.txt','w')
        i=0
        while i<len(contants_list_name):
            if(contants_list_name[i].cget("text")!='(削除されました)'):
                f.write(contants_list_name[i].cget("text")+'\n'+contants_list_weight[i].get()+'\n'+contants_list_time[i].get()+'\n')
            i+=1
        f.close()
        config_flag=True
        global config_sub
        config_sub.destroy()
    end_botton = tk.Button(
    add_frame,
    text='保存して終了',
    command=end_config)
    end_botton.pack(padx=10,pady=5,side='left')


root.mainloop()