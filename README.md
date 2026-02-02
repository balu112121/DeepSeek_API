# DeepSeek API ComfyUI 插件

这个插件允许你在ComfyUI中通过火山引擎的DeepSeek API优化和生成AI绘画提示词。

## 功能特性

1. **提示词助手**：根据简短描述生成专业级AI绘画提示词
2. **API配置管理**：方便地保存和加载API配置
3. **提示词增强**：对已有提示词进行优化和增强
4. **中英翻译**：将中文描述翻译优化为英文提示词

## 安装方法

1. 将整个 `DeepSeek_API` 文件夹复制到 `ComfyUI/custom_nodes/` 目录下
2. 重启ComfyUI
3. 在节点菜单中找到 `DeepSeek_API` 分类

## 获取API密钥

1. 访问火山引擎控制台：https://console.volcengine.com/
2. 注册并登录账号
3. 在AI产品中找到DeepSeek服务
4. 创建API密钥并获取Endpoint

## 节点说明

### 1. DeepSeek 提示词助手
- **输入**: 
  - text: 简短描述文本
  - role_setting: 角色设定
  - api_key: 火山引擎API密钥
  - 其他参数：温度、token数量、创意级别等
- **输出**: 优化后的提示词文本

### 2. DeepSeek API 配置
- 用于保存和加载API配置
- 避免每次都需要输入API密钥

### 3. DeepSeek 提示词增强
- 对已有提示词进行细节增强
- 优化提示词结构
- 添加艺术风格描述
- 中英翻译优化

## 使用示例

1. 连接一个文本输入到 `DeepSeek提示词助手`
2. 输入你的简短描述，如："一个女孩在樱花树下"
3. 配置API密钥和参数
4. 执行工作流，获取优化后的专业提示词
5. 将输出的提示词连接到你的文本编码器节点

## 参数说明

- **temperature**: 控制生成随机性（0.0-1.0）
- **max_tokens**: 最大输出长度
- **creative_level**: 
  - standard: 标准提示词
  - creative: 创意型提示词
  - detailed: 详细描述型提示词

## 注意事项

1. 需要有效的火山引擎API密钥
2. 注意API调用次数限制和费用
3. 建议先在小规模测试后再进行批量处理
4. 生成的提示词可能需要根据实际效果微调

### 南光AIGC

南光AIGC-AIGC全能方案设计解决专家 VX:nankodesign2001

南光AIGC绘画 仙宫云新人注册网址---https://www.xiangongyun.com/register/MJAT43 新人注册仙宫云送5元代金券， 填写邀请码（输入我们的邀请码：MJAT43 ）还额外送3元代金券 完成后可以得到仙宫云8元账户余额，可以免费带你玩转5小时发高配4090 D显卡AIGC绘画。

https://istarry.com.cn/?sfrom=jbEHmC
StartAI PS插件，提供多种强大的AI功能，轻松提升设计效率，邀您免费体验，我的邀请码：jbEHmC，点击注册。

### 三大自媒体平台

小红书
https://www.xiaohongshu.com/user/profile/5fe63b41000000000100811d?m_source=itab

抖音
https://www.douyin.com/user/self?showTab=post

bilibili（B站）
https://space.bilibili.com/404783526


### 如果您受益于本项目，不妨请作者喝杯咖啡，您的支持是我最大的动力

<div style="display: flex; justify-content: left; gap: 20px;">
    <img src="https://github.com/balu112121/ComfyUI_NanKo_AI_Recognize/blob/main/Alipay.jpg" width="300" alt="支付宝收款码">
    <img src="https://github.com/balu112121/ComfyUI_NanKo_AI_Recognize/blob/main/WeChat.jpg" width="300" alt="微信收款码">
</div>

# 商务合作
如果您有定制工作流/节点的需求，或者想要学习插件制作的相关课程，请联系我
wechat:nankodesign2001
