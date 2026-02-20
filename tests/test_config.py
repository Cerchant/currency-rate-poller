from app.config import Settings


def test_symbols_parsed_from_comma_separated_string():
    s = Settings(
        database_url="postgresql+asyncpg://test:test@localhost/test",
        symbols="EUR,RUB,GBP",
    )
    assert s.symbols_list == ["EUR", "RUB", "GBP"]


def test_symbols_strips_whitespace():
    s = Settings(
        database_url="postgresql+asyncpg://test:test@localhost/test",
        symbols=" EUR , RUB ",
    )
    assert s.symbols_list == ["EUR", "RUB"]
