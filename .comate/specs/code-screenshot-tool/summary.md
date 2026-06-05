# 代码截图工具 - 项目总结

## 完成情况

所有任务已顺利完成，项目构建通过。

## 实现功能

### 1. 代码编辑区
- 左侧带行号的代码编辑区
- 支持 Tab 键插入 2 空格缩进，Shift+Tab 减少缩进
- 行号与编辑器滚动同步
- 默认加载示例 JavaScript 代码

### 2. 实时预览卡片
- macOS 窗口样式，顶部有红黄绿三个圆点
- 实时显示语言标签
- 使用 highlight.js 进行语法高亮
- 代码编辑与预览实时同步

### 3. 设置面板
- **10 种主题切换**：Dracula、One Dark、Monokai、GitHub Dark、GitHub Light、Atom One Dark、Atom One Light、Solarized Dark、Solarized Light、Night Owl
- **内边距调整**：16px ~ 64px 滑块控制
- **圆角调整**：4px ~ 24px 滑块控制
- **字体大小调整**：12px ~ 24px 滑块控制
- **语言选择**：20 种编程语言支持

### 4. 一键导出
- 支持 1x / 2x / 4x 分辨率 PNG 导出
- 使用 html2canvas 精确捕获预览卡片区域
- 导出文件名包含分辨率标记

## 新增/修改文件

| 文件 | 类型 | 说明 |
|------|------|------|
| `package.json` | 修改 | 添加 highlight.js、html2canvas 依赖 |
| `index.html` | 修改 | 更新页面标题为 Code Screenshot |
| `src/style.css` | 重写 | 简化为基础全局样式 |
| `src/App.vue` | 重写 | 主布局：左右分栏 + 底部设置面板 |
| `src/components/CodeEditor.vue` | 新建 | 代码编辑区组件 |
| `src/components/PreviewCard.vue` | 新建 | 预览卡片组件 |
| `src/components/MacWindowFrame.vue` | 新建 | macOS 窗口顶部栏 |
| `src/components/SettingsPanel.vue` | 新建 | 设置面板组件 |
| `src/composables/useCodeEditor.ts` | 新建 | 代码编辑逻辑 |
| `src/composables/useSettings.ts` | 新建 | 设置状态管理 |
| `src/composables/useExport.ts` | 新建 | 导出逻辑封装 |
| `src/themes/index.ts` | 新建 | 主题与语言配置 |
| `src/components/HelloWorld.vue` | 删除 | 旧项目示例组件 |

## 技术栈

- Vue 3 + TypeScript + Vite
- highlight.js（语法高亮）
- html2canvas（DOM 转 PNG）
- Vue 3 Composition API + reactive

## 运行方式

```bash
yarn dev      # 启动开发服务器
yarn build    # 生产构建
```

## 布局说明

- **桌面端**：左右分栏布局，左侧编辑器，右侧预览
- **移动端**（≤900px）：上下堆叠布局
- 整体采用深色主题，与代码预览风格统一
