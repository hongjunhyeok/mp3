from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from random import shuffle
import glob
from pygame import mixer
from tinytag import *
from threading import Thread
import time
_BASE_DIR = 'c:/temp/mp3'
class MP3Frame(Frame) :
    def __init__(self,master,base_dir=_BASE_DIR):
        Frame.__init__(self,master)

        self.base_dir = base_dir
        self.master = master
        self.master.title("MP3Player")
        self.pack(fill=BOTH, expand=True)
        self.make_info_frame()
        self.make_button_frame()


        # 디렉토리에서 목록읽기
        # 폴더 바꿨을때와 시작할 시 호출
        self.load_list()# 현재 지정된 폴더에서 파일을 읽어서 리스트에 채우는 역할

        self.current= 0
        self.position= 0
        self.status=False
        mixer.init()

    def make_info_frame(self):
        frameInfo = Frame(self)
        frameInfo.pack(fill=X)

        # 디렉토리 상태 표시 라벨
        Label(frameInfo, text = "현재 폴더 : ").pack(side=LEFT, padx=5, pady=5)
        self.lb1BaseDir = Label(frameInfo, text =self.base_dir)
        self.lb1BaseDir.pack(side=LEFT, padx=5, pady=5, fill=X)

        frameInfo = Frame(self)
        frameInfo.pack(fill=X)  # 크기는 x축으로 고정

        # 현재곡 상태 표시 라벨
        Label(frameInfo, text = "현재곡 : ").pack(side=LEFT, padx=5, pady=5)
        self.lb1SongTitle = Label(frameInfo,text='---')
        self.lb1SongTitle.pack(side = LEFT , padx=5, pady=5 , fill= X)#크기는 x축으로 고정

        frameInfo=Frame(self)
        frameInfo.pack(fill=BOTH)

        # 리스트 박스 / 윈도우 크기 확장시 확장.
        self.listbox = Listbox(self, height=5)
        self.listbox.pack(fill=BOTH, expand=True)
        self.listbox.bind(self)

        frameInfo = Frame(self)
        frameInfo.pack(fill=BOTH)


        #스케일
        Label(frameInfo,text ='---').pack(side=LEFT, padx=5,pady=5)
        frameInfo = Frame(self)
        frameInfo.pack(fill=BOTH)
        self.length =Label(frameInfo,text='---', anchor=CENTER)
        self.length.pack(fill=X)
        self.scale=Scale(frameInfo, from_=0, to =100, orient=HORIZONTAL)
        self.scale.pack(fill=X)
    def update_progress(self):
        try:
            while self.run:
                if self.status:
                    self.position=mixer.music.get_pos()
                    self.progress.set(self.position)
                time.sleep(0.1)
        except Exception as err:
            print('{0}'.format(err))




        # 버튼이 여러개이므로 프레임이 필요함. 버튼은 라벨을 기본적으로 상속받는다.
        # button frame으로 버튼을 메소드화
    def get_position(self):
        pass


    # def setpos(self):
    #     self.oldpos=self.newpos
    #     self.newpos=self.scale.get()
    #     if self.newpos - self.oldpos != 1:
    #         self.changed = True


    def make_button_frame(self):
        self.frameButtons=Frame(self)
        self.frameButtons.pack(fill=X)
        # 포토이미지를 지역변수로 보내게되면 버튼이 제대로 인식을 못해 그래서 참조변수를 이용
        # 이미지가 변경되어야 하므로 참조변수화 시켰음.
        self.play_img=PhotoImage(file='play.png')
        self.pause_img=PhotoImage(file='pause.png')
        # 참조를 증가시키기위해 사용 // 지역변수로 사용하면 잘안돼..
        self.prev_img = PhotoImage(file='previous.png')
        self.next_img=PhotoImage(file='next.png')
        self.shuffle_img=PhotoImage(file='shuffle.png')
        self.folder_img=PhotoImage(file='folder.png')

        ## command 버튼이 눌러졌을때 호출할 함수.
        ## 이벤트에  의해 호출되는 메소드는 on을 붙여준다.
        self.btnSelect=Button(self.frameButtons, image=self.folder_img,
                              command=lambda :self.on_change_dir())
        self.btnSelect.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.btnPrev = Button(self.frameButtons, image = self.prev_img,
                              command = lambda: self.on_prev())
        self.btnPrev.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.btnPlay = Button(self.frameButtons, image=self.play_img,
                              command=lambda: self.on_play())
        self.btnPlay.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.btnNext = Button(self.frameButtons, image=self.next_img,
                              command=lambda: self.on_next())
        self.btnNext.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        self.btnShuffle = Button(self.frameButtons, image=self.shuffle_img,
                              command=lambda: self.on_shuffle())
        self.btnShuffle.pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

        # 리스트 박스 구성
        # selec_set 은 클릭하면 파란줄 생기게 해주는거.
    def load_list(self):
        self.lb1BaseDir.config(text=self.base_dir)

        #attribute로 가지고있었으나 지금은 지역변수로 운영하고있다.  왜?? list가 이미 관리중
        # list와 file_list 두개를 관리하면 피곤하니 여기서 관리하도록 함.
        file_list = glob.glob1(self.base_dir,'*.mp3')
        #clear
        print(file_list)
        self.listbox.delete(0,END)
        for file in file_list:
            self.listbox.insert(END,file)

        self.current = 0

        self.listbox.select_set(self.current)
        title=self.listbox.get(self.current)
    def on_change_dir(self):
        dir = filedialog.askdirectory() # 시스템 대화상자 호출 운영체제가 제공.

        # dir이 아무것도 리턴이 안되는경우 // 대화상자에서 취소를 누른경우를 대비해서 만듦.
        if dir:
            self.base_dir=dir
            self.load_list()

    def on_prev(self):
        self.listbox.select_clear(self.current)
        if self.current == 0:
            self.current = self.listbox.size() -1
        else:
            self.current -=1
        self.listbox.select_set(self.current)

        self.play()
        ## status 검사해서 True 면 재생중이므로 일시정지로
        ## config라벨은 play에서 담당하므로 오직 버튼 이벤트에만 집중하도록한다.
    def on_play(self):
        if self.status :#재생이면 중지로
            self.btnPlay.config(image=self.pause_img)
            self.status =False
            self.position = mixer.music.get_pos()
            mixer.music.pause()

        else : # 중지면 재생으로
            self.btnPlay.config(image=self.play_img)
            self.status = True
            if self.position :
                mixer.music.unpause()
            else:
                self.play()
        # 인덱스조정후 플레이 시킴
        # 리스트 항목 선택을 바꿈 > 해제후 선택
    def on_next(self):
        self.listbox.select_clear(self.current) # 선택 해제

        self.current=(self.current+1)%self.listbox.size()
        self.listbox.select_set(self.current)  # 새로운 선택 설정
        self.status=True
        self.play()
        # if self.status :#재생이면 중지로
        #     self.btnPlay.config(image=self.pause_img)
        #
        #     self.position = mixer.music.get_pos()
        #     mixer.music.pause()
        #
        #     if self.position:
        #         mixer.music.unpause()
        #     else:
        #
        #          self.play()



        #목록을 가져온뒤 목록 shuffle
    def show_value(self,method):
        print(method.get())

    def on_shuffle(self):
        mp3_list = list(self.listbox.get(0,END))# x텍스트를 얻는다.
        shuffle(mp3_list)
        title = self.lb1SongTitle.cget('text')


        #delete prev list
        self.listbox.delete(0,END)


        # 새로운 목록 넣기
        for file in mp3_list:
            self.listbox.insert(END,file)
        self.currnet=mp3_list.index(title)
        self.listbox.select_set(self.current)

    def on_select(self,event):
        current=self.listbox.curselection() # 튜플로 리턴
        if current:# current 확인인
            self.current=current[0]
            self.play()

    ## 여러군데서 쓰이는 메소드
    def play(self):
        self.position=0
        mp3=self.base_dir+'/'+self.listbox.get(self.current)
        mixer.music.load(mp3)
        mixer.music.play()

        self.status = True
        try:
            tag =TinyTag.get(mp3)
            print('this track is by %s.'% tag.artist)

            print('It is %f seconds long.'% tag.duration)
        except Exception as err:
            print('%s'%err)

        def get_duration():
            return tag.duration
        def get_artist():
            return tag.artist


       # 일시정지상태에서 이전 다음곡 누를경우 자동 재생시키기위해선 , 주석처리된 코드를 사용한다.
        self.btnPlay.config(image=self.play_img)
        self.status = True
      #  w재생정보 갱신
        title = self.listbox.get(self.current)
        self.lb1SongTitle.config(text=title)
        try:
            duration=tag.duration
            self.length.config(text=int(duration))
        except Exception as err:
            print('태그가 없습니다.')




class MP3Player(Thread):
    def __init__(self, value = 0, displacement=None, interval=0.1,on_change=None):
        Thread.__init__(self)
        self.value=value
        self.interval=interval
        self.on_change=on_change

    def measure(self):
        return self.value

    def run(self):
        try:
            for self.value in self.sensor:
                time.sleep(self.interval)
                if self.on_change:
                    self.on_change(self.value)
        except:
            print('센서 스레드가 종료합니다.')
def main():
    root = Tk()
    root.geometry('500x200+100+100')
    MP3Frame(root)
    root.mainloop()

if __name__=='__main__':
    main()
