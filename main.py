import requests
import re
from bs4 import BeautifulSoup


def get_url_in_html(html_content):
    """
    html 컨텐츠내 a 엘리먼트의 href url 주소를 추출함
    :param html_content:
    :return:
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.findAll('a')
    urls = {link.get('href') for link in links}
    return urls


def get_redirection_url(resp):
    """
    리다이렉션 url 리스트를 반환
    :param resp: 
    :return: 
    """
    urls = [hist.url for hist in reversed(resp.history[1:]) if hist.status_code in [301, 302]]
    urls.append(resp.url)
    return urls


def is_spem_link_domain(re_url, spemLinkDomains):
    """
    스펨 링크 안에 포함된 url 인지 확인
    :param re_url:
    :param spemLinkDomains:
    :return:
    True 스팸 링크에 포함
    False 스팸 링크에 미포함
    """
    for spam_link in spemLinkDomains:
        if spam_link in re_url:
            return True
    return False


def count_redirection_depth(resp):
    """
    요청한 url 의 리다이렉트 단계
    :param resp: 
    :return: 
    """
    return len(resp.history)


def extract_url_in_content(content):
    """
    카드 안의 문자열 컨텐츠 중에 url 추출
    :param content:
    :return:
    """
    ret = re.findall('https?://[^\s]+', content)
    return set(ret)


def is_spem_in_redirection_url(resp, spemLinkDomains, redirectionDepth):
    """
    리다이렉트 url 중에 스팸링크가 있는지 여부
    :param resp:
    :param spemLinkDomains:
    :param redirectionDepth:
    :return:
    """
    redirection_urls = get_redirection_url(resp)
    for re_url in redirection_urls[:redirectionDepth]:
        if is_spem_link_domain(re_url, spemLinkDomains):
            return True
    return False


def should_scan_in_html_content(resp, redirection_depth):
    """
    html 컨텐츠 검색이 필요한지 여부
    :param resp: 
    :param redirection_depth:
    :return:
    필요하면 True.
    필요하지 않다면 False
    """
    req_rd_depth = count_redirection_depth(resp)
    return  req_rd_depth < redirection_depth


def is_spem_in_html_content(resp, spemLinkDomains):
    """
    html a 테그 안 href 의 url 중에 스펨 링크가 있는지 여부
    :param resp:
    :param spemLinkDomains:
    :return:
    """
    link_urls = get_url_in_html(resp.text)
    for urls in link_urls:
        if is_spem_link_domain(urls, spemLinkDomains):
            return True
    return False


def is_spam(content, spem_link_domains, redirection_depth):
    """
    스팸여부를 알리는 main 함수
    :param content: 카드 컨텐츠
    :param spem_link_domains: 스팸 링크 도메인
    :param redirection_depth: 스팸 여부 찾는 단계
    :return: 
    """
    # 컨텐츠 안의 url 들을 전부 검색한다.
    urls_in_content = extract_url_in_content(content)

    for url in urls_in_content:
        resp = requests.get(url)

        if is_spem_in_redirection_url(resp, spem_link_domains, redirection_depth):
            return True

        if should_scan_in_html_content(resp, redirection_depth):
            return is_spem_in_html_content(resp, spem_link_domains)
        else:
            return False
