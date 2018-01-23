from MP3Player import MP3Player
import glob
from os.path import exists

_BASE_DIR = 'c:/temp/mp3'

def create_player(base_dir=_BASE_DIR):
    file_list = glob.glob1(base_dir, '*.mp3')
    player = MP3Player(file_list, base_dir)
    return player

def print_menu(status):
    if status :
        print('곡선택(S) | 목록변경(C) | 멈춤(U) | 다음(N) | 이전 (V) | 셔플(F) | 종료(X)')
    else:
        print('곡선택(S) | 목록변경(C) | 재생(P) | 다음(N) | 이전 (V) | 셔플(F) |  종료(X)')


def change_list():
    while True:
        new_path = input('새로운 폴더 : ')
        if exists(new_path):
            break
        print('존재하지 않는 폴더입니다. 다시 입력하세요.')

    return create_player(new_path)


def load():
    if exists('config.dat'): # 설정 파일이 있으면
        with open('config.dat', 'r') as file:
            mp3_player = MP3Player()
            mp3_player.load(file)
    else:   # 설정 파일이 없으면
        mp3_player = create_player()
    return mp3_player


def save(player):
    with open('config.dat','w') as file:
        player.save(file)


def main():
    # mp3_player = create_player()
    mp3_player = load()
    while True :
        print_menu(mp3_player.get_status())
        select = input('선택 > ').upper()
        if select == 'S':
            mp3_player.select_song()
        elif select == 'C':
            mp3_player.pause()
            mp3_player = change_list()
        elif select == 'P':
            mp3_player.play()
        elif select == 'U':
            mp3_player.pause()
        elif select == 'N':
            mp3_player.next()
        elif select == 'V':
            mp3_player.prev()
        elif select == 'F':
            mp3_player.shuffle()
        elif select == 'X':
            save(mp3_player)
            return
        else :
            print('잘못된 선택입니다.')

if __name__ == '__main__':
    main()