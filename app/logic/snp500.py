import re

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dparser

from app.logic.exceptions import ElementNotFoundException
from app.models import Snp500, db, Snp500Changes


def parse_companies(soup: BeautifulSoup):
    """
    parse snp500 companies, wiki
    """
    table = soup.find('table', {'id': 'constituents'})
    if not table:
        raise ElementNotFoundException('#constituents not found on a webpage')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    new_n = old_n = 0
    for tr in trs:
        is_new = True
        tds = tr.find_all('td')
        if len(tds) < 9:
            continue
        ticker = tds[0].text.strip()
        name = tds[1].text.strip()
        gics_sector = tds[3].text.strip()
        gics_subindustry = tds[4].text.strip()
        hq_location = tds[5].text.strip()
        info_source = 'wiki'
        _date = date_first_added_opt = tds[6].text.strip()
        r = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', _date)
        if r:
            _date = r.group(0)
        if len(_date) > 0:
            date_first_added = dparser.parse(_date).date()
        else:
            date_first_added = None
        cik = tds[7].text.strip()
        founded = tds[8].text.strip()
        try:
            model = Snp500.query.filter(Snp500.ticker == ticker).limit(1).one()
            is_new = False
            old_n += 1
        except:
            new_n += 1
            model = Snp500(
                ticker=ticker,
                name=name,
                gics_sector=gics_sector,
                gics_subindustry=gics_subindustry,
                hq_location=hq_location,
                info_source=info_source,
                date_first_added=date_first_added,
                date_first_added_opt=date_first_added_opt,
                cik=cik,
                founded=founded
            )
        if is_new:
            db.session.add(model)
        db.session.commit()
    return {
        'total': new_n + old_n,
        'new': new_n,
        'old': old_n,
    }


def parse_changes(soup: BeautifulSoup) -> dict:
    """
    parse changes within snp500 index, wiki
    """
    table = soup.find('table', {'id': 'changes'})
    if not table:
        raise ElementNotFoundException('#changes not found on a webpage')
    tbody = table.find('tbody')
    trs = tbody.find_all('tr')
    new_n = old_n = 0
    for tr in trs:
        is_new = True
        tds = tr.find_all('td')
        if len(tds) < 6:
            continue
        _date = tds[0].text.strip()
        if len(_date) > 0:
            date = dparser.parse(_date).date()
        else:
            date = None
            continue
        ticker_added = tds[1].text.strip()
        name_added = tds[2].text.strip()
        ticker_removed = tds[3].text.strip()
        name_removed = tds[4].text.strip()
        reason = tds[5].text.strip()
        info_source = 'wiki'
        and_vals = [
            Snp500Changes.date == date,
            Snp500Changes.ticker_added == ticker_added,
            Snp500Changes.ticker_removed == ticker_removed,
        ]
        try:
            model = Snp500Changes.query.filter(*and_vals).limit(1).one()
            is_new = False
            old_n += 1
        except:
            new_n += 1
            model = Snp500Changes(
                date=date,
                ticker_added=ticker_added,
                name_added=name_added,
                ticker_removed=ticker_removed,
                name_removed=name_removed,
                info_source=info_source,
                reason=reason
            )
        if is_new:
            db.session.add(model)
        db.session.commit()
    return {
        'total': new_n + old_n,
        'new': new_n,
        'old': old_n,
    }


def _do_parse_snp500_wiki_html(html) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    companies = parse_companies(soup)
    changes = parse_changes(soup)
    return {
        'companies': companies,
        'changes': changes
    }

def parse_snp500_wiki() -> dict:
    """
    parse S&P500 companies and changes from wiki
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    res = requests.get(url)
    return _do_parse_snp500_wiki_html(res.text)



