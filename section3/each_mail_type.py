from collections import defaultdict

class IntervieweUtility:
    @staticmethod
    def required_info_for_document_rejection(이름, 공고명, 몇차면접, 인터뷰날짜):
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = 이름
        required_info['금번_채용_공고명'] = 공고명
        return required_info
    
    @staticmethod
    def required_info_for_interview_rejection(이름, 공고명, 몇차면접, 인터뷰날짜):
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = 이름
        required_info['금번_채용_공고명'] = 공고명
        return required_info
    
    @staticmethod
    def required_info_for_first_interview(이름, 공고명, 몇차면접, 인터뷰날짜):
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = 이름
        required_info['금번_채용_공고명'] = 공고명
        required_info['몇차_채용인지'] = 몇차면접
        required_info['다음_인터뷰_날짜'] = 인터뷰날짜
        return required_info
    
    @staticmethod
    def required_info_for_second_interview(이름, 공고명, 몇차면접, 인터뷰날짜):
        required_info = defaultdict()
        required_info['이메일_받는_사람_이름'] = 이름
        required_info['금번_채용_공고명'] = 공고명
        required_info['몇차_채용인지'] = 몇차면접
        required_info['다음_인터뷰_날짜'] = 인터뷰날짜
        return required_info