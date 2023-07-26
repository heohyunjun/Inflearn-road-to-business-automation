from collections import defaultdict

class IntervieweUtility:
    @staticmethod
    def required_info_for_document_rejection():
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = input("이메일 받는 사람 이름 :")
        required_info['금번_채용_공고명'] = input("채용 공고명")
        return required_info
    
    @staticmethod
    def required_info_for_interview_rejection():
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = input("이메일 받는 사람 이름 :")
        required_info['금번_채용_공고명'] = input("채용 공고명")
        return required_info
    
    @staticmethod
    def required_info_for_first_interview():
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = input("이메일 받는 사람 이름 :")
        required_info['금번_채용_공고명'] = input("채용 공고명: ")
        required_info['몇차_채용인지'] = input("몇차 채용인지 (1|2): ")
        required_info['다음_인터뷰_날짜'] = input("다음 인터뷰 날짜 : ")
        return required_info
    
    @staticmethod
    def required_info_for_second_interview():
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = input("이메일 받는 사람 이름 :")
        required_info['금번_채용_공고명'] = input("채용 공고명: ")
        required_info['몇차_채용인지'] = input("몇차 채용인지 (1|2): ")
        required_info['다음_인터뷰_날짜'] = input("다음 인터뷰 날짜 : ")
        return required_info