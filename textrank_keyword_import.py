from konlpy.tag import Kkma, Komoran
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import numpy as np
from collections import Counter, defaultdict
from scipy.sparse import csr_matrix

#text = "법원 보류 명령에도 美상무 지명자 재검토할 필요 있다 삼성전자·SK하이닉스, 일정 차질 전망…예의 주시 중(서울=연합뉴스) 강태우 기자 = 미국 도널드 트럼프 행정부의 보조금 및 대출금 지출 일시 중단 조치가 법원 개입으로 제동이 걸린 가운데, 삼성전자와 SK하이닉스 등 국내 반도체 업계의 긴장감이 커지고 있다. 이미 한국 업체들이 조 바이든 전 대통령 임기 막바지에 보조금 계약을 마친 상태이지만, 트럼프 행정부 측이 그 내용을 검토하기 전에는 보조금 지급을 장담할 수 없다는 입장을 밝히고 나섰기 때문이다. 도널드 트럼프 대통령[AP=연합뉴스]    30일 업계에 따르면 트럼프 행정부의 산업·무역 정책을 총괄할 하워드 러트닉 상무부 장관 지명자는 29일(현지시간) 상원 인사청문회에서 반도체법 보조금을 받기로 미국 정부와 확정한 계약을 이행(honor)하겠냐는 질문에 말할 수 없다. 내가 읽지 않은 무엇을 이행할 수 없다고 답했다.    그는 반도체법을 반도체 제조를 다시 미국으로 가져오기 위한 우리의 능력에 대한 훌륭한 착수금이라고 평가하면서도 우리가 그것들을 검토해 제대로 할 필요가 있다고 생각한다고 말했다.  앞서 배스 백악관 예산관리국(OMB) 국장 대행은 지난 28일(현지시간) 각 정부 기관에 보낸 메모에서 반도체(CHIPS) 인센티브 프로그램, 청정 차량을 위한 세액 공제, 첨단 제조·생산 세액 공제 등이 포함된 연방 차원의 보조금 및 대출금 지출을 잠정 중단한다고 밝혔다.    트럼프 행정부의 국정 운영 기조에 맞지 않는 전임 바이든 행정부 사업 등을 걸러낸다는 취지다.    이에 대해 워싱턴DC 연방법원은 28일 보류 명령을 내리며 제동을 걸었고, 이날 백악관은 연방 차원의 보조금 및 대출금 집행 잠정 중단 지시 문서를 철회했다.    다만 DEI(다양성·공평성·포용성) 이니셔티브와 기후 변화 등과 관련한 연방 차원의 지출을 겨냥한 도널드 트럼프 대통령의 행정명령은 여전히 유효하다는 게 백악관의 설명이다.    아직 지켜봐야 할 부분이 남은 상황이지만 연방 자금 집행 중단 조치에 대한 트럼프 대통령의 의지가 큰 만큼 이 조치가 현실화하는 것을 완전히 배제할 수는 없다는 게 업계 안팎의 시각이다.    앞서 트럼프 대통령은 후보 시절부터 보조금이나 저리 대출 등의 혜택을 제공하는 바이든 행정부의 입법 성과인 인플레이션 감축법(IRA)과 반도체법에 부정적인 입장을 여러 차례 밝혀왔다. 삼성전자 미국 텍사스주 공장[AFP 연합뉴스 자료사진. 재판매 및 DB 금지]    이번 조치가 시행되면 IRA 등에 따라 한국 기업들이 받게 돼 있는 세액 공제 혜택과 대출금, 미국에 대규모 설비투자를 추진 중인 삼성전자와 SK하이닉스 등 한국 반도체 기업들이 반도체법에 따라 받게 돼 있는 보조금 등에도 영향이 있을 수 있다는 관측이다.    이미 지급이 결정된 수천억 원∼수조 원 규모의 보조금이 줄면 공장 착공 및 생산 지연 등 기존에 세워둔 일정에 차질이 빚어질 수밖에 없다. 이에 따라 삼성전자와 SK하이닉스도 현 상황에 촉각을 곤두세우는 모습이다.    반도체 업계 관계자는 아직 구체적으로 상황이 나온 것은 아니지만 계속해서 (트럼프 행정부의 움직임을) 예의주시하고 있다고 말했다.    삼성전자는 미국 텍사스주 테일러시에 파운드리(반도체 위탁생산) 공장을 짓기 위해 370억 달러 이상의 최종 투자 규모를 결정하고, 작년 12월 20일 미국 상무부와 47억4천500만 달러(약 6조9천억원)의 직접 보조금을 지급하는 계약을 최종 체결했다.    삼성전자는 이를 토대로 첨단 미세공정 개발, 테일러 공장 건설, 고객 유치 등에 박차를 가해 2026년 테일러 공장 가동 준비에 차질이 없도록 한다는 방침도 세웠다.    파운드리 시장 2위인 삼성전자의 테일러 공장은 업계 1위 대만 TSMC와의 격차를 줄이고, 후발 주자인 중국 업체들을 따돌리기 위한 중요한 생산거점으로 기대를 모으고 있다. SK하이닉스 미국 투자계획 발표행사 참석한 주미대사(워싱턴=연합뉴스) 조현동 주미대사가 3일(현지시간) 미국 인디애나주 웨스트 라파예트에 위치한 퍼듀 대학에서 개최된 SK하이닉스 투자 발표 행사에 참석해 축사하고 있다.     SK 하이닉스는 웨스트 라파예트 지역에 고대역폭 메모리(HBM)를 이용한 첨단 패키징 공장을 건설하고, 관련 연구개발(R&D)을 위한 투자를 예정하고 있다. 2024.4.4 [주미한국대사관 제공. 재판매 및 DB 금지] photo@yna.co.kr    인디애나주 웨스트라피엣에 인공지능(AI) 메모리용 어드밴스드 패키징 생산 기지를 건설하기로 한 SK하이닉스도 지난달 19일 미 상무부로부터 최대 4억5천800만 달러(약 6천639억원)의 직접 보조금 지급이 결정됐다.    인디애나 공장에서는 오는 2028년 하반기부터 차세대 고대역폭 메모리(HBM) 등 AI 메모리 제품이 양산될 예정이다.    TSMC는 총 650억 달러를 투자해 미국 애리조나주에 3개의 첨단 반도체 제조공장을 짓기로 하고, 66억 달러의 보조금을 받기로 했다. 이 중 첫 번째 공장은 4나노 칩 양산을 시작한 상태다.    업계에선 이미 기업들이 전임 정부로부터 보조금을 받았거나 트럼프 정부에서도 문제없이 받을 수 있을 것이라는 시각도 있다.    특히 TSMC는 이미 지난해에 보조금 일부를 먼저 받은 것으로 전해졌다. 삼성전자와 SK하이닉스의 지급 여부는 확인되지 않았다.    웬들 황 TSMC 최고재무책임자(CFO)는 19일 미국 CNBC 방송과의 인터뷰에서 지난해 4분기에 이미 첫 번째 보조금으로 15억 달러를 받았다며 트럼프 정부에서도 보조금이 계속 들어올 것으로 예상한다고 말했다.    일각에서는 설사 보조금이 일시 집행 중단되더라도 한국의 대미 설비투자 및 고용 창출과 연계된 보조금 등은 해당 투자 지역을 지역구로 둔 여야 의원들의 입김으로 인해 복원될 수 있다는 기대 섞인 관측도 나온다.    burning@yna.co.kr"

kkma = Kkma()
tfidf = TfidfVectorizer()
cnt_vec = CountVectorizer()
komoran = Komoran()

def komoran_tokenizer(sentences):
    words = komoran.pos(sentences)
    words = [word for word, tag in words if tag in {'NNG', 'NNP', 'XR', 'VA', 'VV'}]    # 일반명사, 고유명사, 어근, 형용사, 동사
    return words

def scan_vocabulary(sents, min_count=2):
    counter = Counter(sent for sent in sents)
    counter = {w: c for w, c in counter.items() if c >= min_count}  # 빈도수 min_count 이상 단어만 선택
    idx_to_vocab = [w for w, _ in sorted(counter.items(), key=lambda x: -x[1])]  # 빈도수 기준 정렬
    vocab_to_idx = {vocab: idx for idx, vocab in enumerate(idx_to_vocab)}  # 단어 -> 인덱스 매핑
    
    return idx_to_vocab, vocab_to_idx

def text2sentences(text):
    sentences = kkma.sentences(text)
    return sentences


def dict_to_mat(d, n_rows, n_cols):
    rows, cols, data = [], [], []
    for (i, j), v in d.items():
        rows.append(i)
        cols.append(j)
        data.append(v)
    return csr_matrix((data, (rows, cols)), shape=(n_rows, n_cols))


def cooccurrence(tokens, vocab_to_idx, window=2, min_cooccurence=2):
    counter = defaultdict(int)
    
    for s, token_i in enumerate(tokens):
        vocabs = [vocab_to_idx[w] for w in token_i if w in vocab_to_idx]
        vocabs = [vocab_to_idx[w] for w in token_i if w in vocab_to_idx]
        n = len(vocabs)
        
        for i, v in enumerate(vocabs):
            b = max(0, i - window)  # 윈도우 범위 시작
            e = min(i + window + 1, n)  # 윈도우 범위 끝 (+1 해야 포함됨)
            
            for j in range(b, e):
                if i == j:
                    continue
                counter[(v, vocabs[j])] += 1
                counter[(vocabs[j], v)] += 1
    
    counter = {k: v for k, v in counter.items() if v >= min_cooccurence}
    n_vocabs = len(vocab_to_idx)
    
    return dict_to_mat(counter, n_vocabs, n_vocabs)


def pagerank(x, df=0.85, max_iter=30):
    assert 0 < df < 1

    # initialize
    A = normalize(x, axis=0, norm='l1')
    R = np.ones(A.shape[0]).reshape(-1,1)
    bias = (1 - df) * np.ones(A.shape[0]).reshape(-1,1)

    # iteration
    for _ in range(max_iter):
        R = df * (A * R) + bias

    return R

    
# main
# if __name__ == '__main__':
    
#     words = komoran_tokenizer(text)                                         # text -> 단어 (토크나이저)
#     idx_to_vocab, vocab_to_idx = scan_vocabulary(words)                     # 2번 이상 출현한 단어만 정렬
    
#     tokens = [komoran_tokenizer(sent) for sent in text2sentences(text)]     # text -> 문장 -> 단어(토크나이저)
#     g = cooccurrence(tokens, vocab_to_idx, window=2, min_cooccurence=2)     # window 범위로 cooccurence 가중치 설정
#     R = pagerank(g, df = 0.85, max_iter=30).reshape(-1)                     # RageRank 알고리즘
#     idxs = R.argsort()[-30:]                                                # PageRank 결과 상위 30개 정렬
#     keywords = [idx_to_vocab[idx] for idx in reversed(idxs)]                

#     print(keywords)

def textrank_keyword_main(text):
    words = komoran_tokenizer(text)                                         # text -> 단어 (토크나이저)
    idx_to_vocab, vocab_to_idx = scan_vocabulary(words)                     # 2번 이상 출현한 단어만 정렬
        
    tokens = [komoran_tokenizer(sent) for sent in text2sentences(text)]     # text -> 문장 -> 단어(토크나이저)
    g = cooccurrence(tokens, vocab_to_idx, window=2, min_cooccurence=2)     # window 범위로 cooccurence 가중치 설정
    R = pagerank(g, df = 0.85, max_iter=30).reshape(-1)                     # RageRank 알고리즘
    idxs = R.argsort()[-30:]                                                # PageRank 결과 상위 30개 정렬
    keywords = [idx_to_vocab[idx] for idx in reversed(idxs)]                

    return keywords
    