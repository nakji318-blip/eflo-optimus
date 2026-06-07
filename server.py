#!/usr/bin/env python3
"""
EFLO Optimus — Render.com 本番サーバー
・静的ファイル（HTML/CSS/JS）の配信
・Anthropic APIへのプロキシ（CORS回避）
"""

import os
import json
import urllib.request
import urllib.error
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── 設定 ──────────────────────────────────────────────
# APIキーは環境変数から取得（Renderのダッシュボードで設定）
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
API_URL = "https://api.anthropic.com/v1/messages"
API_VER = "2023-06-01"
PORT    = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ─────────────────────────────────────────────────────

app = Flask(__name__, static_folder=BASE_DIR)
CORS(app)

# ── トップページ ──────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

# ── 静的ファイル配信 ──────────────────────────────────
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(BASE_DIR, filename)

# ── APIプロキシ ────────────────────────────────────────
@app.route("/api/claude", methods=["POST", "OPTIONS"])
def proxy():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    if not API_KEY:
        return jsonify({"error": {"message": "APIキーが設定されていません。Renderの環境変数 ANTHROPIC_API_KEY を確認してください。"}}), 500

    try:
        body = request.get_data()
        req = urllib.request.Request(
            API_URL,
            data=body,
            headers={
                "Content-Type":      "application/json",
                "x-api-key":         API_KEY,
                "anthropic-version": API_VER,
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=60) as res:
            return app.response_class(
                response=res.read(),
                status=res.status,
                mimetype="application/json"
            )

    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(f"[API Error] {e.code}: {err[:300]}")
        return jsonify({"error": {"message": err}}), e.code

    except Exception as e:
        print(f"[Server Error] {e}")
        return jsonify({"error": {"message": str(e)}}), 500

# ── ヘルスチェック（Render.com監視用） ────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok", "api_key_set": bool(API_KEY)}), 200

# ── 起動 ──────────────────────────────────────────────
if __name__ == "__main__":
    print(f"EFLO Optimus サーバー起動: port={PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=False)
