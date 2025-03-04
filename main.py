from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import aiohttp
import json
import ssl

@register("prompt_plus", "羽灯鬼", "Prompt Plus", "1.0.0","https://github.com/yudengghost/astrbot_plugin_prompt_plus")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    @filter.command("提示词")
    async def prompt(self, event: AstrMessageEvent):
        """使用AI模型生成回复的提示词命令"""
        # 获取用户消息
        user_message = event.message_str
        
        # 发送等待提示
        yield event.plain_result("收到了，请稍候🥸")
        
        try:
            # 准备请求数据
            data = {
                "prompt": "下面将会给出非常高级的图片描述，丰富这段文本的表现力并转化为保留较多关键信息的关键词组，按照画面质量描述与风格词汇、主体描述、细节描述的顺序以逗号分隔， 40 词左右，英文小写输出，合并为一行:" + user_message,
                "id": "0"
            }
            
            # 创建不验证SSL的客户端
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            # 发送请求
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
                async with session.post('https://prompt-gpt.deno.dev/ai', json=data) as response:
                    if response.status == 200:
                        result = await response.text()
                        yield event.plain_result(f"{result}")
                    else:
                        yield event.plain_result(f"请求失败，状态码：{response.status}")
        except Exception as e:
            logger.error(f"处理提示词命令时出错: {str(e)}")
            yield event.plain_result(f"抱歉，处理请求时出现错误: {str(e)}")
            # 打印详细错误信息到日志
            logger.error(f"详细错误信息: {e}", exc_info=True)
