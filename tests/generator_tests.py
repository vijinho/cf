from generator import generate as g


def setup():
    print("SETUP!")


def teardown():
    print("TEAR DOWN!")


def test_regions():
    assert len(g.regions) > 1


def test_eurozone():
    assert 'eurozone' in g.regions
    assert all(lang in [
        "AT",
        "BE",
        "CY",
        "DE",
        "EE",
        "ES",
        "FI",
        "FR",
        "GR",
        "IE",
        "IT",
        "LV",
        "LT",
        "LU",
        "MT",
        "NL",
        "PT",
        "SI",
        "SK"] for lang in g.regions['eurozone'])


def test_regions_gb():
    assert 'northernEurope' in g.regions
    assert 'GB' in g.regions['northernEurope']
    assert 'europe' in g.regions
    assert 'GB' in g.regions['europe']


def test_languages():
    assert len(g.languages) > 1


def test_languages_en():
    assert 'en' in g.languages
    en = g.languages['en']
    assert 'name' in en
    assert en['name'] == 'English'
    assert 'alpha2' in en
    assert en['alpha2'] == 'en'
    assert 'alpha3' in en
    assert en['alpha3'] == 'eng'


def test_currencies():
    assert len(g.currencies) > 1


def test_currencies_gbp():
    assert 'GBP' in g.currencies
    gbp = g.currencies['GBP']
    assert gbp['decimals'] == 2
    assert gbp['name'] == 'Pound sterling'
    assert int(gbp['number']) == 826


def test_rates():
    assert len(g.rates) > 1


def test_rates_gbp():
    assert '2015' in g.rates
    assert g.rates['2015']['rates']['GBP'] == 0.7285


def test_countries():
    assert len(g.countries) > 1


def test_countries_uk():
    assert len(g.countries) > 1
    assert 'UK' in g.countries
    uk = g.countries['UK']
    assert 'currencies' in uk
    assert 'GBP' in uk['currencies']
    assert 'languages' in uk
    assert all(
        lang in ['eng', 'cor', 'gle', 'gla', 'wel'] for lang in uk['languages'])
    assert 'name' in uk
    assert uk['name'] == 'United Kingdom'


def test_get_weighted_userid():
    assert g.get_weighted_userid(2015) > 0


def test_get_random_weighted_country():
    assert len(g.random_weighted_country()) == 2

