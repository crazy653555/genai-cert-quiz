# GPT與多模態AI發展時間軸（2017年至今）

> 備註：原始資料中提到「對偶引擎」，經查證應為 **DALL·E**（OpenAI圖像生成引擎，讀音近似「對偶」），以下統一以DALL·E標示。若原意非此，請再確認。

## 一、架構奠基期（2017-2019）

| 時間 | 事件 | 說明 |
|---|---|---|
| 2017年6月 | **Transformer架構誕生** | Google Brain團隊發表論文《Attention Is All You Need》，提出完全基於「自注意力機制（Self-Attention）」的架構，捨棄RNN/LSTM，可平行運算、適合大規模訓練，是後續所有LLM的技術基礎。 |
| 2018年6月 | **GPT-1發布** | OpenAI推出第一代GPT（Generative Pre-trained Transformer），證明「預訓練+微調」模式可行。 |
| 2018年 | **BERT發布（Google）** | 雙向Transformer編碼器，強化上下文理解，與GPT的單向生成式路線並行發展。 |
| 2019年2月 | **GPT-2發布** | 參數量大幅提升，生成文字流暢度大增，OpenAI一度因「濫用疑慮」分階段釋出模型。 |

## 二、大語言模型規模化期（2020-2022）

| 時間 | 事件 | 說明 |
|---|---|---|
| 2020年5月 | **GPT-3發布** | 1750億參數，具備「少樣本學習（Few-shot Learning）」能力，奠定Scaling Laws（規模法則）典範。 |
| 2021年1月 | **DALL·E發布** | OpenAI首代文字生成圖像模型，開啟「文生圖」多模態應用。 |
| 2022年4月 | **DALL·E 2發布** | 圖像品質大幅提升，解析度與真實感增強。 |
| 2022年9月 | **Whisper發布** | OpenAI開源語音辨識模型，支援99種語言，奠定「聽」的能力基礎。 |
| 2022年11月30日 | **ChatGPT發布（基於GPT-3.5）** | 以對話介面封裝LLM，爆紅全球，成為生成式AI革命的起點。 |

## 三、多模態爆發期（2023）

| 時間 | 事件 | 說明 |
|---|---|---|
| 2023年3月14日 | **GPT-4發布** | 首個具備圖像理解能力的多模態模型，語言理解、邏輯推理、法律醫學等表現大幅躍進。 |
| 2023年9月25日 | **ChatGPT新增語音與視覺功能** | 正式具備「聽、說、讀、畫」雛形：可語音對話、辨識圖片內容。 |
| 2023年10月 | **DALL·E 3整合進ChatGPT** | 圖像生成直接整合於對話中，文生圖品質再升級。 |
| 2023年11月 | **GPTs功能推出** | 使用者可用Prompt自訂專屬AI機器人（GPT），並上架供他人使用，標誌「人人可打造AI助理」時代。 |

## 四、智慧助理化期（2024）

| 時間 | 事件 | 說明 |
|---|---|---|
| 2024年1月10日 | **GPT Store正式上線** | GPTs商店化，用戶可發布/使用客製化AI應用，上線時已累積大量應用。 |
| 2024年2月15日 | **Sora首次亮相（文生影片）** | OpenAI展示文字生成高畫質影片模型，多模態從「圖像」擴展至「影片」。 |
| 2024年5月13日 | **GPT-4o發布** | 「o」代表omni（全能），首個原生端到端多模態模型，能即時處理文字、語音、影像，延遲大幅降低，真正實現「全模態互動」。 |
| 2024年9月12日 | **o1-preview發布** | OpenAI首個「推理模型」，強化複雜邏輯與數學推理能力（think before answer）。 |
| 2024年12月5日 | **o1正式版發布** | 推理模型正式開放ChatGPT用戶使用。 |
| 2024年12月 | **Sora正式對外開放** | ChatGPT Plus/Pro用戶可使用文生影片功能（美加地區）。 |

## 五、推理與全模態整合期（2025）

| 時間 | 事件 | 說明 |
|---|---|---|
| 2025年1月31日 | **o3-mini發布** | 輕量推理模型，兼顧速度與推理能力。 |
| 2025年2月27日 | **GPT-4.5發布（研究預覽）** | 更大規模的對話模型預覽版。 |
| 2025年3月25日 | **GPT-4o原生圖像生成** | 圖像生成能力原生整合進GPT-4o，不再依賴獨立DALL·E呼叫。 |
| 2025年4月 | **GPT-4.1發布 / o3、o4-mini發布** | GPT-4.1聚焦程式撰寫、指令遵循與長文本；o3/o4-mini強化推理能力。 |
| 2025年8月7日 | **GPT-5發布** | 整合快速模型＋深度推理模型＋自動路由機制於單一系統，取代GPT-4o成為ChatGPT預設模型，是推理與多模態能力的全面整合版本。 |

## 重點整理摘要（考試用）

- **Transformer（2017）** 是所有LLM的技術基礎，核心為「自注意力機制」，可平行運算。
- **GPT系列演進**：GPT-1（2018）→ GPT-2（2019）→ GPT-3（2020，規模化里程碑）→ GPT-3.5/ChatGPT（2022，應用爆紅）→ GPT-4（2023，首個多模態）→ GPT-4o（2024，全模態即時互動）→ GPT-5（2025，推理+多模態整合）。
- **多模態三支線**：
  - 圖像：DALL·E（2021）→ DALL·E 2（2022）→ DALL·E 3（2023）→ GPT-4o原生圖像生成（2025）
  - 語音：Whisper（2022，聽）→ ChatGPT語音對話（2023，說）→ GPT-4o即時語音（2024）
  - 影片：Sora（2024亮相，同年底開放）
- **生態系發展**：GPTs（2023.11，自訂AI助理）→ GPT Store（2024.1，應用商店化）
- **推理模型支線**：o1（2024.9）→ o3-mini（2025.1）→ o3/o4-mini（2025.4）→ 整合進GPT-5（2025.8）

## 資料來源

- [GPT-4o - Wikipedia](https://en.wikipedia.org/wiki/GPT-4o)
- [GPT-4 - Wikipedia](https://en.wikipedia.org/wiki/GPT-4)
- [OpenAI GPT Model Release Timeline](https://hidekazu-konishi.com/entry/openai_gpt_model_release_timeline.html)
- [Whisper (speech recognition system) - Wikipedia](https://en.wikipedia.org/wiki/Whisper_(speech_recognition_system))
- [GPT-5 - Wikipedia](https://en.wikipedia.org/wiki/GPT-5)
- [OpenAI o1 - Wikipedia](https://en.wikipedia.org/wiki/OpenAI_o1)
- [OpenAI o3 - Wikipedia](https://en.wikipedia.org/wiki/OpenAI_o3)
- [Sora (text-to-video model) - Wikipedia](https://en.wikipedia.org/wiki/Sora_(text-to-video_model))
- [GPT Store - Wikipedia](https://en.wikipedia.org/wiki/GPT_Store)
- [OpenAI Says ChatGPT Can Now See, Hear, And Speak](https://www.mediapost.com/publications/article/389566/None)
