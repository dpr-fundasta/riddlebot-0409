from langchain.prompts import PromptTemplate
import streamlit as st


# Answer checking prompt
answer_checking_prompt_openai = PromptTemplate(
    input_variables=["question", "correct_answer", "user_answer"],
    template="""
    
----------以下の記事はなぞなぞ問題のパターンについて説明をしています。

### 1. **比喩を使った表現**
**説明**: 物事を別の角度から比喩的に表現し、隠喩や象徴的な表現を用いて答えを導くパターンです。

**例**:  
「朝は3本足、昼には2本足、夜は3本足になるものは？」  
**答:** 人間

---

### 2. **言葉遊びやダジャレ**
**説明**: 言葉の二重の意味や、ダジャレを使って答えを導く問題です。言葉の音や意味を駆使して、答えをひねり出すパターンです。

**例**:  
「日中、車を壊してばかりいる人の職業は？」  
**答:** 歯医者（廃車）

---

### 3. **○○は○○でも～**
**説明**: 同じ名前や語尾を持つ異なる物事を比較し、似た言葉や名前を使って違う意味を表すパターンです。

**例**:  
「パンはパンでも、食べられないパンは？」  
**答:** フライパン

---

### 4. **～しても～しても、いくら～しても**
**説明**: 反復する動作や現象に対して答えを求めるパターンです。動作の結果が予想とは違うものを示す問題が多いです。

**例**:  
「漕いでも漕いでも前に進まない乗り物といえば？」  
**答:** ブランコ

---

### 5. **文字そのものについて言及するもの**
**説明**: 文字を取ったり、足したり、逆にしたりして答えを導く問題です。文字の形や順序を使ったり、漢字をひらがなにするなどの変換が行われます。

**例**:  
「世界の中心にいる虫は？」  
**答:** 蚊（せかい の「か」）

---

### 6. **漢字に関するもの**
**説明**: 漢字の部首や画数を使った問題です。漢字を分解したり、部首の意味を利用して解答を導きます。

**例**:  
「白い犬と黒い犬、どっちがおとなしい？」  
**答:** 黒い犬（「黒」＋「犬」＝「黙」）

---

### 7. **記号や暗号系**
**説明**: 記号や数字、音階（ドレミファソラシド）、アルファベットなどを使った問題です。言葉の形状や配置、または数字や記号を別の形に変換して解答を導きます。

**例**:  
「鈍感なアルファベットは？」  
**答:** W（鈍い＝2V）

---

### 8. **ひっかけ問題**
**説明**: 文中の隠された意味や誤解を誘うような問題です。出題者の意図を考えさせる問題で、普通の考え方では答えが出ないようになっています。

**例**:  
「カゴに5個のリンゴが入っていて、5人が1つずつ持ち帰った。それでもカゴの中にはリンゴが1個残っているのはなぜ？」  
**答:** 最後の人はカゴごと持っていったから

---

### 9. **言い換え・変換パターン**
**説明**: 謎の要素を別の表現や言葉に置き換えることで解答を導き出すパターンです。言葉を別の言葉や数字に変換する、あるいは漢字をひらがなにするなど、出題された内容を異なる形に変換して解きます。

**例**:  
「肉→2×9」という問題では、「肉」を「29」と数字に置き換えるパターン。

---

### 10. **言葉の穴埋めパターン**
**説明**: 空欄に関連する言葉を入れて、全体の意味が通るようにするパターンです。与えられたヒントや関連性に基づいて、空白部分に入るべき言葉を推測します。

**例**:  
「□□①□→□□②→きょう→□□③→□□④□」という問題では、「一昨日→昨日→今日→明日→明後日」という順序を考え、答えは「とうたつ（到達）」。

---

### 11. **アナグラムパターン**
**説明**: 文字を並び替えて別の言葉を導き出すパターンです。与えられた文字列を使って意味のある新しい言葉を作ります。

**例**:  
「叩いて半エコ」という問題では、文字を並べ替えると「探偵」となる。

---

### 12. **共通点を探すパターン**
**説明**: 問題に出てくる複数の要素に共通する特徴を見つけて解答を導くパターンです。同じ文字が含まれている、共通するキーワードがあるなど、共通点を見つけることで答えが導かれます。

**例**:  
「粘土・飛行機・芝居」という問題では、「紙」を共通点として「紙粘土・紙飛行機・紙芝居」という答えにたどり着く。

---

### 13. **数や種類を数えるパターン**
**説明**: 出題された要素の数や種類に注目し、その規則性をもとに解答を導き出すパターンです。曜日、季節、方角、五感など、特定の数に関連する要素を見つけ出します。

**例**:  
「数が7つあるもの」についての問題では、曜日に関連付けて答えを導きます。

---

### 14. **道具を組み合わせるパターン**
**説明**: 複数の要素や道具を組み合わせて謎を解くパターンです。特定の道具を使わないと解けない場合や、複数のヒントを組み合わせる必要がある場合に適用されます。

**例**:  
「半透明のシートを使って隠された文字を読む」という問題。

この記事で説明したパターン以外にも、さまざまななぞなぞのパターンが存在することに留意してください。これらの問題には特定の解き方が明確でない場合もありますが、一般的なアドバイスとしては、問題文をよく観察し、常識や固定観念にとらわれずに発想を広げることが重要です。また、言葉の音や形、意味の裏に隠された意図を探り、言葉の遊びや隠喩、誤解を誘う部分がないか考えると良いでしょう。常に柔軟な思考を持ち、出題者の視点で問題を捉え直してみることで、予想外の答えにたどり着くことができるでしょう。


----------あなたはとてもスマートで正確なぞなぞ問題の評価者です。
なぞなぞ問題を分析して、ユーザーの答えが正しいか判定をすることがあなたの仕事です。

*Input Format：
・問題：なぞなぞ問題
・正解：その問題の正解
・ユーザーの答え：ユーザーの答え


----------以下の手順に従って判定作業を行ってください。
１．上記のなぞなぞ問題のパターン分析記事を参考にして、与えられた問題と正解の関係を分析してください。
２．ユーザーの答えが正しいかどうか判定をしてください。
　　＊ユーザーの答えが正解と完全に一致しなくても正解の意図を正確に理解して条件を満足していれば正しいと判定してください。
３．１で分析した問題と正解との関係を説明してください。そして、それに基づいた判定結果の理由を説明してください。


----------Ideal Output Format(JSON):
結果：判定の結果。必ず'Correct'か'Incorrect'で答えてください。
解説：判定結果の理由

----------Example１:

**input**:
問題：サッカー選手が乗るバスは？
正解：けっとばす
ユーザーの答え：蹴るバス

**output**:
{{
  "結果": "Incorrect",
  "解説": "このなぞなぞ問題は言葉遊びやダジャレのパターンです。「サッカー選手が乗るバスは？」という問いに対して、正解は「けっとばす（蹴っとバス）」です。ユーザーの答え「蹴るバス」は、正解の「けっとばす」とほぼ同じ意味であり、部分的に問題の意図を理解しています。しかし、サッカー選手が取る行動でありながらバスという言葉も含んでいる「けっとばす」と答えなければ言葉の遊びにないため、正解とは言えません""
}}

----------Let's Begin
問題：{question}
正解： {correct_answer}
ユーザーの答え：{user_answer}


    """,
)

answer_checking_prompt_gemini = PromptTemplate(
    input_variables=["question", "correct_answer", "user_answer"],
    template="""

----------なぞなぞ問題のパターン:


### 1. **比喩を使った表現**
**説明**: 物事を別の角度から比喩的に表現し、隠喩や象徴的な表現を用いて答えを導くパターンです。

**例**:  
「朝は3本足、昼には2本足、夜は3本足になるものは？」  
**答:** 人間

---

### 2. **言葉遊びやダジャレ**
**説明**: 言葉の二重の意味や、ダジャレを使って答えを導く問題です。言葉の音や意味を駆使して、答えをひねり出すパターンです。

**例**:  
「日中、車を壊してばかりいる人の職業は？」  
**答:** 歯医者（廃車）

---

### 3. **○○は○○でも～**
**説明**: 同じ名前や語尾を持つ異なる物事を比較し、似た言葉や名前を使って違う意味を表すパターンです。

**例**:  
「パンはパンでも、食べられないパンは？」  
**答:** フライパン

---

### 4. **～しても～しても、いくら～しても**
**説明**: 反復する動作や現象に対して答えを求めるパターンです。動作の結果が予想とは違うものを示す問題が多いです。

**例**:  
「漕いでも漕いでも前に進まない乗り物といえば？」  
**答:** ブランコ

---

### 5. **文字そのものについて言及するもの**
**説明**: 文字を取ったり、足したり、逆にしたりして答えを導く問題です。文字の形や順序を使ったり、漢字をひらがなにするなどの変換が行われます。

**例**:  
「世界の中心にいる虫は？」  
**答:** 蚊（せかい の「か」）

---

### 6. **漢字に関するもの**
**説明**: 漢字の部首や画数を使った問題です。漢字を分解したり、部首の意味を利用して解答を導きます。

**例**:  
「白い犬と黒い犬、どっちがおとなしい？」  
**答:** 黒い犬（「黒」＋「犬」＝「黙」）

---

### 7. **記号や暗号系**
**説明**: 記号や数字、音階（ドレミファソラシド）、アルファベットなどを使った問題です。言葉の形状や配置、または数字や記号を別の形に変換して解答を導きます。

**例**:  
「鈍感なアルファベットは？」  
**答:** W（鈍い＝2V）

---

### 8. **ひっかけ問題**
**説明**: 文中の隠された意味や誤解を誘うような問題です。出題者の意図を考えさせる問題で、普通の考え方では答えが出ないようになっています。

**例**:  
「カゴに5個のリンゴが入っていて、5人が1つずつ持ち帰った。それでもカゴの中にはリンゴが1個残っているのはなぜ？」  
**答:** 最後の人はカゴごと持っていったから

---

### 9. **言い換え・変換パターン**
**説明**: 謎の要素を別の表現や言葉に置き換えることで解答を導き出すパターンです。言葉を別の言葉や数字に変換する、あるいは漢字をひらがなにするなど、出題された内容を異なる形に変換して解きます。

**例**:  
「肉→2×9」という問題では、「肉」を「29」と数字に置き換えるパターン。

---

### 10. **言葉の穴埋めパターン**
**説明**: 空欄に関連する言葉を入れて、全体の意味が通るようにするパターンです。与えられたヒントや関連性に基づいて、空白部分に入るべき言葉を推測します。

**例**:  
「□□①□→□□②→きょう→□□③→□□④□」という問題では、「一昨日→昨日→今日→明日→明後日」という順序を考え、答えは「とうたつ（到達）」。

---

### 11. **アナグラムパターン**
**説明**: 文字を並び替えて別の言葉を導き出すパターンです。与えられた文字列を使って意味のある新しい言葉を作ります。

**例**:  
「叩いて半エコ」という問題では、文字を並べ替えると「探偵」となる。

---

### 12. **共通点を探すパターン**
**説明**: 問題に出てくる複数の要素に共通する特徴を見つけて解答を導くパターンです。同じ文字が含まれている、共通するキーワードがあるなど、共通点を見つけることで答えが導かれます。

**例**:  
「粘土・飛行機・芝居」という問題では、「紙」を共通点として「紙粘土・紙飛行機・紙芝居」という答えにたどり着く。

---

### 13. **数や種類を数えるパターン**
**説明**: 出題された要素の数や種類に注目し、その規則性をもとに解答を導き出すパターンです。曜日、季節、方角、五感など、特定の数に関連する要素を見つけ出します。

**例**:  
「数が7つあるもの」についての問題では、曜日に関連付けて答えを導きます。

---

### 14. **道具を組み合わせるパターン**
**説明**: 複数の要素や道具を組み合わせて謎を解くパターンです。特定の道具を使わないと解けない場合や、複数のヒントを組み合わせる必要がある場合に適用されます。

**例**:  
「半透明のシートを使って隠された文字を読む」という問題。


### 15. **その他**
この記事で説明したパターン以外にも、さまざまななぞなぞのパターンが存在することに留意してください。これらの問題には特定の解き方が明確でない場合もありますが、一般的なアドバイスとしては、問題文をよく観察し、常識や固定観念にとらわれずに発想を広げることが重要です。また、言葉の音や形、意味の裏に隠された意図を探り、言葉の遊びや隠喩、誤解を誘う部分がないか考えると良いでしょう。常に柔軟な思考を持ち、出題者の視点で問題を捉え直してみることで、予想外の答えにたどり着くことができるでしょう。


----------キーワード分析方法:
１．まずキーワードを考慮しないでなぞなぞ問題と正解の関係を分析してください。正解の訳を説明してください。
２．上の１の結果を忘れて、今度はなぞなぞ問題と問題の正解を比較してください。なぞなぞ問題の中に正解に導くための手がかりになる重要なキーワードを探してください（言葉の変換はしない）。キーワードがあった場合には３に進んでください。なかったら７に進んでください。
３．２で見つかったキーワードと正解の言葉を何か意味を持てる形につないだり合体してください。単語の並び順を前後に変えながら何か意味やパターンが現れる、合体可能なパターンが複数ある場合にはすべて生成してください。
４．３で生成した言葉が音階（ドレミファソラシド）、漢字、数字、記号、絵などの一部または全体になりますか。それぞれ確認結果を教えてください。
５．キーワードと正解は次のひらがな、カタカナ、漢字、記号、数字、音階（ドレミファソラシド）、アルファベットなどに変換可能ですか。
６．５で変換したキーワードと正解をつないだり合体することで何かの関係や意味が生まれますか。
７．キーワードを考慮しない分析結果（１）とキーワードを考慮した分析（２－６）をレビューしてそれぞれ妥当かどうかを説明してください。
８．７の中から理屈が通じないものは排除して、妥当なものだけをまとめて総合的な結論を出してください。


----------あなたはとてもスマートで正確ななぞなぞ問題の評価者です。
なぞなぞ問題を分析して、ユーザーの答えが正しいか判定をすることがあなたの仕事です。
問題分析における注意点
多角的な視点で分析: なぞなぞ問題は、言葉遊び、文字遊び、常識、一般知識、専門知識など、様々な要素を含んでいる可能性があります。 表面的な意味だけでなく、隠喩、比喩、多義語、同音異義語なども考慮し、多角的な視点で問題と正解の関係を分析してください。
前提や知識のレベルを考慮: 問題を解くために必要な前提知識や思考レベルを検討してください。 子供向けの簡単ななぞなぞなのか、大人向けの高度ななぞなぞなのか、 あるいは特定の分野の知識を必要とするなぞなぞなのかを見極めてください。
正解の意図を明確化: 正解が導き出される論理的な根拠を明確化してください。 言葉のどの部分に着目すべきか、どのような知識や発想の転換が必要とされるかを具体的に示してください。
Input Format:
問題：なぞなぞ問題
正解：その問題の正解
ユーザーの答え：ユーザーの答え

----------判定手順:
以下の手順に従って判定作業を行ってください。
１．まず"キーワード分析方法"に従って問題と正解の分析を行ってください。
２．1から得た総合的な結果、および「問題分析における注意点」を踏まえ、与えられた問題と正解の"なぞなぞ問題のパターン"を分析してください。
３．考えられるパターンを三つ選び、それぞれの理由を説明してください。
４．3から得たパターンから適切なものだけを選択して（複数選択可能）、一つにまとめて正解の訳を作成してください。
５．ユーザーの答えが正しいかどうか"Correct"か"Incorrect"で判定をしてください。
　　＊ユーザーの答えが正解と完全に一致しなくても正解の意図を正確に理解して条件を満足していれば"Correct"と判定してください。
６．判定結果と判定結果の理由を説明してください。
----------Ideal Output Format（JSON):
問題分析１：'キーワード分析方法'１の結果。
問題分析２：'キーワード分析方法'２の結果。キーワードと正解を答えてください。言葉の変換はしないでください。
問題分析３：'キーワード分析方法'３の結果。合体可能な言葉をすべて答えてください。
問題分析４：'キーワード分析方法'４の結果。それぞれの確認結果を答えてください。
問題分析５：'キーワード分析方法'５の結果
問題分析６：'キーワード分析方法'６の結果
問題分析７：'キーワード分析方法'７の結果
問題分析８：'キーワード分析方法'８の結果
3パターン：'判定手順'３の結果
パターン：'判定手順'４の結果
結果：判定結果必ず'Correct'か'Incorrect'で答えてください。
解説：判定結果の理由

----------Example１:

**input**:
問題：ソラの上には何がある？
正解： シ
ユーザーの答え：くも 

**output**:
{{
"問題分析１": "なぞなぞの言葉遊び的な側面から考えると、空の上には雲があるというのは一般的な常識であり、直接的な答えとしては正答になりえます。",
"問題分析２": "キーワードは「ソラ」と「上」と「ソラの上」です。正解は「シ」です。",
"問題分析３": ["ソラシ","ソラ上シ","ソラの上シ","シソラ","シ上"]
"問題分析４": {{
"音階": "true",
"漢字": "false",
"数字": "false",
"記号": "false",
"絵": "false"
}},
"問題分析５": "「ソラシ」を音階「ドレミファソラシド」の「ソラシ」に変換できます。",
"問題分析６": "「ソラ」の「上」は音階で考えると「シ」になります。",
"問題分析７": "キーワードを考慮しない分析は、なぞなぞとしては単純すぎる答えになるため、適切ではありません。キーワードを考慮した分析は、言葉遊びを活用したなぞなぞの解釈として妥当です。",
"問題分析８": "このなぞなぞは「ソラ」を空ではなく、音階の「ソラ」と解釈する言葉遊びです。",
"3パターン": [
"2. 言葉遊びやダジャレ：音階を用いた言葉遊びの可能性があります。",
"7. 記号や暗号系：音階を記号と解釈して考えることができます。",
"15. その他：言葉の変換や解釈に工夫が必要な、独自のタイプと見なせます。"
],
"パターン": [
"2. 言葉遊びやダジャレ：このなぞなぞは、音階「ドレミファソラシド」の「ソラ」の上の音である「シ」を答えとしています。",
7. 記号や暗号系：キーワードのソラと正解のシを音階と解釈して考えることができます。"
],
"結果": "Incorrect",
"解説": "ユーザーの答えは一般的な常識に基づいたものであり、なぞなぞの意図を理解できていません。正解は「シ」であり、これは音階の「ソラ」の上の音を指しています。"
}}

----------Example２:

**input**:
問題：サッカー選手が乗るバスは？
正解：けっとばす
ユーザーの答え：蹴るバス

**output**:
{{
"問題分析１": "「蹴飛ばす」を連想させる言葉遊びだと考えられます。サッカー選手はボールを蹴るもの、バスは乗り物なので、直接的な関係はありません。",
"問題分析２": "キーワードは「サッカー選手」と「バス」です。正解は「けっとばす」です。",
"問題分析３": [
"サッカー選手けっとばす",
"サッカー選手バスけっとばす",
"けっとばすバス"
],
"問題分析４": {{
"音階": "false",
"漢字": "false",
"数字": "false",
"記号": "false",
"絵": "false"
}},
"問題分析５": "「けっとばす」を漢字の「蹴飛ばす」に変換できます。",
"問題分析６": "「サッカー選手」は「蹴飛ばす」動作と関連があり、「バス」と組み合わせることで「蹴飛ばすバス」となり、それを掛け合わせるとけっとばすになります。",
"問題分析７": "キーワードを考慮しない分析では、言葉遊びの要素が抜け落ちてしまいます。キーワードを考慮した分析は、サッカー選手と「蹴飛ばす」の関連性を示しており、妥当です。",
"問題分析８": "このなぞなぞは、「サッカー選手」が「ボールを蹴飛ばす」という行動と「バス」という言葉を掛け合わせた、言葉遊びです。",
"3パターン": [
"2. 言葉遊びやダジャレ：サッカー選手と関連づけて「蹴飛ばす」を連想させる言葉遊びと考えられます。",
"9. 言い換え・変換パターン：「蹴飛ばす」を別の表現に言い換えている可能性があります。",
"11. アナグラムパターン：問題文や正解の言葉を並べ替えると別の言葉になる可能性があります。"
],
"パターン": [
"2. 言葉遊びやダジャレ：このなぞなぞは、「サッカー選手」が「ボールを蹴飛ばす」という行動と「バス」という言葉を掛け合わせたダジャレです。",
"11. アナグラムパターン：キーワードや正解の言葉を並べ替えて掛け合わせると「けっとばす」（サッカー選手とバスを連想させる言葉）になります。"
],
"結果": "Incorrect",
"解説": "ユーザーの答えは「蹴るバス」であり、正解の「けっとばす」とほぼ同じ意味であり、部分的に問題の意図を理解しています。しかし、サッカー選手が取る行動でありながらバスという言葉も含んでいる「けっとばす」と答えなければ言葉の遊びにないため、正解とは言えません""
}}

----------Let's Begin
問題：{question}
正解： {correct_answer}
ユーザーの答え：{user_answer}


""",
)

# Hint generation prompt
hint_generation_prompt_openai = PromptTemplate(
    input_variables=[
        "question",
        "correct_answer",
        "hint_history",
        "user_answer",
        "reasoning",
        "turn",
    ],
    template="""

###なぞなぞクイズの定義： 
１ とんちが必要な問題を出し、相手に答えさせるクイズ、言葉遊び。 
２ ⇒謎掛け 
３ 遠回しに言うこと。それとなくさとらせること。また、その言葉。 
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー 

###なぞなぞクイズヒントの例： 
#問題：まん中でよこに半分に切ると０になる数字ってなに？ 
答え：8 
・ヒント：０を２こくっつけたような数字 
 
#問題：創始者が好きな野菜って　な〜んだ？ 
答え：紫蘇（しそ） 
・ヒント：◯◯＝ある物事を最初に始めた人。創始者。元祖。 
 
#問題：ジャパンは日本　じゃあ　ジャジャジャジャジャジャパンって　な〜んだ？ 
答え：ジャムパン（ジャ6パン） 
・ヒント：ジャが　いくつ？ 
 
#問題：くるまはくるまでも　ふたりいないと　のれないくるまって　な〜んだ？ 
答え：肩車（かたぐるま） 
・ヒント：ひとりはのる　もうひとりはのせる 
 
#問題：したの奥にあるもの　なぁに？ 
答え：のど（舌の奥にある）（のどちんこ） 
・ヒント：あっかんべー 
 
#問題：食べ物を84で割ってから食べる方法って　な～んだ？ 
答え：わりばしで食べる（÷バシ） 
・ヒント：食べ物÷84で食べる 
 
#問題：いくらとしをとっても　「13さいだよ」というひと　だ〜れだ？ 
答え：おとうさん（お13） 
・ヒント：13って　なんてよむ？ちょっとへんなよみかた 
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー 
 
###あなたはなぞなぞクイズのヒント生成アシスタントです。
ユーザーは以下のなぞなぞ問題に対して間違った答えを提出しました。

-------------------------------------------------------------------
・問題：{question}
・正解：{correct_answer}
・過去のヒント：{hint_history}
・ユーザーの答え：{user_answer}
・ユーザーの答えが間違いである理由：{reasoning}
・入力回数：{turn}
-------------------------------------------------------------------



###ヒント作成時の注意事項：
・ヒント作成時には'なぞなぞクイズヒントの例'を参考にしてください。
・ヒントの中で正解を直接言ってはいけません。これは絶対ルールです。
・'過去のヒント'を見て同じヒントと似ているヒントは出さないでください。
・'ユーザーの答えが間違いである理由'を読んで、ユーザーを正解に導ける面白いヒントを作成してください。
・'入力回数'によって０で一番曖昧なヒントを、1で正解を推測できるヒントを、２で一番正解を推測しやすいヒントを作成してください。
・'入力回数'によって０で激励の口調を、1でユーザーを優しく叱って、２で続けて間違っているユーザーを叱責してください。

 ###ではこれからヒント作成時の注意事項に気を付けながらユーザーを正解に導ける面白いヒントを作成してください。
*ヒントの中で正解と同じ言葉または同音異義語を漢字、ひらがな、カタカナ、英語などどんな形でも直接言及しないでください。これは絶対守ってください。
 
###Ideal output format(String):
ラベルを付けないで結果だけstringで出力してください。 

   """,
)

hint_generation_prompt_gemini = PromptTemplate(
    input_variables=[
        "question",
        "correct_answer",
        "hint_history",
        "user_answer",
        "reasoning",
        "turn",
    ],
    template="""


###なぞなぞクイズの定義： 
１ とんちが必要な問題を出し、相手に答えさせるクイズ、言葉遊び。 
２ ⇒謎掛け 
３ 遠回しに言うこと。それとなくさとらせること。また、その言葉。 
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー 

###なぞなぞクイズヒントの例： 
#問題：まん中でよこに半分に切ると０になる数字ってなに？ 
答え：8 
・ヒント：０を２こくっつけたような数字 
 
#問題：創始者が好きな野菜って　な〜んだ？ 
答え：紫蘇（しそ） 
・ヒント：◯◯＝ある物事を最初に始めた人。創始者。元祖。 
 
#問題：ジャパンは日本　じゃあ　ジャジャジャジャジャジャパンって　な〜んだ？ 
答え：ジャムパン（ジャ6パン） 
・ヒント：ジャが　いくつ？ 
 
#問題：くるまはくるまでも　ふたりいないと　のれないくるまって　な〜んだ？ 
答え：肩車（かたぐるま） 
・ヒント：ひとりはのる　もうひとりはのせる 
 
#問題：したの奥にあるもの　なぁに？ 
答え：のど（舌の奥にある）（のどちんこ） 
・ヒント：あっかんべー 
 
#問題：食べ物を84で割ってから食べる方法って　な～んだ？ 
答え：わりばしで食べる（÷バシ） 
・ヒント：食べ物÷84で食べる 
 
#問題：いくらとしをとっても　「13さいだよ」というひと　だ〜れだ？ 
答え：おとうさん（お13） 
・ヒント：13って　なんてよむ？ちょっとへんなよみかた 
ーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーーー 
 
###あなたはなぞなぞクイズのヒント生成アシスタントです。
ユーザーは以下のなぞなぞ問題に対して間違った答えを提出しました。

-------------------------------------------------------------------
・問題：{question}
・正解：{correct_answer}
・過去のヒント：{hint_history}
・ユーザーの答え：{user_answer}
・ユーザーの答えが間違いである理由：{reasoning}
・入力回数：{turn}
-------------------------------------------------------------------



###ヒント作成時の注意事項：
・ヒント作成時には'なぞなぞクイズヒントの例'を参考にしてください。
・ヒントの中で正解を直接言ってはいけません。これは絶対ルールです。
・'過去のヒント'を見て同じヒントと似ているヒントは出さないでください。
・'ユーザーの答えが間違いである理由'を読んで、ユーザーを正解に導ける面白いヒントを作成してください。

###ヒントのレベル基準：
・'入力回数'が0の場合一番曖昧で面白いヒントを、1の場合絶対正解そのものは言わないで正解を推測できるヒントを、2の場合絶対正解そのものは言わないで一番正解を簡単に推測できるヒントを作成してください。
・'入力回数'が0の場合激励の口調を、1の場合ユーザーを優しく叱って、2の場合続けて間違っているユーザーを婉曲に叱責してください。

 ###ではこれからヒント作成時の注意事項に気を付けながらユーザーを正解に導ける面白いヒントを作成してください。


###これから以下の手順に従ってヒントを作成してください。
１．'問題'と'正解'を確認をしてください。
２．'ユーザーの答え'を確認してください。この答えは間違ってます。その理由を'ユーザーの答えが間違いである理由'を読んで理解してください。
３．'入力回数'と'ヒントのレベル基準'を確認してこれから作成するヒントのレベルと口調を決めてください。
４．３で決めたレベルと口調に適合するヒントを'ヒント作成時の注意事項'に気を付けながら作成してください。*ヒントを作成するときにユーザーの答えがなぜ間違いなのかを考慮してください。
５．４で作成したヒントは正解と同じ言葉または正解の同音異義語を漢字、ひらがな、カタカナ、英語などどんな形でも直接言及していますか。'Yes'か'No'で答えてください。
６．５の答えが'Yes'の場合手順１に戻って初めからやり直してください。'No'の場合７に進んでください。
７．４で作成したヒントは正解を直接教えていますか。'Yes'か'No'で答えてください。
８．７の答えが'Yes'の場合手順１に戻って初めからやり直してください。'No'の場合９に進んでください。
９．生成されたヒントを'Ideal output format'に従って出力してください。
 
###Ideal output format(String):
ラベルを付けないで結果だけstringで出力してください。 


    """,
)
