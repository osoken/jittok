def test_import_root() -> None:
    import jittok

    assert jittok.__package_name__ == "jittok"
