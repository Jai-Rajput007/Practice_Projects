
class Quiz_brain:
    def __init__(self,ques_list):
        self.question_num = 0
        self.ques_list = ques_list
        self.score = 0
    
    def next_question(self):
        current_ques = self.ques_list[self.question_num]
        self.question_num += 1
        user_ans = input(f"Q.{self.question_num}: {current_ques.text} (True/False) : ")
        self.check_ans(user_ans,current_ques.answer)

    def still_has_ques(self):
        return self.question_num <= len(self.ques_list)
    
    def check_ans(self,user_ans,corr_ans):
        if user_ans.lower() == corr_ans.lower():
            print("Right")
            self.score += 1
        else:
            print("Wrong")
            print(f"Correct ans is {corr_ans}")
        print(f"Correct ans was:{corr_ans}")
        print(f"Your current score is : {self.score}/{self.question_num}\n")