# Pro 付费功能 - 任务计划

- [ ] Task 1: 创建 Pro 状态管理与激活逻辑
    - 1.1: 创建 usePro.ts（localStorage 持久化、URL 参数检测、激活函数）
    - 1.2: 在 App.vue 中集成 usePro，挂载时检测激活状态
    - 1.3: 添加 Lemon Squeezy 结账链接常量

- [ ] Task 2: 扩展主题系统为 50+ 并标记免费/Pro
    - 2.1: 在 ThemeConfig 中增加 tier: 'free' | 'pro' 字段
    - 2.2: 保留原有 10 个免费主题，新增 40+ Pro 主题
    - 2.3: 更新 useSettings.ts 支持按 tier 过滤主题

- [ ] Task 3: 实现水印导出机制
    - 3.1: 改造 useExport.ts，导出时通过 Canvas API 绘制水印
    - 3.2: App.vue 中将 isPro 状态传入导出流程，控制是否添加水印
    - 3.3: 验证免费用户导出带水印，Pro 用户导出无水印

- [ ] Task 4: 实现自定义背景图与 Logo 上传
    - 4.1: 创建 useCustomAssets.ts（文件上传、base64 持久化、2MB 限制）
    - 4.2: 改造 PreviewCard.vue 支持自定义背景层和 Logo 层
    - 4.3: 背景图默认添加遮罩层保证代码可读性

- [ ] Task 5: 改造设置面板与 UI 引导
    - 5.1: 创建 ProBadge.vue 小组件（锁图标、Pro 标签）
    - 5.2: 改造 SettingsPanel.vue：主题列表显示 Pro 标签、Pro 主题点击回退并提示
    - 5.3: 在 SettingsPanel 中添加 Upgrade to Pro 按钮和文件上传控件
    - 5.4: 免费用户选择 Pro 主题时显示 Toast/提示引导升级

- [ ] Task 6: 创建 Upgrade 引导横幅
    - 6.1: 创建 UpgradeBanner.vue 组件
    - 6.2: 在 App.vue 中集成，免费用户可见，Pro 用户隐藏
    - 6.3: 点击跳转 Lemon Squeezy 结账页

- [ ] Task 7: 联调验证与构建
    - 7.1: 验证免费/Pro 状态下的所有交互路径
    - 7.2: 验证水印导出效果
    - 7.3: 验证主题解锁、自定义图片功能
    - 7.4: 运行 yarn build 确保无编译错误
