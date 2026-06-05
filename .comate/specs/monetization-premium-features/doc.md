# Pro 付费功能 - 功能设计文档

## 1. 需求概述

在现有代码截图工具基础上引入轻量级付费墙，核心逻辑：**核心功能免费，在关键便利性上收费**。

### 免费用户
- 10 个基础主题可用
- 导出 PNG 时自动叠加 **15% 透明度 "Made by CodeSnap" 水印**（水印只在导出图片中出现，预览区不可见）

### Pro 会员（一次性解锁 / 订阅制）
- **无水印导出**
- **解锁全部 50+ 主题**
- **自定义背景图**：支持上传本地图片作为预览卡片背景
- **自定义 Logo**：支持上传 Logo 图片显示在预览卡片角落

### 收款与激活
- 使用 **Lemon Squeezy** 支付链接收款
- 极简激活：用户付款后通过回调 URL 参数自动解锁 Pro 功能

---

## 2. 架构与技术方案

### 付费墙设计原则
- **无弹窗干扰**：免费用户正常使用所有功能，仅在导出时自动加水印、仅在切换付费主题时显示 "Pro" 标签
- **最小侵入性**：不阻塞免费用户体验，付费功能以 "解锁更多" 的方式自然引导
- **纯前端实现**：激活状态通过 `localStorage` 持久化（轻量级方案，适合个人工具）

### 激活机制（Lemon Squeezy）

```
用户点击 "Upgrade to Pro" 按钮
    ↓
打开 Lemon Squeezy 结账页面（带 redirect_url 参数）
    ↓
付款成功 → 浏览器跳转回应用首页 ?activated=success
    ↓
App.vue 挂载时检测 URL 参数
    ↓
localStorage.setItem('codesnap_pro', 'true')
    ↓
页面刷新，所有 Pro 功能解锁
```

**说明**：此方案为纯前端轻量级实现。Lemon Squeezy 结账页面的 `Redirect URL` 配置为应用地址。由于无后端，激活可被技术用户伪造，但对个人独立工具而言已足够。如需更高安全性，可后续接入 Lemon Squeezy Webhook + 后端验证。

### 状态管理

新增 `usePro.ts` composable：
- `isPro`：是否已激活 Pro（读取 localStorage）
- `activatePro()`：激活 Pro（写入 localStorage + 刷新页面）
- `checkActivationFromURL()`：检测 URL `?activated=success` 参数

### 水印方案

**关键设计**：水印不在 DOM 预览中显示，仅在导出阶段通过 Canvas API 绘制到导出的图片上。

```typescript
// 在 html2canvas 导出后，在 Canvas 上叠加水印
function drawWatermark(canvas: HTMLCanvasElement, text: string) {
  const ctx = canvas.getContext('2d')!;
  ctx.save();
  ctx.globalAlpha = 0.15;
  ctx.font = 'bold 24px system-ui, sans-serif';
  ctx.fillStyle = '#ffffff';
  ctx.textAlign = 'right';
  ctx.textBaseline = 'bottom';
  ctx.fillText(text, canvas.width - 24, canvas.height - 24);
  ctx.restore();
}
```

### 主题扩展

将 highlight.js 的 50+ 热门主题全部加入配置，标记每个主题为 `free` 或 `pro`。免费主题放前 10 个，其余标记为 Pro 专享。

### 自定义背景图 / Logo

- **背景图**：用户上传图片后，通过 `URL.createObjectURL()` 生成临时 URL，作为 PreviewCard 的背景层
- **Logo**：同理，用户上传图片后显示在预览卡片右上角（可调整位置）
- 上传通过 `<input type="file" accept="image/*">` 实现
- 图片数据通过 `localStorage` 或 `indexedDB` 持久化（base64 编码，限制 2MB）

---

## 3. 受影响文件

### 修改文件
| 文件 | 修改类型 | 说明 |
|------|---------|------|
| `src/App.vue` | 修改 | 挂载时检测 URL 激活参数；注入 Pro 状态到各组件 |
| `src/components/SettingsPanel.vue` | 修改 | 添加主题列表 Pro 标签、上传控件、Upgrade 按钮 |
| `src/components/PreviewCard.vue` | 修改 | 支持自定义背景图和 Logo 层 |
| `src/composables/useExport.ts` | 修改 | 导出时根据 Pro 状态决定是否绘制水印 |
| `src/themes/index.ts` | 修改 | 扩展为 50+ 主题，增加 `tier: 'free' \| 'pro'` 字段 |

### 新建文件
| 文件 | 说明 |
|------|------|
| `src/composables/usePro.ts` | Pro 状态管理（检测、激活、持久化） |
| `src/composables/useCustomAssets.ts` | 自定义背景图/Logo 的上传、预览、持久化 |
| `src/components/ProBadge.vue` | Pro 标签小组件（用于标记付费功能） |
| `src/components/UpgradeBanner.vue` | 顶部/设置区 Upgrade 引导横幅 |

---

## 4. 实现细节

### 4.1 usePro.ts - Pro 状态管理

```typescript
const PRO_KEY = 'codesnap_pro';

export function usePro() {
  const isPro = ref(false);

  onMounted(() => {
    // 从 localStorage 读取
    isPro.value = localStorage.getItem(PRO_KEY) === 'true';
    // 检测 URL 激活参数
    checkActivationFromURL();
  });

  function checkActivationFromURL() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('activated') === 'success') {
      activatePro();
      // 清理 URL 参数
      window.history.replaceState({}, '', window.location.pathname);
    }
  }

  function activatePro() {
    localStorage.setItem(PRO_KEY, 'true');
    isPro.value = true;
    window.location.reload();
  }

  return { isPro, activatePro };
}
```

### 4.2 水印导出（useExport.ts 改造）

```typescript
async function exportPNG(
  element: HTMLElement,
  scale: number = 2,
  options: { watermark?: string } = {}
) {
  const canvas = await html2canvas(element, { scale, backgroundColor: null });

  if (options.watermark) {
    drawWatermark(canvas, options.watermark);
  }

  // 下载...
}
```

### 4.3 主题列表改造

每个主题增加 `tier` 字段：
```typescript
export const themes: Record<string, ThemeConfig> = {
  dracula: { name: 'Dracula', url: '...', bg: '...', fg: '...', tier: 'free' },
  // ... 前 10 个免费
  'vs-2015': { name: 'VS 2015', url: '...', bg: '...', fg: '...', tier: 'pro' },
  // ... 其余 40+ 个标记为 pro
};
```

SettingsPanel 中：
- 免费主题正常可选
- Pro 主题显示锁图标 + "Pro" 标签，点击后弹出升级提示

### 4.4 自定义背景图与 Logo（useCustomAssets.ts）

```typescript
export function useCustomAssets() {
  const backgroundImage = ref<string>('');
  const logoImage = ref<string>('');

  function handleFileUpload(file: File, type: 'bg' | 'logo') {
    if (file.size > 2 * 1024 * 1024) {
      alert('Image must be smaller than 2MB');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      const base64 = e.target?.result as string;
      if (type === 'bg') {
        backgroundImage.value = base64;
        localStorage.setItem('codesnap_bg', base64);
      } else {
        logoImage.value = base64;
        localStorage.setItem('codesnap_logo', base64);
      }
    };
    reader.readAsDataURL(file);
  }

  onMounted(() => {
    backgroundImage.value = localStorage.getItem('codesnap_bg') || '';
    logoImage.value = localStorage.getItem('codesnap_logo') || '';
  });

  return { backgroundImage, logoImage, handleFileUpload };
}
```

### 4.5 PreviewCard 改造

在 `.preview-card` 内部增加背景层和 Logo 层：

```vue
<div ref="cardRef" class="preview-card" :style="cardStyle">
  <!-- 自定义背景图 -->
  <div v-if="backgroundImage" class="custom-bg" :style="{ backgroundImage: `url(${backgroundImage})` }"></div>
  
  <MacWindowFrame />
  <div class="code-content" :style="codeStyle">
    <pre><code class="hljs" v-html="highlightedCode"></code></pre>
  </div>
  
  <!-- 自定义 Logo -->
  <img v-if="logoImage" class="custom-logo" :src="logoImage" />
</div>
```

### 4.6 Upgrade 引导设计

- **SettingsPanel 中**：在主题选择器旁显示 "Unlock 50+ themes" 提示；导出按钮区域显示水印提示
- **顶部 Banner（可选）**：免费用户看到 "Upgrade to Pro for watermark-free exports & 50+ themes"
- **点击行为**：打开 Lemon Squeezy 支付链接（`window.open(LEMON_SQUEEZY_URL, '_blank')`）

### 4.7 Lemon Squeezy 配置指南（文档说明）

用户需要在 Lemon Squeezy 中：
1. 创建 Product（如 "CodeSnap Pro"）
2. 获取 Checkout URL（如 `https://codesnap.lemonsqueezy.com/checkout/buy/xxxxx`）
3. 在 Product 设置中配置 `Redirect after purchase` 为应用部署地址 + `?activated=success`
4. 将 Checkout URL 硬编码到应用代码中（或作为环境变量）

---

## 5. 边界条件与异常处理

| 场景 | 处理策略 |
|------|---------|
| 免费用户选择 Pro 主题 | 自动回退到最近的免费主题，显示升级提示 Toast |
| 用户清除浏览器数据 | Pro 状态丢失，需要重新激活（这是纯前端方案的固有局限） |
| 上传图片超过 2MB | 拒绝上传，提示压缩图片 |
| html2canvas 导出失败 | 原有错误处理，不影响功能 |
| URL 参数被伪造激活 | 接受，纯前端方案无法避免，后续可接入后端验证 |
| 自定义背景图与代码可读性冲突 | 背景图默认添加深色遮罩层保证代码可读 |

---

## 6. 数据流

```
App.vue 挂载
    ↓
usePro.ts 读取 localStorage + 检测 URL 参数
    ↓
[isPro = false]                     [isPro = true]
    ↓                                   ↓
免费体验全部功能                    解锁全部功能
导出时 canvas 绘制水印              导出时无水印
Pro 主题显示锁图标                  所有主题可用
设置面板显示 Upgrade 按钮           设置面板显示 Pro badge
    ↓
用户点击 Upgrade → 打开 Lemon Squeezy
    ↓
付款成功 → 跳转回 ?activated=success
    ↓
usePro.ts 检测到参数 → activatePro() → 页面刷新
```

---

## 7. 品牌名

当前使用占位品牌名 **"CodeSnap"**。如用户有指定品牌名，全局替换即可。

---

## 8. 预期结果

### 功能验证
- [ ] 免费用户导出图片带 "Made by CodeSnap" 水印（15% 透明度，右下角）
- [ ] Pro 用户导出图片无水印
- [ ] 主题列表正确区分免费/Pro，Pro 主题有锁图标
- [ ] 免费用户点击 Pro 主题自动回退并提示升级
- [ ] 支持上传自定义背景图，预览和导出均生效
- [ ] 支持上传自定义 Logo，预览和导出均生效
- [ ] 用户付款后通过 URL 回调自动激活 Pro
- [ ] Pro 状态通过 localStorage 持久化

### UI 效果
- 免费用户界面自然引导升级，无强干扰弹窗
- Pro 功能以 subtle 的锁图标/标签标识
- Upgrade 按钮醒目但不突兀
