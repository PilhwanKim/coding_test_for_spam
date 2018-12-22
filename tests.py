from unittest import TestCase
import requests

import main


class MainTests(TestCase):
    def test_result(self):
        self.assertEqual(main.is_spam("spam spam http://bit.ly/2yTkW52", ["www.filekok.com"], 1), False)
        self.assertEqual(main.is_spam("spam spam http://bit.ly/2yTkW52", ["goo.gl"], 1), True)
        self.assertEqual(main.is_spam("spam spam http://bit.ly/2yTkW52", ["tvtv24.com"], 2), True)
        self.assertEqual(main.is_spam("spam spam http://bit.ly/2yTkW52", ["www.filekok.com"], 2), False)
        self.assertEqual(main.is_spam("spam spam http://bit.ly/2yTkW52", ["www.filekok.com"], 3), True)

    def test_extract_url_in_content(self):
        self.assertSetEqual(main.extract_url_in_content("spam spam http://bit.ly/2yTkW52"), {"http://bit.ly/2yTkW52",})
        self.assertSetEqual(main.extract_url_in_content("spam spam http://bit.ly/2yTkW52 spam http://www.filekok.com"),
                            {"http://bit.ly/2yTkW52", "http://www.filekok.com"})

    def test_get_redirected_url(self):
        resp = requests.get("http://bit.ly/2yTkW52")
        self.assertEqual(main.get_redirection_url(resp), ["https://goo.gl/nVLutc",
                                                          "http://tvtv24.com/view.php?id=intro&no=58&query="
                                                          "%EC%96%B4%EC%84%9C%EC%99%80!%20%ED%95%9C%EA%B5%AD%EC%9D%80"
                                                          "%20%EC%B2%98%EC%9D%8C%EC%9D%B4%EC%A7%80%20E09%20170921"])

        resp = requests.get("https://goo.gl/nVLutc")
        self.assertEqual(main.get_redirection_url(resp), ["http://tvtv24.com/view.php?id=intro&no=58&query="
                                                          "%EC%96%B4%EC%84%9C%EC%99%80!%20%ED%95%9C%EA%B5%AD%EC%9D%80"
                                                          "%20%EC%B2%98%EC%9D%8C%EC%9D%B4%EC%A7%80%20E09%20170921"])

    def test_count_redirection_depth(self):
        # 2단계 리다이렉트
        resp = requests.get("http://bit.ly/2yTkW52")
        count = main.count_redirection_depth(resp)
        self.assertEqual(count, 2)

        # 1단계 리다이렉트
        resp = requests.get("https://goo.gl/nVLutc")
        count = main.count_redirection_depth(resp)
        self.assertEqual(count, 1)

        # 리다이렉트 없음
        resp = requests.get("http://tvtv24.com/view.php?id=intro&no=58&query="
                                                          "%EC%96%B4%EC%84%9C%EC%99%80!%20%ED%95%9C%EA%B5%AD%EC%9D%80"
                                                          "%20%EC%B2%98%EC%9D%8C%EC%9D%B4%EC%A7%80%20E09%20170921")
        count = main.count_redirection_depth(resp)
        self.assertEqual(count, 0)

    def test_get_a_url_in_html(self):
        self.assertEqual(main.get_url_in_html(
            """
            <!doctype html>
                <html lang="ko">
                <head>
                <meta charset="utf-8">
                <meta http-equiv="imagetoolbar" content="no">
                <meta http-equiv="X-UA-Compatible" content="IE=10,chrome=1">
                <title>어서와! 한국은 처음이지 E09 170921</title>
                <link rel="stylesheet" href="http://tvtv24.com/css/intro_default.css">
                <!--[if lte IE 8]>
                <script src="http://tvtv24.com/js/html5.js"></script>
                <![endif]-->
                <script src="http://tvtv24.com/js/jquery-1.8.3.min.js"></script>
                <script type="text/javascript">
                var part_site = "http://bit.ly/2FdZqr2";
                var pop_type = "1";
                var msg01 = "무료 이용권이 지급되었습니다";
                var msg02 = "사용하실 아이디 간단히 등록해주세요";
                var msg03 = "";
                </script>
                <script type="text/javascript" src="http://tvtv24.com/js/intro.go.js"></script>
                
                </head>
                <body>
                <style>
                #top {background:#00008B;}
                </style>
                
                <div id="wrap">
                    <div id="top">
                        어서와! 한국은 처음이지 E09 170921 다운로드 << 3571분이 추천하였습니다. >>
                    </div>
                    <div id="head_info">
                        <table cellspacing="0" cellpadding="0" border="0" id="info_table">
                            <tr>
                                <th>번호</th>
                                <td width="358">
                                3884892				</td>
                                <th class="th2">등록자</th>
                                <td>
                                다올리자				</td>
                            </tr>
                            <tr>
                                <th>등록날짜</th>
                                <td>
                                2018-12-22				</td>
                                <th class="th2">평점</th>
                                <td>
                                    <img src="./img/avg_5.png" />
                                </td>
                            </tr>
                            <tr>
                                <th>다운수</th>
                                <td>
                                3279				</td>
                                <th class="th2">서버상태</th>
                                <td>
                                쾌적				</td>
                            </tr>
                        </table>
                    </div>
                        <div id="file_box">
                        <div class="file_div">
                            <table cellspacing="0" cellpadding="0" border="0" id="file_table">
                                <tr>
                                    <th width="30">&nbsp;</th>
                                    <th width="" class="subject">파일목록</th>
                                    <th width="80">내려받기</th>
                                </tr>
                                <tr>
                                    <td align="center" class="file_list"><input type="checkbox" name="file_check" id="file_check1" checked /></td>
                                    <td style="padding-left:5px;" class="file_list"><span class="file_01 onspan" onclick="javascript:is_login(part_site, pop_type, msg01, msg02);">어서와! 한국은 처음이지 E09 170921.HDTV.H264.720p-NEXT.mp4</span></td>
                                    <td align="center" class="file_list"><span class="btn_you onspan" onclick="javascript:is_login(part_site, pop_type, msg01, msg02);">다운로드</span></td>
                                </tr>
                                            </table>
                        </div>
                        <div class="clear"></div>
                    </div>
                    
                    <div id="main">
                        <div class="dn_btn">
                            <span class="onspan"><img src="./img/dn_btn_darkblue_3.png" onclick="javascript:is_login(part_site, pop_type, msg01, msg02, msg03);" /></span>
                        </div>
                        <div class="msgbox">
                            <div id="bo_v_con"><p align="center"> </p></div>
                        </div>
                
                        <a href="http://www.fileok.com"></a>
                        <a href="http://www.fileok2.com"></a>
                        <div id="comment">
                            <div class="cmt_msg">
                                톡톡튀는 댓글평을 달아주세요! 댓글은 당신의 얼굴입니다. 매너댓글 부탁~
                            </div>
                            <div class="cmt_write">
                                <input type="text" name="cmt_input" id="cmt_input" class="cmt_input" value=" 로그인 하시면 댓글을 작성 하실 수 있습니다." onclick="javascript:is_login(part_site, pop_type, msg01, msg02);" /><input type="submit" name="sbm_input" id="sbm_input" class="sbm_input" value="등록하기" onclick="javascript:is_login(part_site, pop_type, msg01, msg02);" />
                                <div class="clear"></div>
                            </div>
                            <div class="cmt_list">
                                <ul>
                                                    <li>
                                        <div class="cmt-icon"><img src="./img/cmt_0.gif" /></div>
                                        <div class="cmt-name">가을수</div>
                                        <div class="cmt-text"><span>우와...대박..감사히 잘보겠습니다~~</span></div>
                                        <div class="cmt-date">2018-12-22</div>
                                    </li>
                                                    <li>
                                        <div class="cmt-icon"><img src="./img/cmt_1.gif" /></div>
                                        <div class="cmt-name">황금열쇠</div>
                                        <div class="cmt-text"><span>오호 ㅎㅎ~^^ 대박 자료 감사합니다!!</span></div>
                                        <div class="cmt-date">2018-12-22</div>
                                    </li>
                                                    <li>
                                        <div class="cmt-icon"><img src="./img/cmt_2.gif" /></div>
                                        <div class="cmt-name">휴먼드림</div>
                                        <div class="cmt-text"><span>완전 강추!! 다른것들도 찾아봐야겠음.ㅋ</span></div>
                                        <div class="cmt-date">2018-12-22</div>
                                    </li>
                                                    <li>
                                        <div class="cmt-icon"><img src="./img/cmt_3.gif" /></div>
                                        <div class="cmt-name">다래랑</div>
                                        <div class="cmt-text"><span>댓글믿고 고고</span></div>
                                        <div class="cmt-date">2018-12-22</div>
                                    </li>
                                                    <li>
                                        <div class="cmt-icon"><img src="./img/cmt_4.gif" /></div>
                                        <div class="cmt-name">오아시스</div>
                                        <div class="cmt-text"><span>소중한 자료 올려주셔서 감사합니다.</span></div>
                                        <div class="cmt-date">2018-12-22</div>
                                    </li>
                                                    <li>
                                        <div class="cmt-icon"><img src="./img/cmt_5.gif" /></div>
                                        <div class="cmt-name">비스타</div>
                                        <div class="cmt-text"><span>내가 원하던 자료!! 선리플 후다운~</span></div>
                                        <div class="cmt-date">2018-12-22</div>
                                    </li>
                                                    <li>
                                        <div class="cmt-icon"><img src="./img/cmt_6.gif" /></div>
                                        <div class="cmt-name">멋진천사</div>
                                        <div class="cmt-text"><span>잘 받아갑니다~</span></div>
                                        <div class="cmt-date">2018-12-22</div>
                                    </li>
                                                </ul>
                                <div class="clear"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="footer" style="border-color:#00008B;">
                    본 사이트는 사이트 제작시 자동수집된 웹하드 자료 안내 페이지로 자료가 삭제되었거나 실제하지 않을수 있으며 다운로드는 해당 웹하드를 통해 다운 받으시면 됩니다.
                </div>
                
                
                
                
                <!-- ie6,7에서 사이드뷰가 게시판 목록에서 아래 사이드뷰에 가려지는 현상 수정 -->
                <!--[if lte IE 7]>
                <script>
                $(function() {
                    var $sv_use = $(".sv_use");
                    var count = $sv_use.length;
                
                    $sv_use.each(function() {
                        $(this).css("z-index", count);
                        $(this).css("position", "relative");
                        count = count - 1;
                    });
                });
                </script>
                <![endif]-->
                
                </body>
                </html>
            """),
            {"http://www.fileok.com", "http://www.fileok2.com"})
