from math import ceil


class Myblock:

    def __init__(self, pageperblock,  nowpage, p):

        # 표시할 페이지 갯수
        self.pageperblock = pageperblock

        # 전체 페이지 수
        self.totalpages = p.num_pages

        # 전체 블록 수
        self.totalblocknums = ceil(float(self.totalpages) / self.pageperblock)

        # 현재 블록
        self.currentblock = ceil(float(nowpage) / pageperblock)

        # 현재 블록 시작 페이지
        self.blockstartpage = ((self.currentblock-1) * pageperblock) + 1

        # 현재 블록 마지막 페이지
        self.blockendpage = self.totalpages if self.totalblocknums == self.currentblock \
            else (self.blockstartpage + (self.pageperblock-1))

        # 현재 블록 페이지 범위
        self.range = range(self.blockstartpage, self.blockendpage+1)

        # 이전 블록 존재 여부
        self.hasprevious = p.page(self.blockstartpage).has_previous()

        # 다음 블록 존재 여부
        self.hasnext = p.page(self.blockendpage).has_next()

    def __str__(self):
        return f'<Mybolck> (pageperblock: {self.pageperblock}, totalblocknums: {self.totalblocknums},' \
            f' currentblock: {self.currentblock}, blockstartpage: {self.blockstartpage}, ' \
            f' blockendpage: {self.blockendpage}, range: {self.range},' \
            f' hasprevious: {self.hasprevious}, hasnext:{self.hasnext})'

