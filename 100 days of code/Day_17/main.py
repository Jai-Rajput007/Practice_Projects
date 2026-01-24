from data import question_data
from question_model import Questions
from quiz_brain import Quiz_brain
Ques_bank = []
for ques in question_data:
    _text = ques["text"]
    _answer = ques["answer"]
    new_q = Questions(text=_text,answer=_answer)
    Ques_bank.append(new_q)

quiz = Quiz_brain(Ques_bank)

while quiz.still_has_ques():
    quiz.next_question()
