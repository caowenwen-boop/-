#!/usr/bin/env python3
"""Google スプレッドシート操作ツール（サービスアカウント + gspread）

⚠️ セキュリティ：鍵ファイル(JSON)は「パスワード」と同じ。
   git / GitHub / 公開リンク等には絶対に置かないこと。
   このスクリプトは鍵の中身を表示・保存しません。

使い方:
  pip install gspread google-auth

  # 1) 接続テスト＋アクセス可能なシート数を確認
  python scripts/gsheet_tool.py test --key ~/.config/gcp/china-ec-sa.json

  # 2) 既存スプレッドシートにタブを追加
  python scripts/gsheet_tool.py add-tab \
      --key ~/.config/gcp/china-ec-sa.json \
      --sheet-id 11J1FBQsEQAPtdlQTljBcZ9ql-XgFby6BsSC7Lqu9bIs \
      --tab "ブンブンテスト"
"""
import argparse
import os
import sys


def get_client(key_path: str):
    import gspread
    key_path = os.path.expanduser(key_path)
    if not os.path.exists(key_path):
        sys.exit(f"❌ 鍵ファイルが見つかりません: {key_path}")
    return gspread.service_account(filename=key_path)


def cmd_test(args):
    gc = get_client(args.key)
    files = gc.list_spreadsheet_files()  # SA がアクセスできるスプレッドシート一覧
    print(f"✅ 接続成功。ロボットがアクセスできるスプレッドシート数: {len(files)}")
    for f in files[:20]:
        print(f"  - {f.get('name')}  (id={f.get('id')})")
    if len(files) > 20:
        print(f"  ... 他 {len(files) - 20} 件")
    if len(files) == 0:
        print("ℹ️ 0 件の場合：対象シートを、サービスアカウントのメール宛に"
              "『編集者』で共有できているか確認してください。")


def cmd_add_tab(args):
    gc = get_client(args.key)
    sh = gc.open_by_key(args.sheet_id)
    titles = [ws.title for ws in sh.worksheets()]
    print("既存タブ:", titles)
    if args.tab in titles:
        print(f"⚠️ 既に『{args.tab}』が存在します。追加しません。")
        return
    sh.add_worksheet(title=args.tab, rows=args.rows, cols=args.cols)
    print(f"✅ タブ『{args.tab}』を追加しました。")


def main():
    ap = argparse.ArgumentParser(description="Google Sheets tool (service account)")
    sub = ap.add_subparsers(dest="action", required=True)

    p_test = sub.add_parser("test", help="接続テスト＋アクセス可能シート数")
    p_test.add_argument("--key", required=True)
    p_test.set_defaults(func=cmd_test)

    p_add = sub.add_parser("add-tab", help="タブ(シート)を追加")
    p_add.add_argument("--key", required=True)
    p_add.add_argument("--sheet-id", required=True)
    p_add.add_argument("--tab", required=True)
    p_add.add_argument("--rows", type=int, default=100)
    p_add.add_argument("--cols", type=int, default=20)
    p_add.set_defaults(func=cmd_add_tab)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
