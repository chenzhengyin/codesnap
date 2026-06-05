# Pro 付费功能 - 项目总结

## 完成情况

所有任务已顺利完成，项目构建通过。

## 实现功能

### 1. 免费用户 vs Pro 会员

| 功能 | 免费用户 | Pro 会员 |
|------|---------|---------|
| 主题数量 | 10 个基础主题 | 全部 55 个主题 |
| 导出水印 | 15% 透明度 "Made by CodeSnap" 水印 | 无水印 |
| 自定义背景图 | ❌ | ✅ 上传本地图片 |
| 自定义 Logo | ❌ | ✅ 上传本地图片 |

### 2. 激活机制（Lemon Squeezy）

```
用户点击 "Upgrade to Pro" / "Unlock Pro — $9"
    ↓
打开 Lemon Squeezy 结账页面
    ↓
付款成功 → 跳转回应用 ?activated=success
    ↓
App.vue 检测到 URL 参数
    ↓
localStorage.setItem('codesnap_pro', 'true')
    ↓
页面自动刷新，Pro 功能解锁
```

### 3. 水印导出机制

- 水印 **不在 DOM 预览中显示**，仅在导出阶段通过 Canvas API 绘制
- 位于导出图片右下角，15% 透明度，白色文字
- 字体大小自适应画布尺寸

### 4. 自定义背景图 / Logo

- 通过 `<input type="file">` 上传，支持 base64 持久化到 localStorage
- 2MB 大小限制
- 背景图自动叠加 50% 黑色遮罩层保证代码可读性
- Logo 显示在预览卡片右下角

### 5. UI 引导设计

- **UpgradeBanner**：顶部横幅，免费用户可见，提示 Pro 优势
- **SettingsPanel**：
  - 主题选择器显示 Pro 锁图标，免费用户点击 Pro 主题触发升级
  - 导出按钮旁显示 "+ watermark" 提示或 Pro badge
  - 底部 "Unlock Pro — $9" 渐变色按钮
- **ProBadge**：锁图标/Pro 标签小组件，复用于多处
- **App Header**：Pro 用户显示紫色 "Pro" badge

---

## 新增/修改文件

| 文件 | 类型 | 说明 |
|------|------|------|
| `src/composables/usePro.ts` | 新建 | Pro 状态管理、URL 激活检测、localStorage 持久化 |
| `src/composables/useCustomAssets.ts` | 新建 | 背景图/Logo 上传、base64 持久化、2MB 限制 |
| `src/components/ProBadge.vue` | 新建 | Pro 标签/锁图标小组件 |
| `src/components/UpgradeBanner.vue` | 新建 | 顶部升级引导横幅 |
| `src/themes/index.ts` | 重写 | 55 个主题（10 免费 + 45 Pro），增加 tier 字段 |
| `src/components/SettingsPanel.vue` | 重写 | Pro 标签、上传控件、升级按钮、水印提示 |
| `src/components/PreviewCard.vue` | 修改 | 支持自定义背景层和 Logo 层 |
| `src/composables/useExport.ts` | 修改 | Canvas 水印绘制、isPro 控制 |
| `src/App.vue` | 修改 | 集成 Pro 状态、自定义资源、激活检测 |

---

## Lemon Squeezy 配置步骤

1. 在 Lemon Squeezy 创建 Product（如 "CodeSnap Pro"）
2. 获取 Checkout URL
3. 配置 `Redirect after purchase` 为应用部署地址 + `?activated=success`
4. 修改 `src/composables/usePro.ts` 中的 `LEMON_SQUEEZY_CHECKOUT_URL`
5. 如需调整价格，修改 `SettingsPanel.vue` 中的按钮文案

---

## 运行方式

```bash
yarn dev      # 启动开发服务器
yarn build    # 生产构建
```

---

## 安全说明

此实现为纯前端轻量级方案：
- Pro 激活状态存储在 localStorage，清除浏览器数据会丢失
- URL 参数激活可被技术用户伪造
- 适合个人独立工具，如需更高安全性可后续接入 Lemon Squeezy Webhook + 后端验证
