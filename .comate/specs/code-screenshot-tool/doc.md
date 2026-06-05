# 代码截图工具 - 功能设计文档

## 1. 需求概述

开发一个代码截图工具，用户可以在左侧编辑代码，右侧实时预览带 macOS 窗口样式的代码卡片，支持主题切换和样式调整，并能一键导出为高分辨率 PNG 图片。

### 核心功能
1. **代码编辑区**：支持输入和编辑代码，实时语法高亮（基于 highlight.js）
2. **实时预览卡片**：模仿 macOS 窗口样式，顶部有红黄绿三个圆点控制按钮
3. **设置面板**：切换 10 种流行主题，调整内边距、圆角、字体大小
4. **一键导出**：将预览卡片精确导出为多 x 分辨率的 PNG 图片

---

## 2. 架构与技术方案

### 技术栈
- **框架**：Vue 3 + TypeScript + Vite（复用现有项目）
- **语法高亮**：highlight.js（支持 190+ 语言，30+ 内置主题）
- **图片导出**：html2canvas（DOM 转 Canvas，再转 PNG 下载）
- **状态管理**：Vue 3 Composition API + reactive（无需 Pinia/Vuex，组件级状态足够）

### 组件架构
```
App.vue
├── CodeEditor.vue          # 左侧：代码编辑区
├── PreviewCard.vue         # 右侧：macOS 风格预览卡片
│   └── MacWindowFrame.vue  # macOS 窗口顶部（红黄绿按钮）
└── SettingsPanel.vue       # 底部/侧边：设置面板
    └── ExportButton.vue    # 导出按钮
```

### Composables
```
useCodeEditor.ts  # 代码编辑逻辑（内容、语言检测）
useSettings.ts    # 设置状态管理（主题、padding、radius、fontSize）
useExport.ts      # 导出逻辑（html2canvas 封装、多分辨率导出）
```

### 主题系统
内置 10 种 highlight.js 主题：
1. Dracula
2. One Dark
3. Monokai
4. GitHub Dark
5. GitHub Light
6. Atom One Dark
7. Atom One Light
8. Solarized Dark
9. Solarized Light
10. Night Owl

主题切换通过动态加载 highlight.js CSS 文件实现。

---

## 3. 受影响文件

### 修改文件
| 文件 | 修改类型 | 说明 |
|------|---------|------|
| `package.json` | 修改 | 添加 `highlight.js` 和 `html2canvas` 依赖 |
| `src/App.vue` | 重写 | 替换现有内容为代码截图工具主布局 |
| `src/style.css` | 修改 | 保留基础样式，移除与旧项目相关的样式 |
| `index.html` | 修改 | 更新页面标题为 "Code Screenshot" |

### 新建文件
| 文件 | 说明 |
|------|------|
| `src/components/CodeEditor.vue` | 代码编辑区组件（textarea + 行号显示） |
| `src/components/PreviewCard.vue` | 预览卡片组件（macOS 窗口 + 高亮代码） |
| `src/components/MacWindowFrame.vue` | macOS 窗口顶部栏组件（红黄绿按钮） |
| `src/components/SettingsPanel.vue` | 设置面板组件（主题选择、滑块控制） |
| `src/composables/useCodeEditor.ts` | 代码编辑逻辑 composable |
| `src/composables/useSettings.ts` | 设置状态管理 composable |
| `src/composables/useExport.ts` | 导出逻辑 composable |
| `src/themes/index.ts` | 主题配置和映射 |

---

## 4. 实现细节

### 4.1 代码编辑区（CodeEditor.vue）

**设计**：
- 左侧显示行号，右侧是 textarea
- 使用 `tabindex` 支持 Tab 键缩进
- 实时同步到 PreviewCard

**核心代码**：
```vue
<template>
  <div class="code-editor">
    <div class="line-numbers">
      <div v-for="n in lineCount" :key="n">{{ n }}</div>
    </div>
    <textarea
      v-model="code"
      @keydown="handleKeydown"
      spellcheck="false"
    />
  </div>
</template>
```

**Tab 键处理**：
- Tab 键插入 2 个空格（而非跳转到下一个元素）
- Shift+Tab 减少缩进

### 4.2 预览卡片（PreviewCard.vue）

**设计**：
- 顶部 macOS 风格标题栏（红黄绿三个圆点）
- 中间代码区域，使用 highlight.js 语法高亮
- 背景色跟随主题变化

**核心代码**：
```vue
<template>
  <div ref="cardRef" class="preview-card" :style="cardStyle">
    <MacWindowFrame />
    <div class="code-content" v-html="highlightedCode" />
  </div>
</template>
```

### 4.3 macOS 窗口顶部（MacWindowFrame.vue）

**设计**：
- 三个圆点：红（#ff5f56）、黄（#ffbd2e）、绿（#27c93f）
- 可选：显示文件名或语言标签

### 4.4 设置面板（SettingsPanel.vue）

**控制项**：
| 设置项 | 控件 | 范围 | 默认值 |
|--------|------|------|--------|
| 主题 | 下拉选择 | 10 种 | Dracula |
| 内边距 | 滑块 | 16px ~ 64px | 32px |
| 圆角 | 滑块 | 4px ~ 24px | 12px |
| 字体大小 | 滑块 | 12px ~ 24px | 14px |
| 语言 | 下拉选择 | highlight.js 支持的语言 | auto |

### 4.5 导出逻辑（useExport.ts）

**实现**：
1. 使用 html2canvas 捕获预览卡片 DOM
2. 支持 1x / 2x / 4x 分辨率导出
3. 将 Canvas 转换为 PNG Blob 并触发下载

**核心代码**：
```typescript
async function exportPNG(scale: number = 2) {
  const canvas = await html2canvas(cardRef.value, {
    scale,
    backgroundColor: null,
    logging: false,
  });
  const link = document.createElement('a');
  link.download = `code-screenshot@${scale}x.png`;
  link.href = canvas.toDataURL('image/png');
  link.click();
}
```

### 4.6 主题系统

**实现方式**：
- 动态创建/切换 `<link>` 标签加载 highlight.js 主题 CSS
- 主题 CSS 从 CDN 加载（或本地 npm 包）
- 预览卡片背景色和文字色通过 CSS 变量映射

---

## 5. 边界条件与异常处理

| 场景 | 处理策略 |
|------|---------|
| 代码为空 | 预览区显示占位提示，导出按钮禁用 |
| 主题 CSS 加载失败 | 回退到默认主题，控制台输出警告 |
| html2canvas 导出失败 | 显示错误提示，建议用户重试 |
| 大文件（>1000 行） | 不做限制，但提示可能影响导出性能 |
| 浏览器不支持 Canvas | 优雅降级，隐藏导出按钮 |
| 移动端布局 | 采用上下布局替代左右布局 |

---

## 6. 数据流

```
用户输入代码
    ↓
CodeEditor.vue (textarea v-model)
    ↓
useCodeEditor.ts (code state)
    ↓
App.vue (props 传递)
    ↓
PreviewCard.vue (highlight.js 渲染)
    ↑
SettingsPanel.vue (theme/padding/radius/fontSize)
    ↓
useSettings.ts (settings state)
    ↓
导出按钮触发 useExport.ts
    ↓
html2canvas → Canvas → PNG 下载
```

---

## 7. 预期结果

### 功能验证
- [ ] 左侧输入代码，右侧实时同步并语法高亮
- [ ] macOS 窗口样式正确显示（红黄绿三个圆点）
- [ ] 切换 10 种主题时，预览卡片颜色正确变化
- [ ] 调整内边距、圆角、字体大小实时生效
- [ ] 导出 1x/2x/4x PNG 图片，清晰无模糊

### UI 效果
- 整体采用左右分栏布局（桌面端）
- 代码编辑区有行号显示
- 预览卡片有阴影和 macOS 窗口效果
- 设置面板简洁直观

### 性能
- 代码输入延迟 < 50ms（防抖 100ms 高亮渲染）
- 导出 2x 图片耗时 < 3s（常规代码量）
