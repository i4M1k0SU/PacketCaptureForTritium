# Packet Capture For Tritium

Tshark runner for Tritium board

## Setup

```bash
sudo apt install -y tshark
pip install -r requirements.txt
cp .env.sample .env
vi .env # Edit .env
```

## Usage

```bash
./app.py
```

## これは何

- Tritium ( https://www.loverpi.com/collections/tritium ) という謎のシングルボードコンピュータ用のtsharkランナー
    - Raspberry Piで動くかはわかりません
- 作ったのは昔なので何も覚えていない
- app.pyを実行すると30秒後にtsharkを実行し、Ethernetのパケットをキャプチャする
    - Systemdを使ってOS起動時に自動でキャプチャを開始することを想定していた模様
- GPIOに接続したボタンを押すとキャプチャを終了し、OSをシャットダウンする
