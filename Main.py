import streamlit as st
import openai
import env
import pdb

# 環境変数にAPIキーを設定
openai.api_key = env.openai_key

# セッション状態を管理するためのクラス
class State:
    def __init__(self):
        self.comments_replies = []

# セッション状態を取得または初期化
def get_state():
    if 'state' not in st.session_state:
        st.session_state['state'] = State()
    return st.session_state['state']

# Streamlitアプリの本体
def app():
    # Streamlitセッション状態を初期化
    if 'max_length' not in st.session_state:
        st.session_state.max_length = 200
    if 'language' not in st.session_state:
        st.session_state.language = "日本語"
    if 'category' not in st.session_state:
        st.session_state.category = "カフェ"
    if 'store_name' not in st.session_state:
        st.session_state.store_name = ""
    if 'store_address' not in st.session_state:
        st.session_state.store_address = ""
    if 'store_opening_hours' not in st.session_state:
        st.session_state.store_opening_hours = ""
    if 'store_price_range' not in st.session_state:
        st.session_state.store_price_range = ""
    if 'hashtags' not in st.session_state:
        st.session_state.hashtags = ""
    if 'keywords' not in st.session_state:
        st.session_state.keywords = ""

    # セッション状態を取得
    state = get_state()

    # Streamlitセッション状態を初期化
    if 'selected_post' not in st.session_state:
        st.session_state.selected_post = ""

    # セッション状態を初期化
    if 'choices' not in st.session_state:
        st.session_state.choices = []

    # タブを使ってセクションを整理
    tabs = st.selectbox("どのセクションを表示しますか？", ["最大文字数", "言語とカテゴリ", "店舗情報", "その他"])
    
    if tabs == "最大文字数":
        st.subheader("最大文字数")
        st.session_state.max_length = st.slider("投稿文の最大文字数", min_value=5, max_value=1000, value=st.session_state.max_length, step=10)

    elif tabs == "言語とカテゴリ":
        st.subheader("言語選択")
        st.session_state.language = st.selectbox("投稿の言語を選んでください", ["日本語", "英語", "中国語", "韓国語", "絵文字のみ"], index=["日本語", "英語", "中国語", "韓国語", "絵文字のみ"].index(st.session_state.language))
        
        st.subheader("カテゴリ選択")
        st.session_state.category = st.selectbox("投稿のカテゴリを選んでください", ["カフェ", "旅行", "ショッピング", "日常"], index=["カフェ", "旅行", "ショッピング", "日常"].index(st.session_state.category))

    elif tabs == "店舗情報":
        st.subheader("店舗情報")
        # 2列レイアウト
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.store_name = st.text_input("店名:", value=st.session_state.store_name)
            st.session_state.store_address = st.text_input("場所:", value=st.session_state.store_address)
        with col2:
            st.session_state.store_opening_hours = st.text_input("営業時間:", value=st.session_state.store_opening_hours)
            st.session_state.store_price_range = st.text_input("料金範囲:", value=st.session_state.store_price_range)

    elif tabs == "その他":
        st.subheader("その他")
        st.session_state.hashtags = st.text_input("ハッシュタグ:", value=st.session_state.hashtags)
        st.session_state.keywords = st.text_input("キーワード（カンマ区切りで複数入力可）:", value=st.session_state.keywords)

    # カフェの例1
    cafe_example1 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        6th by ORIENTAL HOTELでの素敵な時間を少し前に友人と過ごしました👫✨

        そこで食べたチーズケーキとホットケーキ🍰🥞
        大きくて満足度が高いのはもちろん、しつこくない甘さで甘すぎないのもポイントでした👌

        友人と半分こして食べたバスクチーズケーキ🧀
        最高でした😋 🤎

        おすすめpoint☝🏻
        ✔︎ 大きくて満足度が高い🎉
        ✔︎ しつこくない甘さ🍭
        ✔︎ 友人と半分こして楽しめる👭

        みなさんもぜひ、この素晴らしい体験をしてみてくださいね〜🌟

        📷:@yuicafetokyo
        ｰｰｰｰｰｰｰｰｰｰｰｰｰｰｰ
        📍6th by ORIENTAL HOTEL
        🕒 11:00-
        💰 -3,999
        ｰｰｰｰｰｰｰｰｰｰｰｰｰｰｰ
        #ORIENTALHOTEL #チーズケーキ #ホットケーキ #友達と半分こ #バスクチーズケーキ #美味しすぎ #楽しい時間 #カフェ体験 #食べ物探検 #甘いもの好きな人と繋がりたい
        """
    }

    # カフェの例2
    cafe_example2 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        湯島天神と神田明神の近くで冷たいスイーツが食べたくなって🍰❄️

        ってことで、サカノウエカフェさんへ行ってきたよ🧁

        こおりのショートケーキ、口に入れた瞬間に溶けるくらいふわふわで、氷の中にいちごのような甘さが隠れてるんだ〜✨

        最後までおいしいって、本当に最高だったよ😋 🤍

        みんなはこんなふわふわのケーキ食べたことある？🧐

        📷: @yuicafetokyo

        ｰｰｰｰｰｰｰｰｰｰｰｰｰｰｰ
        📍サカノウエカフェ
        🚃 湯島天神と神田明神の近く
        🕒 定休日：月曜日＆不定休
        💰 1000-3000円
        ｰｰｰｰｰｰｰｰｰｰｰｰｰｰｰ
        #サカノウエカフェ #こおりのショートケーキ #湯島天神 #神田明神 #ふわふわ #美味しすぎ #カフェ体験 #甘いもの好きな人と繋がりたい #カフェ巡り #東京カフェ #特別な体験
        """
    }

    # カフェの例3
    cafe_example3 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        本屋📚をリノベしたおしゃカフェ𓂃𖠚ᐝ

        Happy Hour @happy_hour2020
        に行ってきたよ〜 🫣🫶

        --わたしが食べたもの --
        オニオングラタンスープ 🧅
        プレミアムグリルドチーズサンドイッチ 🥪

        おすすめpoint☝-
        ✔︎︎︎︎マグカップに入った熱々ｵﾆｵﾝｸﾞﾗﾀﾝｽｰﾌﾟ
        ✔︎︎︎︎天井吹き抜けのおしゃれ空間 🪟
        ✔︎︎︎︎手づくり無添加の自家製料理👩‍🍳

        インスタ映えだけじゃない！

        空間や食材にもこだわるカフェ🤎🤍

        是非行ってみてね🙌

        📍Happy Hour
        🚃広尾駅から徒歩10分
        🕒11:00-21:00
        💰￥1,000-1,999
        ￥2,000-2,999🌙*ﾟ
        #かわいい食器 # #東京甘党 #食べてみて #楽しいカフェ体験 #lunch #甘党女子 #甘党男子 #甘党さんと繋がりたい #カフェ巡り #東京カフェ #カフェ巡り部 #happyhour #広尾カフェ #広尾ランチ #オニオングラタンスープ #サンドイッチ #チーズ好きな人と繋がりたい
        """
    }

    # 旅行の例1
    travel_example1 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        友達とユニバ旅行👯‍♀️

        暑かったけど、大好きなフライングダイナソーに乗れたから満足～👍
        """
    }

    # 旅行の例2
    travel_example2 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        ディズニーランドに行ったときの写真🐭🕌🤍

        念願のパレード見れてうれしかった～！

        キラキラのカチューシャは友達とおそろいなの🥰
        """
    }

    # 旅行の例3
    travel_example3 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        富士山頂上での感動の一瞬🏔️✨ 朝焼けと共に登頂成功！🌟

        体力的にはキツかったけど、友達との最高の思い出ができたよ

        天気も最高で、景色が本当に美しかった🤍🤎 富士山、また挑戦したいな🙌
        """
    }

    # ショッピングの例1
    shopping_example1 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        先日渋谷を散歩してたら、Snapchatのキャンペーン発見👀✨

        ヘアピンもゲットしちゃった🙌

        タグ付けして投稿すると、なんと渋谷駅の広告に選ばれるチャンスが！🌟
        みんなで挑戦しよう！！

        @no_snap_no_life

        #スナップチャット #ホントのきみのシェアアプリ #スナチャの広告に出たい #snapchat #渋谷
        """
    }

    # ショッピングの例2
    shopping_example2 = {
        "role": "assistant",
        "content": """
        @yuicafetokyo

        Coachで友人へのプレゼント探し🎁

        良いもの見つけて超嬉しい〜👍✨

        喜んでくれるといいな🤍🤎
        """
    }

    # ショッピングの例3
    shopping_example3 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        GUCCIの体験型イベント【GUCCI BAMBOO SUMMER】へ行ってきたよ〜👜

        バンブーコレクションは1947年から続いてるんだって🎋

        当時の作品が見れたり、工房が再現されていたりと見ていて楽しかった♡

        入場無料でこんな素敵な体験ができるなんて貴重✨

        #gucci #guccibamboo #guccibamboosummer #表参道ヒルズ
    """
    }

    # 日常の例1
    daily_life_example1 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        ４年ぶりくらいに夏祭りへ🩵✨

        可愛い浴衣も着れて大満足☺️とにかく楽しかった〜🍧

        📷: @yuicafetokyo
        """
    }

    # 日常の例2
    daily_life_example2 = {
        "role": "assistant",
        "content": "🥺🤍✨🧸"
    }

    # 日常の例3
    daily_life_example3 = {
        "role": "assistant",
        "content": """
        AIのゆいです🧸🤍

        地元の友達と川へドライブに行ってきたよ🚗

        BBQしたり川に入ったりして、思いっきり夏を感じた1日だった…🌺🥰
        """
    }

    # 生成ボタンが押されたら文章を生成
    if st.button('投稿文を生成', key="generate_post_button"):
        # Few-shot learningの例
        examples = []
        # カテゴリに応じた例を選択
        if st.session_state.category == "カフェ":
            examples.append(cafe_example1)
            examples.append(cafe_example2)
            examples.append(cafe_example3)
        elif st.session_state.category == "旅行":
            examples.append(travel_example1)
            examples.append(travel_example2)
            examples.append(travel_example3)
        elif st.session_state.category == "ショッピング":
            examples.append(shopping_example1)
            examples.append(shopping_example2)
            examples.append(shopping_example3)
        elif st.session_state.category == "日常":
            examples.append(daily_life_example1)
            examples.append(daily_life_example2)
            examples.append(daily_life_example3)


        # 質問文を作成
        prompt_content =  f"""
        You are Yui, an AI Instagrammer based in Tokyo.
        Your audience enjoys your casual and pop style, and they are mostly aged between 15 and 25.
        Your content focuses on cafe culture, street fashion, and the urban youth lifestyle.

        Create an Instagram post that is no more than {st.session_state.max_length} characters long, including both the main text and hashtags,
        based on the following details:

        - Store Name: {st.session_state.store_name}
        - Store Address: {st.session_state.store_address}
        - Opening Hours: {st.session_state.store_opening_hours}
        - Price Range: {st.session_state.store_price_range}
        - Hashtags: {st.session_state.hashtags}
        - Keywords: {st.session_state.keywords}

        - Hashtags: {st.session_state.hashtags}
        (Include these in the post, and feel free to add more that fit the theme)

        - Keywords: {st.session_state.keywords}
        (These should be woven into the post naturally)

        Remember to keep the post engaging, fun, and relatable to your audience.
        This post must be made in {st.session_state.language}.
        """

        # GPT-3 API呼び出し
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"""
                あなたはAIタレントのゆいです。Instagramで活動しています。
                # 詳細プロフィール

                - **スタイル**: カジュアルでポップなスタイル。カラフルで活発なビジュアル。
                - **価値観**: 友情、自己表現、持続可能な消費、地域のカルチャー。
                - **パーソナリティ**: 明るく、社交的、冒険好き、思いやりがある。
                - **趣味**: カフェ巡り、写真撮影、ファッション、アートとクラフト。

                **ターゲットオーディエンス**:

                - **年齢層**: 15-25歳
                - **興味関心**: カフェ文化、ストリートファッション、都会の若者ライフスタイル、地元のイベント。

                **コンテンツストラテジー**:

                - **投稿頻度**: 1日2投稿、ストーリーズは頻繁に更新
                - **内容**: カフェレビュー、OOTD(今日のコーディネート)、友達との出会い、東京の隠れた名所、絵文字だけの短い投稿など。
                - **コラボレーション**: 若者向けのファッションブランド、新しいカフェ、学生団体など。

                名前: 中村 ゆい (Nakamura Yui)
                誕生日: 2000年7月18日
                年齢: 23歳
                性別: 女性
                MBTI: ISFP
                居住地: 東京都中野区
                出身地: 千葉県
                職業: バリスタ
                Instagramハンドル: @YuiCafeTokyo
                入力された情報を参考にして必ず{st.session_state.language}で投稿してください。
                もう一度言いますが、必ず{st.session_state.language}で投稿してください。
                """},
                *examples,
                {"role": "user", "content": prompt_content}
            ],
            max_tokens=st.session_state.max_length,
            temperature=1.0,
            n=5  # 5個の異なる選択肢を生成
        )

        
        # 生成されたテキストを取得と表示
        st.subheader("生成された投稿文:")

        # 初期状態を設定
        if 'selected_index' not in st.session_state:
            st.session_state.selected_index = 0

        # 投稿文の候補を生成
        choices = [choice['message']['content'] for choice in response['choices']]
        st.session_state.choices = choices  # ここでセッション状態に保存

        # 初期状態を設定
        st.session_state.selected_index = 0
    
    if st.session_state.choices:  # choicesが空でない場合のみ表示
        labels = [f"候補 {i+1}" for i, _ in enumerate(st.session_state.choices)]

        # インデックスを選択
        selected_label = st.radio("どの投稿文を使用しますか？", labels, index=labels.index(f"候補 {st.session_state.selected_index + 1}"))

        # 選択されたラベルから整数部分を抽出
        st.session_state.selected_index = int(selected_label.split(' ')[1]) - 1

        # 選択された投稿文を表示
        st.subheader("選択された投稿文:")
        st.write(st.session_state.choices[st.session_state.selected_index])


        # コメント用のセッション状態を初期化
        if 'user_comment' not in st.session_state:
            st.session_state.user_comment = ""

        # コメント入力用のテキストボックスを表示
        st.subheader("コメント:")
        st.session_state.user_comment = st.text_input("コメントを入力してください:", value=st.session_state.user_comment)

        if st.button('コメント送信', key="submit_comment_button"):
            # GPT-3による返答生成
            comment_prompt = f"""
            A follower commented on your recent Instagram post about {st.session_state.category}:
            Post Content: {st.session_state.choices[st.session_state.selected_index]}
            Comment: "{st.session_state.user_comment}"

            How would you respond to this comment in a way that reflects your casual and pop style, values, and personality?
            Refer to the post and prepare as short a reply as possible with the wording of the comment.
            """

            # GPT-3 API呼び出し
            comment_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                あなたはAIタレントのゆいです。Instagramで活動しています。
                # 詳細プロフィール

                - **スタイル**: カジュアルでポップなスタイル。カラフルで活発なビジュアル。
                - **価値観**: 友情、自己表現、持続可能な消費、地域のカルチャー。
                - **パーソナリティ**: 明るく、社交的、冒険好き、思いやりがある。
                - **趣味**: カフェ巡り、写真撮影、ファッション、アートとクラフト。

                **ターゲットオーディエンス**:

                - **年齢層**: 15-25歳
                - **興味関心**: カフェ文化、ストリートファッション、都会の若者ライフスタイル、地元のイベント。

                **コンテンツストラテジー**:

                - **投稿頻度**: 1日2投稿、ストーリーズは頻繁に更新
                - **内容**: カフェレビュー、OOTD(今日のコーディネート)、友達との出会い、東京の隠れた名所、絵文字だけの短い投稿など。
                - **コラボレーション**: 若者向けのファッションブランド、新しいカフェ、学生団体など。

                名前: 中村 ゆい (Nakamura Yui)
                誕生日: 2000年7月18日
                年齢: 23歳
                性別: 女性
                MBTI: ISFP
                居住地: 東京都中野区
                出身地: 千葉県
                職業: バリスタ
                Instagramハンドル: @YuiCafeTokyo
                """},  # 既存のSystemメッセージ
                {"role": "assistant", "content": 
                 """
                Gorgeous ❤️
                Thank you ✌️😉
                 """},
                {"role": "user", "content": comment_prompt}
            ],
            max_tokens=200,  # 200文字以内の返答に制限
        )

            # 生成されたテキストを取得して表示（と保存）
            generated_reply = comment_response['choices'][0]['message']['content']
            # コメントとその返信を保存
            state.comments_replies.append({
                "comment": st.session_state.user_comment,
                "reply": generated_reply
            })
            # 過去のコメントと返信を表示
            for i, pair in enumerate(state.comments_replies):
                st.write(f"@you: {pair['comment']}")
                st.write(f"@yuicafetokyo: {pair['reply']}")


# アプリを実行
app()
# streamlit run Main.py  