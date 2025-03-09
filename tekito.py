import streamlit as st
import streamlit_calendar as st_calendar
from datetime import datetime, timedelta

st.set_page_config(layout='wide')

st.title("ゴミ出し予定アプリ")

# 今日の日付を取得
今日 = datetime.now()

# 今日の日付を表示
st.write("今日の日付は:", 今日.strftime('%Y年%m月%d日'))

曜日の日付 = []
for i in range(100):  # 今後100週間分の月曜日、火曜日、木曜日を取得
    月曜日 = 今日 + timedelta(days=(0 - 今日.weekday() + 7) % 7 + 7 * i)  # 月曜日
    火曜日 = 今日 + timedelta(days=(1 - 今日.weekday() + 7) % 7 + 7 * i)  # 火曜日
    木曜日 = 今日 + timedelta(days=(3 - 今日.weekday() + 7) % 7 + 7 * i)  # 木曜日
    曜日の日付.append(月曜日)
    曜日の日付.append(火曜日)  # 火曜日を追加
    曜日の日付.append(木曜日)

# イベントを定義
event_list = []
for i, 日付 in enumerate(曜日の日付):
    if 日付.weekday() == 0:  # 月曜日
        event = {
            'id': str(i + 1),  # IDをユニークにする
            'title': '可燃ごみ',  # 月曜日のイベント名
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),  # 開始日時
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),  # 終了日時
            'editable': False,  # 編集不可能にする
        }
    elif 日付.weekday() == 1:  # 火曜日
        event = {
            'id': str(i + 1),  # IDをユニークにする
            'title': '資源・電池類',  # 火曜日のイベント名
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),  # 開始日時
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),  # 終了日時
            'editable': False,  # 編集不可能にする
        }
        # 火曜日に追加するイベントをリストに追加
        event_list.append({
            'id': str(i + 1) + "_2",  # IDをユニークにするために変更
            'title': '紙製容器包装・雑がみ・ペットボトル・空き缶・空きびん',  # 新しいイベント名
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),  # 開始日時
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),  # 終了日時
            'editable': False,  # 編集不可能にする
        })
    elif 日付.weekday() == 3:  # 木曜日
        event = {
            'id': str(i + 1),  # IDをユニークにする
            'title': '可燃ごみ',  # 木曜日のイベント名
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),  # 開始日時
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),  # 終了日時
            'editable': False,  # 編集不可能にする
        }
    event_list.append(event)

# 今日の予定を表示
今日の予定 = [event for event in event_list if event['start'].startswith(今日.strftime('%Y-%m-%d'))]

if 今日の予定:
    st.header("今日の予定")  # 中くらいの見出しを表示
    for event in 今日の予定:
        with st.expander(event['title'], expanded=False):  # タッチしたときに展開する
            st.write(f"開始: {event['start']}")
            st.write(f"終了: {event['end']}")
else:
    st.write("今日のゴミ出し予定はありません。")  # 予定がない場合のメッセージ


# オプションを指定
options = {
    'initialView': 'dayGridMonth',
    # left/center/rightの3つの領域に表示するものはこの例の順番でなくてもいい
    'headerToolbar': {
        # ヘッダーの左側に表示するものを指定
        # 日付を移動するボタンが表示される。'today'を省略してもいい
        'left': 'today prev,next',
        # ヘッダーの中央に表示するものを指定
        # 'title'は表示されている日付などのこと
        'center': 'title',
        # ヘッダーの右側に表示するものを指定
        # ビュー名をカンマ区切りで列挙して指定するとビューを切り替えるためのボタンが表示される
        'right': 'dayGridMonth,timeGridWeek,listWeek',
    },
    'footerToolbar': {
        # ヘッダーと同じものをフッターにも配置できる。配置しない場合は省力する
        # 'center': 'title',
    },
    'titleFormat': {
        # 例えば月の表記を数字を指定できる
        # 年/月/日の順番にするのはlocaleで設定
        'year': 'numeric', 'month': '2-digit', 'day': '2-digit'
    },
    'buttonText': {
        # 各ボタンを日本語化してみる
        'today': '今日',
        'month': '月ごと',
        'week': '週ごと',
        'day': '日ごと',
        'list': 'リスト'
    },
    'locale': 'ja', # 日本語化する
    'firstDay': '1', # 週の最初を月曜日(1)にする。デフォルトは日曜日(0)
}

# イベントを表示するカレンダーを作成
st_calendar.calendar(events=event_list, options=options)