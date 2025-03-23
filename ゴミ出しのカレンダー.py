import streamlit as st
import streamlit_calendar as st_calendar
from datetime import datetime, timedelta

st.set_page_config(
    page_title="ゴミ出しアプリ",
    page_icon="🚮",
    layout="wide",  # "centered"や"wide"を選べます
    
    )

# カスタムCSSを埋め込む
st.markdown(
    """
    <style>
        .big-font {
            font-size: 50px !important;
            color: #0000FF
        }
        .custom-button {
            background-color: #4CAF50; /* 緑色 */
            color: white; /* 文字色を白に */
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 12px; /* 角を丸くする */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# おしゃれなタイトルを表示
st.markdown('<p class="big-font">ゴミ出し予定アプリ</p>', unsafe_allow_html=True)



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
    
# 粗大ごみの日を追加するための関数
def get_first_wednesday(year, month):
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    if first_weekday <= 2:  # 1日が水曜日より前の場合
        first_wednesday = first_day + timedelta(days=(2 - first_weekday))
    else:  # 1日が水曜日以降の場合
        first_wednesday = first_day + timedelta(days=(2 - first_weekday) + 7)

    return first_wednesday

# 不燃ごみの日を追加するための関数
def get_second_wednesday(year, month):
    first_day = datetime(year, month, 1)
    first_weekday = first_day.weekday()
    if first_weekday <= 2:  # 1日が水曜日より前の場合
        second_wednesday = first_day + timedelta(days=(2 - first_weekday) + 7)
    else:  # 1日が水曜日以降の場合
        second_wednesday = first_day + timedelta(days=(2 - first_weekday) + 14)

    return second_wednesday

# イベントを定義
event_list = []
for i, 日付 in enumerate(曜日の日付):
    if 日付.weekday() == 0:  # 月曜日
        event = {
            'id': str(i + 1),
            'title': '可燃ごみ',
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),
            'editable': False,
        }
        event_list.append(event)  # ここで可燃ごみのイベントを追加

    elif 日付.weekday() == 1:  # 火曜日
        event = {
            'id': str(i + 1),
            'title': '資源・電池類',
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),
            'editable': False,
        }
        event_list.append(event)  # ここで資源・電池類のイベントを追加
        event_list.append({
            'id': str(i + 1) + "_2",
            'title': '紙製容器包装・雑がみ・ペットボトル・空き缶・空きびん',
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),
            'editable': False,
        })

    elif 日付.weekday() == 3:  # 木曜日
        event = {
            'id': str(i + 1),
            'title': '可燃ごみ',
            'start': 日付.strftime('%Y-%m-%dT07:25:00'),
            'end': 日付.strftime('%Y-%m-%dT07:30:00'),
            'editable': False,
        }
        event_list.append(event)  # ここで可燃ごみのイベントを追加

# 不燃ごみの日を追加
for month in range(1, 13):  # 1月から12月まで
    year = 今日.year
    second_wednesday = get_second_wednesday(year, month)
    event = {
        'id': f'second_wednesday_{month}',
        'title': '不燃ごみ',
        'start': second_wednesday.strftime('%Y-%m-%dT07:25:00'),
        'end': second_wednesday.strftime('%Y-%m-%dT07:30:00'),
        'editable': False,
    }
    event_list.append(event)

    # 粗大ごみの日を追加
    first_wednesday = get_first_wednesday(year, month)
    event = {
        'id': f'first_wednesday_{month}',
        'title': '粗大ごみ',
        'start': first_wednesday.strftime('%Y-%m-%dT07:25:00'),
        'end': first_wednesday.strftime('%Y-%m-%dT07:30:00'),
        'editable': False,
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