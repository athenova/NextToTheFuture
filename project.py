from simple_blogger import CommonBlogger
from simple_blogger.generators.OpenAIGenerator import OpenAITextGenerator
from datetime import datetime
from datetime import timedelta
from simple_blogger.senders.TelegramSender import TelegramSender
from simple_blogger.senders.InstagramSender import InstagramSender

class Project(CommonBlogger):
    def _example_task_creator(self):
        return [
            {
                "problem": "problem",
                "technic": "technic",
                "description": "description",
                "group": "group"
            }
        ]

    def _get_category_folder(self, task):
        return f"{task['group']}/{task['technic']}"
                    
    def _get_topic_folder(self, task):
        return f"{task['problem']}"

    def _system_prompt(self, task):
        return "Ты - коуч будущего с передовыми техниками, нестандартными инсайтами и проверенными стратегиями, которые помогут твоим клиентам создать свою новую реальность"

    def _task_converter(self, idea):
        return { 
                    "group": idea['group'],
                    "technic": idea['technic'],
                    "problem": idea['problem'],
                    "description_prompt": f"Опиши проблему '{idea['problem']}' из области '{idea['group']}', не описывай решение, создай заголовок и выдели его одиночными обратными апострофами, сократи текст до тезизов 'Как было', 'Причины', 'Что сделано', 'Результат', используй не более {self.topic_word_limit} слов",
                    "description_image": f"Нарисуй рисунок, вдохновлённый проблемой '{idea['problem']}' из области '{idea['group']}'",
                    "solution_prompt": f"Опиши решение проблемы '{idea['problem']}' с помощью техники '{idea['technic']}' из области '{idea['group']}', создай заголовок и выдели его одиночными обратными апострофами, используй не более {self.topic_word_limit} слов",
                    "solution_image": f"Нарисуй рисунок, вдохновлённый темой '{idea['technic']}' из области '{idea['group']}'",
                }

    def __init__(self, **kwargs):
        super().__init__(
            first_post_date=datetime(2025, 2, 24),
            text_generator=OpenAITextGenerator(),
            topic_word_limit=300,
            days_between_posts=timedelta(days=3),
            reviewer=TelegramSender(channel_id=-1002312034777, send_text_with_image=False),
            senders=[TelegramSender(channel_id=f"@NextToTheFuture"), InstagramSender(channel_token_name='FUTUREUNLOCKED_OFFICIAL_TOKEN')],
            **kwargs
        )

    