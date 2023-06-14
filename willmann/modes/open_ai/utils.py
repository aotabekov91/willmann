import os
import time

import openai

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class AIAnswer(QObject):
    
    answered=pyqtSignal(str, str)
    def __init__(self, parent):
        super(AIAnswer, self).__init__()
        self.parent=parent
        self.question=None
        self.completion=openai.Completion(api_register=os.environ['OPEN_AI_API'])

    def loop(self):
        self.running=True

        while self.running:
            if self.question:
                answer=self.get_answer(self.question)
                self.answered.emit(self.question, answer)
            self.question=None
            time.sleep(1)

    def get_answer(self, question):

        try:

            r=self.completion.create(
                prompt=question,
                model='text-davinci-003',
                # up_p=0.1,
                max_tokens=3000)

            return r['choices'][0]['text']
        except:
            return 'Could not fetch an answer from OPENAI'
