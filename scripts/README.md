# scripts · 工具脚本

## gsheet_tool.py — Google 表格操作（服务账号 + gspread）

用服务账号密钥操作 Google 表格：测试连接 / 新增标签页。

### ⚠️ 密钥安全（重要）
- 密钥文件（如 `china-ec-sa.json`）**等同密码**，**绝不放进 git / GitHub / 公开链接**。
- 建议放在仓库外，例如 `~/.config/gcp/china-ec-sa.json`。
- 根目录 `.gitignore` 已忽略常见密钥文件名，双保险。
- 本脚本不会打印/保存密钥内容。

### 安装
```bash
pip install gspread google-auth
```

### 用法
```bash
# 1) 测试连接 + 列出机器人能访问的表格数量
python scripts/gsheet_tool.py test --key ~/.config/gcp/china-ec-sa.json

# 2) 给指定表格新增标签页
python scripts/gsheet_tool.py add-tab \
    --key ~/.config/gcp/china-ec-sa.json \
    --sheet-id 11J1FBQsEQAPtdlQTljBcZ9ql-XgFby6BsSC7Lqu9bIs \
    --tab "ブンブンテスト"
```

### 前提
- 目标表格需已「共享」给服务账号邮箱（`xxx@xxx.iam.gserviceaccount.com`），权限「编辑者」。
- `test` 返回数量为 0 时，多半是没共享给该服务账号邮箱。
