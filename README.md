# EFLO Optimus — 警備業務 AI支援システム

株式会社イーフロ 中島誠一 管理責任者

## ツール一覧

| ツール | 説明 |
|---|---|
| Tool-01 現場AIBot | 7現場のマニュアルをAIが即答 |
| Tool-05 警備学校 | 新人隊員向けオンボーディング（v2.0） |

## Render.com デプロイ手順

1. このリポジトリをGitHubにpush
2. [Render.com](https://render.com) でNew Web Serviceを作成
3. GitHubリポジトリを接続
4. 環境変数 `ANTHROPIC_API_KEY` を設定
5. デプロイ完了 → 固定URLが発行される

## 環境変数

| 変数名 | 説明 |
|---|---|
| `ANTHROPIC_API_KEY` | AnthropicのAPIキー（Renderのダッシュボードで設定） |

## ローカル起動（開発用）

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-api03-...
python server.py
```

© 株式会社イーフロ
