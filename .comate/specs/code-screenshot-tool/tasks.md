# 代码截图工具 - 任务计划

- [ ] Task 1: 安装依赖并配置项目
    - 1.1: 安装 highlight.js 和 html2canvas
    - 1.2: 更新 index.html 页面标题
    - 1.3: 清理 src/style.css 保留基础样式

- [ ] Task 2: 创建核心逻辑 Composables
    - 2.1: 创建 useCodeEditor.ts（代码内容、行号、语言检测）
    - 2.2: 创建 useSettings.ts（主题、padding、radius、fontSize 状态管理）
    - 2.3: 创建 useExport.ts（html2canvas 封装、多分辨率导出）
    - 2.4: 创建 src/themes/index.ts（10 种主题配置映射）

- [ ] Task 3: 创建 UI 组件
    - 3.1: 创建 MacWindowFrame.vue（红黄绿三个圆点窗口顶部）
    - 3.2: 创建 CodeEditor.vue（带行号的代码编辑区）
    - 3.3: 创建 PreviewCard.vue（macOS 窗口 + 高亮代码预览）
    - 3.4: 创建 SettingsPanel.vue（主题选择、滑块控制、导出按钮）

- [ ] Task 4: 组装主应用并完善样式
    - 4.1: 重写 App.vue 为主布局（左右分栏 + 设置面板）
    - 4.2: 编写全局样式确保布局、主题、响应式正常
    - 4.3: 验证所有交互：编辑、主题切换、样式调整、导出
