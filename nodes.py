import json
import os
import requests
import torch
import folder_paths
from server import PromptServer
from aiohttp import web

# 尝试导入aiohttp，如果失败则使用同步方式
try:
    import aiohttp
    import asyncio
    HAS_AIOHTTP = True
except ImportError:
    HAS_AIOHTTP = False

class DeepSeekPromptAssistant:
    """
    DeepSeek API提示词优化助手节点
    使用火山引擎的DeepSeek模型优化AI绘画提示词
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": "一个女孩在樱花树下",
                    "placeholder": "输入您想要优化的简短描述..."
                }),
                "role_setting": ("STRING", {
                    "multiline": True,
                    "default": "你是一位专业的AI绘画提示词生成专家，精通Stable Diffusion、Midjourney、DALL-E等AI绘画工具。请根据用户输入生成高质量、详细、富有创意的英文AI绘画提示词。提示词应包含：主体描述、环境背景、艺术风格、构图、光线、色彩、细节描述等要素。使用逗号分隔关键词，确保提示词结构清晰、层次分明。",
                    "placeholder": "输入角色设定..."
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "输入火山引擎API密钥"
                }),
                "endpoint": ("STRING", {
                    "multiline": False,
                    "default": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                    "placeholder": "API端点URL"
                }),
                "model": ("STRING", {
                    "multiline": False,
                    "default": "deepseek-v3-2-251201",
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 1000,
                    "min": 100,
                    "max": 2000,
                    "step": 100
                }),
                "creative_level": (["standard", "creative", "detailed"], {
                    "default": "detailed"
                }),
            },
            "optional": {
                "preset_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "可选：预设的提示词模板"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("optimized_prompt",)
    FUNCTION = "optimize_prompt"
    CATEGORY = "DeepSeek_API"
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = {}
        else:
            self.config = {}
    
    def save_config(self, api_key, endpoint):
        """保存配置到文件"""
        self.config['api_key'] = api_key
        self.config['endpoint'] = endpoint
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def optimize_prompt(self, text, role_setting, api_key, endpoint, model, 
                       temperature, max_tokens, creative_level, preset_prompt=""):
        """
        调用DeepSeek API优化提示词
        """
        # 如果没有提供api_key，尝试从配置加载
        if not api_key and 'api_key' in self.config:
            api_key = self.config.get('api_key', '')
        
        if not endpoint and 'endpoint' in self.config:
            endpoint = self.config.get('endpoint', endpoint)
        
        if not api_key:
            return ("错误：请提供火山引擎API密钥",)
        
        # 根据创意级别调整提示词要求
        creative_settings = {
            "standard": "生成标准、实用的提示词",
            "creative": "生成富有创意和想象力的提示词",
            "detailed": "生成极其详细、包含丰富细节的提示词"
        }
        
        creative_instruction = creative_settings.get(creative_level, "生成详细提示词")
        
        # 构建系统提示
        system_prompt = f"""{role_setting}

要求：
1. {creative_instruction}
2. 使用英文输出（除非用户特别要求其他语言）
3. 输出格式：纯文本，包含完整提示词
4. 结构：主体描述、环境、风格、光照、色彩、细节、质量标签
5. 如果用户输入是中文，请先理解其含义，然后生成英文提示词

示例输出格式：
[主体详细描述], [环境背景], [艺术风格], [构图], [光线效果], [色彩调性], [细节特征], [质量标签如masterpiece, best quality, 8K]

现在请根据以下描述生成提示词："""
        
        # 构建用户输入
        user_input = text
        if preset_prompt:
            user_input = f"{text}\n\n参考预设风格：{preset_prompt}"
        
        # 构建API请求数据
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        try:
            # 发送API请求
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                optimized_prompt = result['choices'][0]['message']['content'].strip()
                
                # 清理可能的Markdown格式
                optimized_prompt = optimized_prompt.replace('```', '').replace('prompt', '').strip()
                
                # 保存配置
                self.save_config(api_key, endpoint)
                
                return (optimized_prompt,)
            else:
                error_msg = f"API请求失败: {response.status_code} - {response.text}"
                return (f"错误: {error_msg}",)
                
        except requests.exceptions.Timeout:
            return ("错误: API请求超时",)
        except requests.exceptions.RequestException as e:
            return (f"错误: 网络请求失败 - {str(e)}",)
        except Exception as e:
            return (f"错误: {str(e)}",)
    
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 总是重新执行节点，因为每次都需要调用API
        return float("nan")

class DeepSeekConfigNode:
    """
    DeepSeek API配置节点
    用于保存和加载API配置
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "输入火山引擎API密钥"
                }),
                "endpoint": ("STRING", {
                    "multiline": False,
                    "default": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
                }),
                "action": (["save", "load"], {
                    "default": "save"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("api_key", "endpoint")
    FUNCTION = "manage_config"
    CATEGORY = "DeepSeek_API"
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
    
    def manage_config(self, api_key, endpoint, action):
        if action == "save":
            # 保存配置
            config = {
                "api_key": api_key,
                "endpoint": endpoint
            }
            try:
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                return (api_key, endpoint)
            except Exception as e:
                return (f"保存失败: {str(e)}", endpoint)
        else:
            # 加载配置
            try:
                if os.path.exists(self.config_file):
                    with open(self.config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    return (config.get('api_key', ''), config.get('endpoint', endpoint))
                else:
                    return (api_key, endpoint)
            except:
                return (api_key, endpoint)

class DeepSeekPromptEnhancer:
    """
    DeepSeek提示词增强节点
    在已有提示词基础上进行优化增强
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "输入基础提示词..."
                }),
                "enhancement_type": (["add_details", "improve_structure", "add_style", "translate_zh2en"], {
                    "default": "add_details"
                }),
                "api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                }),
            },
            "optional": {
                "custom_instruction": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "自定义增强指令（可选）..."
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_prompt",)
    FUNCTION = "enhance_prompt"
    CATEGORY = "DeepSeek_API"
    
    def enhance_prompt(self, base_prompt, enhancement_type, api_key, custom_instruction=""):
        # 如果没有提供api_key，尝试从配置加载
        config_file = os.path.join(os.path.dirname(__file__), "config.json")
        if not api_key and os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    api_key = config.get('api_key', '')
            except:
                pass
        
        if not api_key:
            return ("错误：请提供API密钥",)
        
        # 根据增强类型设置系统提示
        enhancement_instructions = {
            "add_details": "你是一个AI绘画提示词专家。请为以下提示词添加更多细节描述，包括但不限于：材质纹理、光影效果、环境氛围、人物表情动作等。保持原有结构，只做增强。输出增强后的完整英文提示词。",
            "improve_structure": "你是一个AI绘画提示词优化专家。请优化以下提示词的结构，使其更加清晰、有条理，遵循：主体->环境->风格->构图->光线->色彩->细节->质量标签的顺序。输出优化后的完整英文提示词。",
            "add_style": "你是一个艺术风格专家。请为以下提示词添加或强化艺术风格描述，可以考虑添加：艺术家风格、艺术运动、绘画技法等。输出增强后的完整英文提示词。",
            "translate_zh2en": "你是一个专业的翻译和AI绘画提示词专家。请将以下中文提示词翻译并优化为专业的英文AI绘画提示词，确保符合Stable Diffusion的最佳实践。输出优化后的英文提示词。"
        }
        
        system_prompt = enhancement_instructions.get(enhancement_type, "")
        if custom_instruction:
            system_prompt = custom_instruction
        
        endpoint = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        
        payload = {
            "model": "deepseek-v3-2-251201",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": base_prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 800
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                enhanced_prompt = result['choices'][0]['message']['content'].strip()
                enhanced_prompt = enhanced_prompt.replace('```', '').replace('prompt', '').strip()
                return (enhanced_prompt,)
            else:
                return (f"错误: API请求失败 - {response.status_code}",)
                
        except Exception as e:
            return (f"错误: {str(e)}",)

# 节点注册
NODE_CLASS_MAPPINGS = {
    "DeepSeekPromptAssistant": DeepSeekPromptAssistant,
    "DeepSeekConfigNode": DeepSeekConfigNode,
    "DeepSeekPromptEnhancer": DeepSeekPromptEnhancer,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DeepSeekPromptAssistant": "DeepSeek 提示词助手",
    "DeepSeekConfigNode": "DeepSeek API 配置",
    "DeepSeekPromptEnhancer": "DeepSeek 提示词增强",
}