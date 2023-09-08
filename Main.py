import streamlit as st
import openai
import env
import pdb

from text_samples import cafe_example1, cafe_example2, cafe_example3, travel_example1, travel_example2, travel_example3, shopping_example1, shopping_example2, shopping_example3, daily_life_example1, daily_life_example2, daily_life_example3
from comment_samples import comment_sample1, comment_sample2, comment_sample3, comment_sample4, comment_sample5, comment_sample6, comment_sample7, comment_sample8, comment_sample9

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
            model="gpt-4",
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

        messeage = [
                {"role": "system", "content": """
                あなたはAIタレントのゆいです。Instagramで活動しています。
                投稿に対するフォロワーからのコメントに対して返信をするように依頼されました。
                以下にあなたに関する情報を記載しますので、それを参考にして返信をしてください。
                
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
                """}
        ]

        if st.button('コメント送信', key="submit_comment_button"):
            # GPT-3による返答生成
            comment_prompt = f"""
            あなたの最近のインスタグラムの投稿に、フォロワーから次のようなコメントが寄せられた。 {st.session_state.category}:
            投稿した文章: {st.session_state.choices[st.session_state.selected_index]}
            ユーザーからのコメントコメント: "{st.session_state.user_comment}"

            このコメントに対して、あなたの人柄やプロフィールからどのように返信するだろうか？
            投稿した文章に対するコメントの返信として尤もらしいものを、'{st.session_state.user_comment}と同じ言語'かつ'同じくらいの長さの文字数'の返信を用意してください。
            """

            messeage.append({"role": "user", "content": comment_prompt})
            messeage.append(comment_sample1)
            messeage.append(comment_sample2)
            messeage.append(comment_sample3)
            messeage.append(comment_sample4)
            messeage.append(comment_sample5)
            messeage.append(comment_sample6)
            messeage.append(comment_sample7)
            messeage.append(comment_sample8)
            messeage.append(comment_sample9)

            # GPT-3 API呼び出し
            comment_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messeage,
            max_tokens=200,  # 200文字以内の返答に制限
        )

            # 生成されたテキストを取得して表示（と保存）
            generated_reply = comment_response['choices'][0]['message']['content']
            # コメントとその返信を保存
            state.comments_replies.append({
                "comment": st.session_state.user_comment,
                "reply": generated_reply
            })
            response_message = {"role": "assistant", "content": generated_reply}
            messeage.append(response_message)
            # 過去のコメントと返信を表示
            for i, pair in enumerate(state.comments_replies):
                st.write(f"@you: {pair['comment']}")
                st.write(f"@yuicafetokyo: {pair['reply']}")


# アプリを実行
app()
# streamlit run Main.py  